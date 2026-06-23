from django import forms
from .models import CourseConfig, UploadedFile

class UploadedFileForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['file']
        widgets = {
            'file': forms.ClearableFileInput(attrs={
                'class': 'form-control glass-input',
                'accept': '.xlsx, .xls',
                'id': 'excelFileUploader'
            })
        }

class CourseConfigForm(forms.ModelForm):
    class Meta:
        model = CourseConfig
        fields = [
            'course_name', 'course_code', 'department', 'regulation', 
            'faculty_name', 'academic_year', 'year_admitted', 'class_name'
        ]
        widgets = {
            'course_name': forms.TextInput(attrs={'class': 'form-control glass-input'}),
            'course_code': forms.TextInput(attrs={'class': 'form-control glass-input'}),
            'department': forms.TextInput(attrs={'class': 'form-control glass-input'}),
            'regulation': forms.TextInput(attrs={'class': 'form-control glass-input'}),
            'faculty_name': forms.TextInput(attrs={'class': 'form-control glass-input'}),
            'academic_year': forms.TextInput(attrs={'class': 'form-control glass-input'}),
            'year_admitted': forms.TextInput(attrs={'class': 'form-control glass-input'}),
            'class_name': forms.TextInput(attrs={'class': 'form-control glass-input'}),
        }

