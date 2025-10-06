#!/usr/bin/env python
"""Test server to verify our Django setup"""
import os
import sys
import django
from django.core.wsgi import get_wsgi_application
from django.core.management import execute_from_command_line

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'womens_wear_ecommerce.settings')

if __name__ == '__main__':
    print("Starting test Django server...")
    print(f"Current directory: {os.getcwd()}")
    print(f"Python executable: {sys.executable}")
    
    # Add current directory to Python path
    if os.getcwd() not in sys.path:
        sys.path.insert(0, os.getcwd())
    
    django.setup()
    
    print("Django apps loaded:")
    from django.apps import apps
    for app in apps.get_app_configs():
        print(f"  - {app.label}")
    
    print("\nStarting server on port 8004...")
    execute_from_command_line(['manage.py', 'runserver', '8004'])
