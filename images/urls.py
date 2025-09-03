# your_app/urls.py - URL configuration
from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_image, name='upload_image'),
    # Add other API endpoints here
]