#!/usr/bin/env python
"""Simple test to check Django URL patterns"""
import os
import sys
import django
from django.conf import settings

# Add current directory to path
sys.path.insert(0, os.getcwd())

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'womens_wear_ecommerce.settings')
django.setup()

# Test URL patterns
from django.urls import reverse
from django.test import Client

client = Client()

try:
    # Test homepage URL
    response = client.get('/')
    print(f"Homepage status: {response.status_code}")
    if response.status_code == 200:
        print("✅ Homepage is working!")
        print(f"Content type: {response.get('Content-Type')}")
        print(f"Content length: {len(response.content)} bytes")
    else:
        print(f"❌ Homepage error: {response.status_code}")
        
except Exception as e:
    print(f"❌ Error testing homepage: {e}")

# Test if our apps are loaded
from django.apps import apps
installed_apps = [app.label for app in apps.get_app_configs()]
print(f"\nInstalled apps: {installed_apps}")

# Check if our shop app is loaded
if 'shop' in installed_apps:
    print("✅ Shop app is loaded")
    try:
        from shop.views import homepage
        print("✅ Homepage view imported successfully")
    except ImportError as e:
        print(f"❌ Cannot import homepage view: {e}")
else:
    print("❌ Shop app is NOT loaded")
