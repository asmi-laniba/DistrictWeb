import logging
from .models import AuditLog

class AuditLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        if request.user.is_authenticated and request.method in ['POST', 'PUT', 'DELETE']:
            # Log significant actions
            action = f"{request.method} request to {request.path}"
            ip = request.META.get('REMOTE_ADDR')
            AuditLog.objects.create(user=request.user, action=action, ip_address=ip)
            
        return response
