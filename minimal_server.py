#!/usr/bin/env python
"""Minimal Django server to test"""
import os
import sys
from django.conf import settings
from django.http import HttpResponse
from django.urls import path
from django.core.wsgi import get_wsgi_application
from django.core.management import execute_from_command_line

# Add current directory to path
sys.path.insert(0, os.getcwd())

# Minimal Django configuration
if not settings.configured:
    settings.configure(
        DEBUG=True,
        SECRET_KEY='test-key-123',
        ALLOWED_HOSTS=['*'],
        ROOT_URLCONF=__name__,
        INSTALLED_APPS=[
            'django.contrib.contenttypes',
            'django.contrib.auth',
        ],
    )

def test_view(request):
    return HttpResponse("""
    <html>
    <head><title>MINIMAL TEST WORKING</title></head>
    <body style="background: #e91e63; color: white; text-align: center; padding: 50px; font-family: Arial;">
        <h1>✅ MINIMAL DJANGO TEST WORKING!</h1>
        <p>If you see this, Django is working correctly.</p>
        <p>The issue might be with our main project configuration.</p>
    </body>
    </html>
    """)

urlpatterns = [
    path('', test_view, name='test'),
]

if __name__ == '__main__':
    import django
    django.setup()
    execute_from_command_line(['minimal_server.py', 'runserver', '9001'])
