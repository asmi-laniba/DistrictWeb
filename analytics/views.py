from django.shortcuts import render
from .models import Prediction, Alert
from departments.models import Project

def prediction_dashboard(request):
    predictions = Prediction.objects.select_related('project').all()
    high_risk_projects = predictions.filter(risk_score__gt=0.7)
    
    context = {
        'predictions': predictions,
        'high_risk_projects': high_risk_projects,
    }
    return render(request, 'analytics/predictions.html', context)
