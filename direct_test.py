#!/usr/bin/env python
"""Direct test of our Django setup"""
import os
import django
from django.conf import settings

# Configure Django settings directly
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'womens_wear_ecommerce.settings')
django.setup()

print(f"DEBUG: {settings.DEBUG}")
print(f"ROOT_URLCONF: {settings.ROOT_URLCONF}")
print(f"INSTALLED_APPS: {settings.INSTALLED_APPS}")

# Test URL resolution
from django.test import Client
from django.urls import reverse, resolve

print("\nTesting URL resolution:")
try:
    homepage_url = reverse('shop:homepage')
    print(f"Homepage URL: {homepage_url}")
    
    resolved = resolve('/')
    print(f"Root URL resolves to: {resolved.func.__name__}")
    
    # Test with Django test client
    client = Client()
    response = client.get('/')
    print(f"Test client response: {response.status_code}")
    print(f"Content (first 100 chars): {response.content[:100]}")
    
except Exception as e:
    print(f"Error: {e}")

# Try to import and call our view directly
print("\nTesting view import:")
try:
    from shop.views import homepage
    print("✅ Homepage view imported successfully")
    
    # Create a mock request
    from django.test import RequestFactory
    factory = RequestFactory()
    request = factory.get('/')
    
    response = homepage(request)
    print(f"Direct view call response: {response.status_code}")
    print(f"Content: {response.content[:100]}")
    
except Exception as e:
    print(f"❌ Error calling view: {e}")
