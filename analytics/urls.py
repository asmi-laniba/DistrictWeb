from django.urls import path
from . import views

urlpatterns = [
    path('predictions/', views.prediction_dashboard, name='prediction_dashboard'),
]
