from django.urls import path
from . import views

urlpatterns = [
    path('projects/add/', views.add_project, name='add_project'),
    path('projects/<int:pk>/', views.project_detail, name='project_detail'),
    path('projects/<int:pk>/edit/', views.edit_project, name='edit_project'),
    path('', views.department_list, name='department_list'),
    path('<str:dept_name>/', views.department_detail, name='department_detail'),
]
