import os
from django.conf import settings
from .models import CourseConfig, UploadedFile, GeneratedReport
from .excel_reader import read_input_excel
from .calc_engine import calculate_co_attainment
from .excel_writer import write_output_excel

def process_uploaded_workbook(uploaded_file_id, config_id=None):
    """
    Orchestration pipeline:
    1. Retrieve the UploadedFile and CourseConfig
    2. Extract student rows from the uploaded sheet using excel_reader
    3. Run pure Python calculations using calc_engine
    4. Construct the styled output workbook using excel_writer (with formulas)
    5. Save metrics into GeneratedReport and flag completion status
    """
    try:
        uploaded_file = UploadedFile.objects.get(id=uploaded_file_id)
        uploaded_file.status = 'processing'
        uploaded_file.save()
        
        # Load course config (fallback to first available or default)
        if config_id:
            config = CourseConfig.objects.get(id=config_id)
        else:
            config = CourseConfig.objects.first()
            if not config:
                config = CourseConfig.objects.create() # defaults trigger automatically
                
        input_path = uploaded_file.file.path
        
        # 1. Read input rows
        students = read_input_excel(input_path)
        
        # 2. Update Student Count in UploadedFile
        uploaded_file.student_count = len(students)
        uploaded_file.save()
        
        if len(students) == 0:
            raise ValueError("No student records could be successfully parsed from the uploaded Excel sheet. Please verify row structures.")
            
        # 3. Calculate float outcomes in Python for DB/Charts
        analysis = calculate_co_attainment(students, config.survey_inputs)
        
        # 4. Write fully styled output workbook with live Excel formulas and embedded chart
        output_filename = f"Generated_Attainment_{uploaded_file.id}.xlsx"
        output_dir = os.path.join(settings.MEDIA_ROOT, 'reports')
        os.makedirs(output_dir, exist_ok=True)
        
        output_path = os.path.join(output_dir, output_filename)
        
        write_output_excel(students, config, output_path)
        
        # 5. Populate GeneratedReport ORM entry
        report_file_rel = os.path.join('reports', output_filename)
        
        attainments = analysis['attainments']
        
        # Create or update report
        report, created = GeneratedReport.objects.update_or_create(
            uploaded_file=uploaded_file,
            defaults={
                'file': report_file_rel,
                'filename': output_filename,
                'co1_attainment': attainments['CO1']['final'],
                'co2_attainment': attainments['CO2']['final'],
                'co3_attainment': attainments['CO3']['final'],
                'co4_attainment': attainments['CO4']['final'],
                'co5_attainment': attainments['CO5']['final'],
            }
        )
        
        # Update uploaded file state to completed
        uploaded_file.status = 'completed'
        uploaded_file.save()
        
        return report
        
    except Exception as e:
        # Capture error states and set to failed
        try:
            uploaded_file = UploadedFile.objects.get(id=uploaded_file_id)
            uploaded_file.status = 'failed'
            uploaded_file.error_message = str(e)
            uploaded_file.save()
        except Exception:
            pass
        raise e
