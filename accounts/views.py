from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.conf import settings
from .models import User, Address
from .forms import (
    UserRegistrationForm, UserLoginForm, UserProfileForm, 
    AddressForm, PasswordChangeForm
)
from checkout.models import Order
from shop.models import Wishlist, RecentlyViewed


def register_view(request):
    """User registration"""
    if request.user.is_authenticated:
        return redirect('shop:homepage')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully! Welcome to our store.')
            return redirect('shop:homepage')
    else:
        form = UserRegistrationForm()
    
    context = {
        'form': form,
        'page_title': 'Create Account - Join Our Community',
    }
    return render(request, 'accounts/register.html', context)


def login_view(request):
    """User login"""
    if request.user.is_authenticated:
        return redirect('shop:homepage')
    
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            
            if user:
                login(request, user)
                next_url = request.GET.get('next', 'shop:homepage')
                messages.success(request, f'Welcome back, {user.get_full_name()}!')
                return redirect(next_url)
            else:
                messages.error(request, 'Invalid email or password.')
    else:
        form = UserLoginForm()
    
    context = {
        'form': form,
        'page_title': 'Login - Access Your Account',
    }
    return render(request, 'accounts/login.html', context)


def logout_view(request):
    """User logout"""
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('shop:homepage')


@login_required
def profile(request):
    """User profile view"""
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    context = {
        'form': form,
        'page_title': 'My Profile - Account Information',
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def order_history(request):
    """User order history"""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    paginator = Paginator(orders, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'orders': page_obj.object_list,
        'page_title': 'Order History - My Orders',
    }
    return render(request, 'accounts/order_history.html', context)


@login_required
def order_detail(request, order_number):
    """Order detail view"""
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    
    context = {
        'order': order,
        'page_title': f'Order Details - {order.order_number}',
    }
    return render(request, 'accounts/order_detail.html', context)


@login_required
def wishlist(request):
    """User wishlist"""
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product')
    
    paginator = Paginator(wishlist_items, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'wishlist_items': page_obj.object_list,
        'page_title': 'My Wishlist - Saved Items',
    }
    return render(request, 'accounts/wishlist.html', context)


@login_required
def address_book(request):
    """User address book"""
    addresses = Address.objects.filter(user=request.user).order_by('-is_default', '-created_at')
    
    context = {
        'addresses': addresses,
        'page_title': 'Address Book - Manage Addresses',
    }
    return render(request, 'accounts/address_book.html', context)


@login_required
def add_address(request):
    """Add new address - redirect to checkout"""
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            messages.success(request, 'Address added successfully!')
            return redirect('checkout:checkout')
    else:
        form = AddressForm()
    
    # Redirect to checkout page for address management
    return redirect('checkout:checkout')


@login_required
def edit_address(request, address_id):
    """Edit address - redirect to checkout"""
    address = get_object_or_404(Address, id=address_id, user=request.user)
    
    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            messages.success(request, 'Address updated successfully!')
            return redirect('checkout:checkout')
    
    # Redirect to checkout page for address management
    return redirect('checkout:checkout')


@login_required
def delete_address(request, address_id):
    """Delete address - redirect to checkout"""
    address = get_object_or_404(Address, id=address_id, user=request.user)
    
    if request.method == 'POST':
        address.delete()
        messages.success(request, 'Address deleted successfully!')
        return redirect('checkout:checkout')
    
    # Redirect to checkout page for address management
    return redirect('checkout:checkout')


@login_required
def account_settings(request):
    """Account settings"""
    recently_viewed = RecentlyViewed.objects.filter(
        user=request.user
    ).select_related('product').order_by('-viewed_at')[:10]
    
    context = {
        'recently_viewed': recently_viewed,
        'page_title': 'Account Settings - Preferences',
    }
    return render(request, 'accounts/settings.html', context)


@login_required
def change_password(request):
    """Change password"""
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Password changed successfully!')
            return redirect('accounts:profile')
    else:
        form = PasswordChangeForm(request.user)
    
    context = {
        'form': form,
        'page_title': 'Change Password',
    }
    return render(request, 'accounts/change_password.html', context)


def forgot_password(request):
    """Forgot password"""
    # Implementation for password reset
    context = {
        'page_title': 'Forgot Password - Reset Your Password',
    }
    return render(request, 'accounts/forgot_password.html', context)


def reset_password(request, token):
    """Reset password with token"""
    # Implementation for password reset with token
    context = {
        'token': token,
        'page_title': 'Reset Password',
    }
    return render(request, 'accounts/reset_password.html', context)
