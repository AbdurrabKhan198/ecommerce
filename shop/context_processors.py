from django.conf import settings
from .models import Category, SubCategory, Wishlist
from cart.models import Cart


def categories_context(request):
    """Add categories and subcategories to template context"""
    categories = Category.objects.filter(is_active=True).order_by('sort_order', 'name')
    
    # Get subcategories grouped by category for navbar dropdown
    subcategories_by_category = {}
    for category in categories:
        subcategories = SubCategory.objects.filter(
            category=category, 
            is_active=True
        ).order_by('sort_order', 'name')
        if subcategories.exists():
            subcategories_by_category[category] = subcategories
    
    return {
        'categories': categories,
        'subcategories_by_category': subcategories_by_category
    }


def cart_context(request):
    """Add cart information to template context"""
    cart_items_count = 0
    cart_total = 0
    
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            cart_items_count = cart.total_items
            cart_total = cart.total_amount
        except Cart.DoesNotExist:
            pass
    
    return {
        'cart_items_count': cart_items_count,
        'cart_total': cart_total,
        'free_shipping_threshold': settings.FREE_SHIPPING_THRESHOLD,
        'currency_symbol': settings.CURRENCY_SYMBOL,
    }


def wishlist_context(request):
    """Add wishlist information to template context"""
    wishlist_count = 0
    
    if request.user.is_authenticated:
        try:
            wishlist_count = Wishlist.objects.filter(user=request.user).count()
        except:
            pass
    
    return {
        'wishlist_count': wishlist_count,
    }


def site_settings(request):
    """Add site-wide settings to template context"""
    return {
        'site_name': 'King Dupatta House',
        'support_phone': '+91 7860247786',
        'support_email': 'Kingdupattahouse@gmail.com',
        'support_whatsapp': '+91 7499099900',
        'store_address': 'Akbari Gate, Near Nakhas, Victoria Street, Nakhas-226003, Lucknow, Uttar Pradesh',
        'store_city': 'Lucknow',
        'store_state': 'Uttar Pradesh',
        'store_pincode': '226003',
        'established_year': '2013',
        'years_in_business': '10+',
        'business_rating': '4.0',
        'business_reviews': '14+',
    }
