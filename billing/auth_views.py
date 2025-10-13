from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .decorators import superuser_required

def billing_login(request):
    """Standalone billing system login"""
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('billing:advanced_dashboard')
        else:
            # Show access denied for non-superusers
            return render(request, 'billing/access_denied.html', {
                'message': 'Access Denied - Superuser Required',
                'description': 'This billing system is restricted to superusers only. Please contact your administrator for access.'
            })
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if email and password:
            user = authenticate(request, username=email, password=password)
            if user:
                if user.is_superuser:
                    login(request, user)
                    messages.success(request, 'Welcome to the Billing System!')
                    return redirect('billing:advanced_dashboard')
                else:
                    messages.error(request, 'Access denied. This billing system is restricted to superusers only.')
            else:
                messages.error(request, 'Invalid email/username or password.')
        else:
            messages.error(request, 'Please fill in all required fields.')
    
    return render(request, 'billing/login.html')

@login_required
@superuser_required
def billing_logout(request):
    """Billing system logout"""
    logout(request)
    messages.success(request, 'You have been logged out of the billing system.')
    return redirect('billing:login')
