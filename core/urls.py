from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('deployment/<int:pk>/', views.deployment_detail, name='deployment_detail'),
    path('api/health/', views.api_health, name='api_health'),
    path('api/deployments/', views.api_deployments, name='api_deployments'),
    path('api/deployment/create/', views.api_create_deployment, name='api_create_deployment'),
]
