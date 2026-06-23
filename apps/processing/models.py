from django.db import models

def get_default_co_po_mapping():
    return {
        "CO1": {"PO-1": 3.0, "PO-2": 3.0, "PO-3": 3.0, "PO-4": 3.0, "PO-5": None, "PO-6": None, "PO-7": None, "PO-8": None, "PO-9": None, "PO-10": None, "PO-11": None, "PO-12": 3.0, "PSO-1": 1.0, "PSO-2": None, "PSO-3": 1.0},
        "CO2": {"PO-1": 3.0, "PO-2": 3.0, "PO-3": 3.0, "PO-4": 3.0, "PO-5": None, "PO-6": None, "PO-7": None, "PO-8": None, "PO-9": None, "PO-10": None, "PO-11": None, "PO-12": 3.0, "PSO-1": 1.0, "PSO-2": None, "PSO-3": 1.0},
        "CO3": {"PO-1": 3.0, "PO-2": 3.0, "PO-3": 3.0, "PO-4": 3.0, "PO-5": None, "PO-6": None, "PO-7": None, "PO-8": None, "PO-9": None, "PO-10": None, "PO-11": None, "PO-12": 3.0, "PSO-1": 1.0, "PSO-2": None, "PSO-3": 1.0},
        "CO4": {"PO-1": 3.0, "PO-2": 3.0, "PO-3": 3.0, "PO-4": 3.0, "PO-5": None, "PO-6": None, "PO-7": None, "PO-8": None, "PO-9": None, "PO-10": None, "PO-11": None, "PO-12": 3.0, "PSO-1": 1.0, "PSO-2": None, "PSO-3": None},
        "CO5": {"PO-1": 3.0, "PO-2": 3.0, "PO-3": 3.0, "PO-4": 3.0, "PO-5": None, "PO-6": None, "PO-7": None, "PO-8": None, "PO-9": None, "PO-10": None, "PO-11": None, "PO-12": 3.0, "PSO-1": 1.0, "PSO-2": None, "PSO-3": 1.0},
    }

def get_default_survey_inputs():
    return {
        "CO1": "((46/50)*3+(4/50)*2)",
        "CO2": "((45/50)*3+(5/50)*2+(0/52)*1)",
        "CO3": "((42/50)*3+(8/50)*2+(0/52))",
        "CO4": "((46/50)*3+(2/50)*2+(2/50))",
        "CO5": "((42/50)*3+(5/50)*2+(3/50))"
    }

class CourseConfig(models.Model):
    course_name = models.CharField(max_length=200, default="AC Machines Lab")
    course_code = models.CharField(max_length=50, default="C0213")
    department = models.CharField(max_length=100, default="B.Tech. - EEE")
    regulation = models.CharField(max_length=50, default="MR22")
    faculty_name = models.CharField(max_length=200, default="Dr. P. Marimuthu")
    academic_year = models.CharField(max_length=50, default="2025-2026")
    year_admitted = models.CharField(max_length=50, default="2025  -  2026")
    class_name = models.CharField(max_length=100, default="III YEAR /V SEM")
    total_students = models.IntegerField(default=66)
    
    # Adjustable mapping coefficients
    co_po_mapping = models.JSONField(default=get_default_co_po_mapping)
    
    # Mathematical strings for indirect attainment
    survey_inputs = models.JSONField(default=get_default_survey_inputs)

    def __str__(self):
        return f"{self.course_name} ({self.course_code}) - {self.academic_year}"

class UploadedFile(models.Model):
    STATUS_CHOICES = [
        ('uploaded', 'Uploaded'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    file = models.FileField(upload_to='uploads/')
    original_filename = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='uploaded')
    student_count = models.IntegerField(default=0)
    error_message = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.original_filename} ({self.status}) - {self.timestamp}"

class GeneratedReport(models.Model):
    uploaded_file = models.OneToOneField(UploadedFile, on_delete=models.CASCADE, related_name='report')
    file = models.FileField(upload_to='reports/')
    filename = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    # Calculated final outcomes
    co1_attainment = models.FloatField(default=0.0)
    co2_attainment = models.FloatField(default=0.0)
    co3_attainment = models.FloatField(default=0.0)
    co4_attainment = models.FloatField(default=0.0)
    co5_attainment = models.FloatField(default=0.0)

    def __str__(self):
        return f"Report for {self.uploaded_file.original_filename} - {self.timestamp}"
