import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'district_plus.settings')
django.setup()

from django.contrib.auth import get_user_model
from departments.models import Department, Project
from grievances.models import Complaint
from analytics.models import Alert, Prediction
import datetime

User = get_user_model()

def populate():
    # Create Superuser
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123', role='collector')
        print("Superuser 'admin' created.")

    # Create Departments
    depts = [
        ('health', 'Health', 'Health and Family Welfare'),
        ('education', 'Education', 'School and Higher Education'),
        ('revenue', 'Revenue', 'District Revenue and Land Records'),
        ('public_works', 'Public Works', 'PWD and Infrastructure'),
        ('police', 'Police', 'District Police and Security'),
    ]
    for code, name, desc in depts:
        Department.objects.get_or_create(name=code, defaults={'description': desc})
    print("Departments created.")

    # Create Projects
    dept_map = {d.name: d for d in Department.objects.all()}
    projects = [
        ('District Hospital Extension', 'health', 50000000, 25000000, 'in_progress', 50),
        ('Primary School Renovation', 'education', 2000000, 1800000, 'completed', 100),
        ('City Surveillance Upgrade', 'police', 15000000, 5000000, 'in_progress', 33),
        ('Smart Water Irrigation', 'public_works', 30000000, 20000000, 'delayed', 60),
        ('Revenue Record Digitization', 'revenue', 10000000, 9000000, 'in_progress', 90),
    ]
    for name, dept_code, budget, used, status, progress in projects:
        dept = dept_map[dept_code]
        p, created = Project.objects.get_or_create(
            name=name, department=dept,
            defaults={
                'budget': budget,
                'budget_used': used,
                'status': status,
                'progress': progress,
                'start_date': datetime.date(2023, 1, 1),
                'end_date': datetime.date(2024, 12, 31)
            }
        )
        # Create Dummy Prediction
        Prediction.objects.get_or_create(
            project=p,
            defaults={
                'predicted_delay_days': 15 if status == 'delayed' else 0,
                'risk_score': 0.8 if status == 'delayed' else 0.2,
                'shortage_probability': 0.5,
                'recommendation': 'Allocate more resources.' if status == 'delayed' else 'On track.'
            }
        )
    print("Projects and Predictions created.")

    # Create Complaints
    complaints = [
        ('John Doe', 'john@example.com', 'health', 'Hospital cleanliness', 'high'),
        ('Jane Smith', 'jane@example.com', 'public_works', 'Potholes on Main Street', 'medium'),
        ('Bob Wilson', 'bob@example.com', 'police', 'Illegal parking', 'low'),
    ]
    for cname, email, dept_code, subject, priority in complaints:
        dept = dept_map[dept_code]
        Complaint.objects.get_or_create(
            citizen_name=cname, citizen_email=email, department=dept,
            subject=subject,
            defaults={'description': 'Detailed complaint description...', 'priority': priority, 'status': 'pending'}
        )
    print("Complaints created.")

    # Create Alerts
    Alert.objects.get_or_create(title="Project Delayed", message="Smart Water Irrigation project is significantly delayed.", severity="danger")
    Alert.objects.get_or_create(title="High Grievances", message="Health department has seen a 20% increase in complaints.", severity="warning")
    print("Alerts created.")

if __name__ == '__main__':
    populate()
