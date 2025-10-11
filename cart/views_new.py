from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings
import json

from .models import Cart, CartItem
from shop.models import Product, ProductVariant, PromoCode, DeliveryOption


def get_cart_count(request):
    """Get cart count for both authenticated and anonymous users"""
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            return cart.total_items
        except Cart.DoesNotExist:
            return 0
    else:
        # For anonymous users, count session cart items
        cart = request.session.get('cart', {})
        return sum(item['quantity'] for item in cart.values())


def cart_detail(request):
    """Cart detail view - works for both authenticated and anonymous users"""
    cart_items = []
    cart_total = 0
    cart_items_count = 0
    
    if request.user.is_authenticated:
        # For logged-in users, use database cart
        try:
            cart = Cart.objects.get(user=request.user)
            cart_items = cart.items.all().select_related('product', 'variant').prefetch_related('product__images')
            cart_total = cart.total_amount
            cart_items_count = cart.total_items
        except Cart.DoesNotExist:
            cart = None
    else:
        # For anonymous users, use session cart
        session_cart = request.session.get('cart', {})
        cart_items = []
        cart_total = 0
        
        for product_id, item_data in session_cart.items():
            try:
                product = Product.objects.get(id=product_id, is_active=True)
                quantity = item_data['quantity']
                price = item_data['price']
                
                cart_items.append({
                    'product': product,
                    'quantity': quantity,
                    'price': price,
                    'total': quantity * price
                })
                cart_total += quantity * price
                cart_items_count += quantity
            except Product.DoesNotExist:
                continue
    
    # Get active promo codes and delivery options
    promo_codes = PromoCode.objects.filter(is_active=True)
    delivery_options = DeliveryOption.objects.filter(is_active=True)
    
    context = {
        'cart_items': cart_items,
        'cart_total': cart_total,
        'cart_items_count': cart_items_count,
        'promo_codes': promo_codes,
        'delivery_options': delivery_options,
        'page_title': 'Shopping Cart - Review Your Items',
        'meta_description': 'Review your items and proceed to checkout',
    }
    return render(request, 'cart/cart_detail.html', context)


@require_POST
def add_to_cart(request):
    """Add product to cart - works for both authenticated and anonymous users"""
    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')
        quantity = int(data.get('quantity', 1))
        
        product = get_object_or_404(Product, id=product_id, is_active=True)
        
        if request.user.is_authenticated:
            # For logged-in users, use database cart
            cart, created = Cart.objects.get_or_create(user=request.user)
            cart_item, item_created = CartItem.objects.get_or_create(
                cart=cart,
                product=product,
                defaults={'quantity': quantity}
            )
            
            if not item_created:
                cart_item.quantity += quantity
                cart_item.save()
        else:
            # For anonymous users, use session cart
            cart = request.session.get('cart', {})
            product_key = str(product_id)
            
            if product_key in cart:
                cart[product_key]['quantity'] += quantity
            else:
                cart[product_key] = {
                    'product_id': product_id,
                    'quantity': quantity,
                    'price': float(product.price)
                }
            
            request.session['cart'] = cart
            request.session.modified = True
        
        return JsonResponse({
            'success': True,
            'message': f'{product.name} added to cart!',
            'cart_count': get_cart_count(request)
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })


@require_POST
def update_cart(request):
    """Update cart item quantities"""
    if request.user.is_authenticated:
        # For logged-in users
        for key, value in request.POST.items():
            if key.startswith('quantity_'):
                item_id = key.split('_')[1]
                quantity = int(value)
                
                if quantity > 0:
                    try:
                        cart_item = CartItem.objects.get(id=item_id, cart__user=request.user)
                        cart_item.quantity = quantity
                        cart_item.save()
                    except CartItem.DoesNotExist:
                        pass
                else:
                    try:
                        cart_item = CartItem.objects.get(id=item_id, cart__user=request.user)
                        cart_item.delete()
                    except CartItem.DoesNotExist:
                        pass
    else:
        # For anonymous users
        cart = request.session.get('cart', {})
        for key, value in request.POST.items():
            if key.startswith('quantity_'):
                product_id = key.split('_')[1]
                quantity = int(value)
                
                if quantity > 0:
                    if product_id in cart:
                        cart[product_id]['quantity'] = quantity
                else:
                    if product_id in cart:
                        del cart[product_id]
        
        request.session['cart'] = cart
        request.session.modified = True
    
    return redirect('cart:cart_detail')


@require_POST
def remove_from_cart(request):
    """Remove item from cart"""
    if request.user.is_authenticated:
        # For logged-in users
        item_id = request.POST.get('item_id')
        try:
            cart_item = CartItem.objects.get(id=item_id, cart__user=request.user)
            cart_item.delete()
            messages.success(request, 'Item removed from cart!')
        except CartItem.DoesNotExist:
            pass
    else:
        # For anonymous users
        product_id = request.POST.get('product_id')
        cart = request.session.get('cart', {})
        if str(product_id) in cart:
            del cart[str(product_id)]
            request.session['cart'] = cart
            request.session.modified = True
            messages.success(request, 'Item removed from cart!')
    
    return redirect('cart:cart_detail')


def clear_cart(request):
    """Clear entire cart"""
    if request.user.is_authenticated:
        # For logged-in users
        try:
            cart = Cart.objects.get(user=request.user)
            cart.items.all().delete()
            messages.success(request, 'Cart cleared!')
        except Cart.DoesNotExist:
            pass
    else:
        # For anonymous users
        request.session['cart'] = {}
        request.session.modified = True
        messages.success(request, 'Cart cleared!')
    
    return redirect('cart:cart_detail')
