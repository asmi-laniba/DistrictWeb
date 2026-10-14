from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core.views import home, dashboard, generate_pdf_report

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('dashboard/', dashboard, name='dashboard'),
    path('report/', generate_pdf_report, name='generate_report'),
    path('accounts/', include('accounts.urls')),

    path('departments/', include('departments.urls')),
    path('grievances/', include('grievances.urls')),
    path('analytics/', include('analytics.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
