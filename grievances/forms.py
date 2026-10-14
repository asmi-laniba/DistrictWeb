from django import forms
from .models import Complaint

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['citizen_name', 'citizen_email', 'department', 'subject', 'description', 'priority']
