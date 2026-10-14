import csv
from django.shortcuts import render, redirect, get_object_or_404
from .models import Complaint
from .forms import ComplaintForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

def submit_grievance(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            if request.user.is_authenticated:
                complaint.user = request.user
            complaint.save()
            messages.success(request, f'Grievance submitted successfully. Your tracking ID is: {complaint.tracking_id}')
            return redirect('home')
    else:
        form = ComplaintForm()
    return render(request, 'grievances/submit.html', {'form': form})

def track_grievance(request):
    complaint = None
    if 'tracking_id' in request.GET:
        tid = request.GET.get('tracking_id')
        complaint = Complaint.objects.filter(tracking_id=tid).first()
        if not complaint:
            messages.error(request, "Invalid tracking ID.")
    return render(request, 'grievances/track.html', {'complaint': complaint})

@login_required
def manage_grievances(request):
    if request.method == 'POST' and 'update_status' in request.POST:
        if not request.user.is_superuser:
            messages.error(request, "Only administrators can update grievance status.")
            return redirect('manage_grievances')
            
        complaint_id = request.POST.get('complaint_id')
        status = request.POST.get('status')
        complaint = get_object_or_404(Complaint, id=complaint_id)
        complaint.status = status
        complaint.save()
        messages.success(request, f'Status for tracking ID {complaint.tracking_id} updated to {complaint.get_status_display()}.')
        return redirect('manage_grievances')
        
    complaints = Complaint.objects.order_by('-created_at')
    return render(request, 'grievances/manage.html', {'complaints': complaints})

@login_required
def export_grievances_pdf(request):
    complaints = Complaint.objects.all().order_by('-created_at')
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="grievances_report.pdf"'
    
    doc = SimpleDocTemplate(response, pagesize=landscape(letter))
    elements = []
    
    styles = getSampleStyleSheet()
    title_style = styles['Heading1']
    elements.append(Paragraph("District Grievance Report", title_style))
    elements.append(Paragraph(f"Generated on: {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
    elements.append(Paragraph("<br/><br/>", styles['Normal']))
    
    data = [["Tracking ID", "Citizen", "Department", "Subject", "Priority", "Status", "Date"]]
    for complaint in complaints:
        data.append([
            complaint.tracking_id,
            complaint.citizen_name,
            str(complaint.department),
            complaint.subject,
            complaint.get_priority_display(),
            complaint.get_status_display(),
            complaint.created_at.strftime('%b %d, %Y')
        ])
        
    table = Table(data, repeatRows=1)
    
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('WORDWRAP', (0, 0), (-1, -1), True)
    ])
    table.setStyle(style)
    elements.append(table)
    
    doc.build(elements)
    return response

@login_required
def export_grievances_csv(request):
    complaints = Complaint.objects.all().order_by('-created_at')
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="grievances_report.csv"'
    
    writer = csv.writer(response)
    writer.writerow(["Tracking ID", "Citizen", "Department", "Subject", "Priority", "Status", "Date"])
    
    for complaint in complaints:
        writer.writerow([
            complaint.tracking_id,
            complaint.citizen_name,
            str(complaint.department),
            complaint.subject,
            complaint.get_priority_display(),
            complaint.get_status_display(),
            complaint.created_at.strftime('%b %d, %Y')
        ])
        
    return response
