import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import FileResponse, Http404
from django.conf import settings
import json

from .models import CourseConfig, UploadedFile, GeneratedReport
from .forms import UploadedFileForm, CourseConfigForm
from .report_generator import process_uploaded_workbook
from .calc_engine import safe_eval_survey

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "Logged out successfully.")
    return redirect('login')

@login_required
def dashboard_view(request):
    # Load or create first course config
    config = CourseConfig.objects.first()
    if not config:
        config = CourseConfig.objects.create()
        
    uploads = UploadedFile.objects.all().order_by('-timestamp')[:10]
    total_uploads = UploadedFile.objects.count()
    completed_reports = UploadedFile.objects.filter(status='completed').count()
    failed_reports = UploadedFile.objects.filter(status='failed').count()
    
    # Fetch the latest processed report for dynamic dashboard analytics
    latest_report = GeneratedReport.objects.select_related('uploaded_file').order_by('-timestamp').first()
    
    chart_data = {
        'labels': ['CO1', 'CO2', 'CO3', 'CO4', 'CO5'],
        'co_direct': [0.0] * 5,
        'co_indirect': [0.0] * 5,
        'co_final': [0.0] * 5,
    }
    
    if latest_report:
        # Since all COs have same direct attainment in this lab scheme, let's re-calculate to fetch individual direct/indirects
        # or load directly. The database has final values.
        survey_inputs = config.survey_inputs
        co1_ind = safe_eval_survey(survey_inputs.get('CO1', '0'))
        co2_ind = safe_eval_survey(survey_inputs.get('CO2', '0'))
        co3_ind = safe_eval_survey(survey_inputs.get('CO3', '0'))
        co4_ind = safe_eval_survey(survey_inputs.get('CO4', '0'))
        co5_ind = safe_eval_survey(survey_inputs.get('CO5', '0'))
        
        # Calculate direct from final and indirect: final = 0.8 * direct + 0.2 * indirect => direct = (final - 0.2 * indirect) / 0.8
        def get_dir(fin, ind):
            try:
                return round((fin - 0.2 * ind) / 0.8, 2)
            except Exception:
                return 0.0
                
        co1_dir = get_dir(latest_report.co1_attainment, co1_ind)
        co2_dir = get_dir(latest_report.co2_attainment, co2_ind)
        co3_dir = get_dir(latest_report.co3_attainment, co3_ind)
        co4_dir = get_dir(latest_report.co4_attainment, co4_ind)
        co5_dir = get_dir(latest_report.co5_attainment, co5_ind)
        
        chart_data['co_direct'] = [co1_dir, co2_dir, co3_dir, co4_dir, co5_dir]
        chart_data['co_indirect'] = [co1_ind, co2_ind, co3_ind, co4_ind, co5_ind]
        chart_data['co_final'] = [
            latest_report.co1_attainment,
            latest_report.co2_attainment,
            latest_report.co3_attainment,
            latest_report.co4_attainment,
            latest_report.co5_attainment,
        ]
        
    context = {
        'config': config,
        'uploads': uploads,
        'total_uploads': total_uploads,
        'completed_reports': completed_reports,
        'failed_reports': failed_reports,
        'latest_report': latest_report,
        'chart_data_json': json.dumps(chart_data)
    }
    return render(request, 'dashboard.html', context)

@login_required
def upload_view(request):
    config = CourseConfig.objects.first()
    if not config:
        config = CourseConfig.objects.create()
        
    if request.method == 'POST':
        form = UploadedFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save(commit=False)
            uploaded_file.original_filename = request.FILES['file'].name
            uploaded_file.status = 'uploaded'
            uploaded_file.save()
            return redirect('process', file_id=uploaded_file.id)
    else:
        form = UploadedFileForm()
        
    return render(request, 'upload.html', {'form': form, 'config': config})

@login_required
def process_view(request, file_id):
    uploaded_file = get_object_or_404(UploadedFile, id=file_id)
    
    # We render a processing loading template which will call the processing view via redirect or ajax
    # To keep it robust, we execute the process_uploaded_workbook inline and redirect to report detail
    # or fail if there's an error.
    if request.method == 'GET' and 'run' in request.GET:
        try:
            config = CourseConfig.objects.first()
            report = process_uploaded_workbook(uploaded_file.id, config_id=config.id if config else None)
            messages.success(request, "Excel Attainment spreadsheet successfully compiled and generated!")
            return redirect('report_detail', report_id=report.id)
        except Exception as e:
            messages.error(request, f"Processing Failed: {str(e)}")
            return redirect('dashboard')
            
    return render(request, 'process.html', {'uploaded_file': uploaded_file})

