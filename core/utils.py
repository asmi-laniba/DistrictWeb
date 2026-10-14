import datetime
from django.http import HttpResponse
from django.template.loader import get_template

from xhtml2pdf import pisa
from io import BytesIO
from departments.models import Project, Department
from grievances.models import Complaint

def generate_pdf_report(request):
    projects = Project.objects.all()
    departments = Department.objects.all()
    complaints = Complaint.objects.all()
    
    template = get_template('core/report_template.html')
    context = {
        'projects': projects,
        'departments': departments,
        'complaints': complaints,
        'date': datetime.datetime.now(),
    }
    
    html = template.render(context)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None
