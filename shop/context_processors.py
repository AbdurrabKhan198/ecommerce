from django.conf import settings
from .models import Category
from cart.models import Cart


def categories_context(request):
    """Add categories to template context"""
    categories = Category.objects.filter(is_active=True).order_by('sort_order')
    return {'categories': categories}


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


def site_settings(request):
    """Add site-wide settings to template context"""
    return {
        'site_name': 'Women\'s Wear Store',
        'support_phone': '1800-XXX-XXXX',
        'support_email': 'support@yourstore.com',
        'support_whatsapp': '+91-XXXXX-XXXXX',
    }
