"""Defining URL-patterns for acp app"""
from django.urls import path
from . import views

app_name = 'acp'

urlpatterns = [
    path('', views.home, name='home'),  # Home page
]
