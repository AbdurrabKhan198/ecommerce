#!/usr/bin/env python
"""Simple test to check homepage"""
import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'womens_wear_ecommerce.settings')
django.setup()

# Test if our apps are loaded
from django.apps import apps
installed_apps = [app.label for app in apps.get_app_configs()]
print(f"Installed apps: {installed_apps}")

# Check if our shop app is loaded
if 'shop' in installed_apps:
    print("Shop app is loaded successfully!")
    try:
        from shop.views import homepage
        print("Homepage view imported successfully!")
        
        # Test URL reverse
        from django.urls import reverse
        url = reverse('shop:homepage')
        print(f"Homepage URL: {url}")
        
    except Exception as e:
        print(f"Error importing homepage view: {e}")
else:
    print("Shop app is NOT loaded")

# Test URL patterns
from django.urls import get_resolver
resolver = get_resolver()
print(f"URL patterns loaded: {len(resolver.url_patterns)} patterns")
