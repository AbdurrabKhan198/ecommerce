#!/usr/bin/env python
"""Debug URL patterns"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'womens_wear_ecommerce.settings')
django.setup()

from django.urls import get_resolver
from django.conf import settings

print(f"DEBUG setting: {settings.DEBUG}")
print(f"ROOT_URLCONF: {settings.ROOT_URLCONF}")

resolver = get_resolver()
print(f"\nNumber of URL patterns: {len(resolver.url_patterns)}")

print("\nURL patterns:")
for i, pattern in enumerate(resolver.url_patterns):
    print(f"  {i+1}. {pattern}")
    
print("\nTrying to import shop.urls directly:")
try:
    from shop import urls as shop_urls
    print(f"Shop URLs imported successfully: {len(shop_urls.urlpatterns)} patterns")
    for pattern in shop_urls.urlpatterns:
        print(f"  - {pattern}")
except Exception as e:
    print(f"Error importing shop.urls: {e}")

print("\nTrying to resolve root URL '/':")
try:
    from django.urls import resolve
    match = resolve('/')
    print(f"Resolved to: {match.view_name} -> {match.func}")
except Exception as e:
    print(f"Error resolving '/': {e}")
