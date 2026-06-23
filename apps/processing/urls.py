from django.urls import path
from . import views

urlpatterns = [
    # Dashboard & History
    path('', views.dashboard_view, name='dashboard'),
    
    # Auth
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    
    # Report Operations
    path('upload/', views.upload_view, name='upload'),
    path('process/<int:file_id>/', views.process_view, name='process'),
    path('report/<int:report_id>/', views.report_detail_view, name='report_detail'),
    path('download/<int:report_id>/', views.download_report_view, name='download_report'),
    
    # Configuration Details
    path('config/edit/', views.config_edit_view, name='config_edit'),
]
