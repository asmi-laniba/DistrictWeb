from django.urls import path
from . import views

urlpatterns = [
    path('submit/', views.submit_grievance, name='submit_grievance'),
    path('track/', views.track_grievance, name='track_grievance'),
    path('manage/', views.manage_grievances, name='manage_grievances'),
    path('export-pdf/', views.export_grievances_pdf, name='export_grievances_pdf'),
    path('export-csv/', views.export_grievances_csv, name='export_grievances_csv'),
]
