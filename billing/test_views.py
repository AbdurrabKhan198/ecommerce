from django.shortcuts import render
from django.http import HttpResponse

def test_billing(request):
    """Simple test view to check if billing URLs work"""
    return HttpResponse("Billing system is working!")

def test_template(request):
    """Test if billing templates can be loaded"""
    try:
        return render(request, 'billing/login.html')
    except Exception as e:
        return HttpResponse(f"Template error: {str(e)}")