@login_required
def report_detail_view(request, report_id):
    report = get_object_or_404(GeneratedReport, id=report_id)
    config = CourseConfig.objects.first()
    
    # Derive direct and indirect values for display/charts
    survey_inputs = config.survey_inputs if config else {}
    co1_ind = safe_eval_survey(survey_inputs.get('CO1', '0'))
    co2_ind = safe_eval_survey(survey_inputs.get('CO2', '0'))
    co3_ind = safe_eval_survey(survey_inputs.get('CO3', '0'))
    co4_ind = safe_eval_survey(survey_inputs.get('CO4', '0'))
    co5_ind = safe_eval_survey(survey_inputs.get('CO5', '0'))
    
    def get_dir(fin, ind):
        try:
            return round((fin - 0.2 * ind) / 0.8, 2)
        except Exception:
            return 0.0
            
    co1_dir = get_dir(report.co1_attainment, co1_ind)
    co2_dir = get_dir(report.co2_attainment, co2_ind)
    co3_dir = get_dir(report.co3_attainment, co3_ind)
    co4_dir = get_dir(report.co4_attainment, co4_ind)
    co5_dir = get_dir(report.co5_attainment, co5_ind)
    
    chart_data = {
        'labels': ['CO1', 'CO2', 'CO3', 'CO4', 'CO5'],
        'co_direct': [co1_dir, co2_dir, co3_dir, co4_dir, co5_dir],
        'co_indirect': [co1_ind, co2_ind, co3_ind, co4_ind, co5_ind],
        'co_final': [
            report.co1_attainment,
            report.co2_attainment,
            report.co3_attainment,
            report.co4_attainment,
            report.co5_attainment
        ]
    }
    
    context = {
        'report': report,
        'config': config,
        'chart_data_json': json.dumps(chart_data)
    }
    return render(request, 'report_detail.html', context)

@login_required
def download_report_view(request, report_id):
    report = get_object_or_404(GeneratedReport, id=report_id)
    file_path = report.file.path
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=report.filename)
    raise Http404("Attainment spreadsheet file not found on server.")

@login_required
def config_edit_view(request):
    config = CourseConfig.objects.first()
    if not config:
        config = CourseConfig.objects.create()
        
    if request.method == 'POST':
        form = CourseConfigForm(request.POST, instance=config)
        if form.is_valid():
            # Update form fields
            config = form.save(commit=False)
            
            # Read CO-PO weight inputs from POST
            new_mapping = {}
            po_list = [
                "PO-1", "PO-2", "PO-3", "PO-4", "PO-5", "PO-6", "PO-7", "PO-8", "PO-9", "PO-10", "PO-11", "PO-12", "PSO-1", "PSO-2", "PSO-3"
            ]
            for co_idx in range(1, 6):
                co_key = f"CO{co_idx}"
                new_mapping[co_key] = {}
                for po in po_list:
                    input_name = f"weight_{co_key}_{po}"
                    val_str = request.POST.get(input_name, "").strip()
                    if val_str:
                        try:
                            new_mapping[co_key][po] = float(val_str)
                        except ValueError:
                            new_mapping[co_key][po] = None
                    else:
                        new_mapping[co_key][po] = None
            
            config.co_po_mapping = new_mapping
            
            # Read survey formulas from POST
            new_survey = {}
            for co_idx in range(1, 6):
                co_key = f"CO{co_idx}"
                input_name = f"survey_{co_key}"
                new_survey[co_key] = request.POST.get(input_name, "").strip()
                
            config.survey_inputs = new_survey
            config.save()
            
            messages.success(request, "Course outcomes and dynamic weight distributions updated!")
            return redirect('dashboard')
    else:
        form = CourseConfigForm(instance=config)
        
    # Render table grids
    po_list = [
        "PO-1", "PO-2", "PO-3", "PO-4", "PO-5", "PO-6", "PO-7", "PO-8", "PO-9", "PO-10", "PO-11", "PO-12", "PSO-1", "PSO-2", "PSO-3"
    ]
    
    context = {
        'form': form,
        'config': config,
        'po_list': po_list,
        'co_list': ["CO1", "CO2", "CO3", "CO4", "CO5"],
        'mapping': config.co_po_mapping,
        'survey': config.survey_inputs
    }
    return render(request, 'config_edit.html', context)
