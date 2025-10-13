from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from functools import wraps

def superuser_required(view_func):
    """
    Decorator that restricts access to superusers only.
    Shows an access denied page for non-superusers.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            # Redirect to login if not authenticated
            from django.contrib.auth.views import redirect_to_login
            return redirect_to_login(request.get_full_path())
        
        if not request.user.is_superuser:
            # Show access denied page for non-superusers
            return render(request, 'billing/access_denied.html', {
                'message': 'Access Denied - Superuser Required',
                'description': 'This billing module is restricted to superusers only. Please contact your administrator for access.'
            })
        
        return view_func(request, *args, **kwargs)
    return wrapper

def superuser_required_with_login(view_func):
    """
    Combined decorator that requires both login and superuser status.
    """
    @login_required
    @superuser_required
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        return view_func(request, *args, **kwargs)
    return wrapper
