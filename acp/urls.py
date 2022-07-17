"""Defining URL-patterns for acp app"""
from django.urls import path
from . import views

app_name = 'acp'

urlpatterns = [
    path('', views.home, name='home'),  # Home page with ACP
    path('jobs/', views.jobs, name='jobs'),  # Joblist page
    path('nodes/', views.nodes, name='nodes'),  # Nodelist page
]
