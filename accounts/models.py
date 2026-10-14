from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('collector', 'District Collector'),
        ('dept_head', 'Department Head'),
        ('staff', 'Staff'),
        ('viewer', 'Viewer'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='viewer')
    department = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
