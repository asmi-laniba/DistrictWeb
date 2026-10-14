import json
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from departments.models import Project, Department
from grievances.models import Complaint
from analytics.models import Alert
from django.db.models import Sum, Count
from .utils import generate_pdf_report


def home(request):
    return render(request, 'core/home.html')

@login_required
def dashboard(request):
    projects_count = Project.objects.count()
    completed_projects = Project.objects.filter(status='completed').count()
    delayed_projects = Project.objects.filter(status='delayed').count()
    
    stats = Project.objects.aggregate(
        total_budget=Sum('budget'),
        total_used=Sum('budget_used')
    )
    total_budget = stats['total_budget'] or 0
    total_used = stats['total_used'] or 0
    budget_remaining = total_budget - total_used
    
    complaints_count = Complaint.objects.count()
    pending_complaints = Complaint.objects.filter(status='pending').count()
    
    recent_alerts = Alert.objects.order_by('-created_at')[:5]
    
    # Department performance data for charts
    depts = Department.objects.annotate(
        proj_count=Count('projects', distinct=True),
        comp_count=Count('complaints', distinct=True)
    ).order_by('name')
    
    chart_labels = [dept.get_name_display() for dept in depts]
    chart_utilization = []
    
    for dept in depts:
        # Calculate dynamic utilization per department
        dept_stats = dept.projects.aggregate(
            tot=Sum('budget'),
            usd=Sum('budget_used')
        )
        tot = dept_stats['tot'] or 0
        usd = dept_stats['usd'] or 0
        util = float(usd / tot * 100) if tot > 0 else 0
        chart_utilization.append(round(util, 1))
    
    context = {
        'projects_count': projects_count,
        'completed_projects': completed_projects,
        'delayed_projects': delayed_projects,
        'total_budget': total_budget,
        'total_used': total_used,
        'budget_remaining': budget_remaining,
        'complaints_count': complaints_count,
        'pending_complaints': pending_complaints,
        'recent_alerts': recent_alerts,
        'depts': depts,
        'chart_labels': json.dumps(chart_labels),
        'chart_utilization': json.dumps(chart_utilization),
        'kpi_target': json.dumps([85] * len(chart_labels)),
    }
    return render(request, 'core/dashboard.html', context)
