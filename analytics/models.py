from django.db import models
from departments.models import Project

class Prediction(models.Model):
    project = models.OneToOneField(Project, on_delete=models.CASCADE, related_name='prediction')
    predicted_delay_days = models.IntegerField(default=0)
    risk_score = models.FloatField(default=0.0) # 0 to 1
    shortage_probability = models.FloatField(default=0.0)
    recommendation = models.TextField(blank=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Prediction for {self.project.name}"

class Alert(models.Model):
    SEVERITY_CHOICES = (
        ('info', 'Info'),
        ('warning', 'Warning'),
        ('danger', 'Critical'),
    )
    title = models.CharField(max_length=200)
    message = models.TextField()
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES, default='info')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.severity.upper()}: {self.title}"
