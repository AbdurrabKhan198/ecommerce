from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings
import json

from .models import Cart, CartItem
from shop.models import Product, ProductVariant


def cart_detail(request):
    """Cart detail view"""
    # For demo purposes, show a sample cart
    context = {
        'page_title': 'Shopping Cart - Review Your Items',
        'meta_description': 'Review your items and proceed to checkout',
        'cart_items_count': 4,
        'cart_total': 1497,
    }
    return render(request, 'cart/cart_detail.html', context)


@login_required
@require_POST
def add_to_cart(request):
    """Add product to cart"""
    product_id = request.POST.get('product_id')
    variant_id = request.POST.get('variant_id')
    quantity = int(request.POST.get('quantity', 1))
    
    product = get_object_or_404(Product, id=product_id, is_active=True)
    variant = None
    
    if variant_id:
        variant = get_object_or_404(ProductVariant, id=variant_id, product=product)
    
    # Get or create cart
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Get or create cart item
    cart_item, item_created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        variant=variant,
        defaults={'quantity': quantity}
    )
    
    if not item_created:
        cart_item.quantity += quantity
        cart_item.save()
    
    messages.success(request, f'{product.name} added to cart!')
    return redirect('cart:cart_detail')


@login_required
@require_POST
def update_cart(request):
    """Update cart item quantities"""
    for key, value in request.POST.items():
        if key.startswith('quantity_'):
            item_id = key.split('_')[1]
            quantity = int(value)
            
            try:
                cart_item = CartItem.objects.get(
                    id=item_id,
                    cart__user=request.user
                )
                if quantity > 0:
                    cart_item.quantity = quantity
                    cart_item.save()
                else:
                    cart_item.delete()
            except CartItem.DoesNotExist:
                continue
    
    messages.success(request, 'Cart updated successfully!')
    return redirect('cart:cart_detail')


@login_required
def remove_from_cart(request, item_id):
    """Remove item from cart"""
    cart_item = get_object_or_404(
        CartItem,
        id=item_id,
        cart__user=request.user
    )
    
    product_name = cart_item.product.name
    cart_item.delete()
    
    messages.success(request, f'{product_name} removed from cart!')
    return redirect('cart:cart_detail')


@login_required
def clear_cart(request):
    """Clear all items from cart"""
    try:
        cart = Cart.objects.get(user=request.user)
        cart.items.all().delete()
        messages.success(request, 'Cart cleared successfully!')
    except Cart.DoesNotExist:
        pass
    
    return redirect('cart:cart_detail')


# AJAX Views
@login_required
@require_POST
def ajax_add_to_cart(request):
    """Add to cart via AJAX"""
    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')
        variant_id = data.get('variant_id')
        quantity = int(data.get('quantity', 1))
        
        product = get_object_or_404(Product, id=product_id, is_active=True)
        variant = None
        
        if variant_id:
            variant = get_object_or_404(ProductVariant, id=variant_id, product=product)
        
        # Check stock
        if variant:
            if variant.stock_quantity < quantity:
                return JsonResponse({
                    'success': False,
                    'error': 'Insufficient stock'
                })
        else:
            if product.stock_quantity < quantity:
                return JsonResponse({
                    'success': False,
                    'error': 'Insufficient stock'
                })
        
        # Get or create cart
        cart, created = Cart.objects.get_or_create(user=request.user)
        
        # Get or create cart item
        cart_item, item_created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            variant=variant,
            defaults={'quantity': quantity}
        )
        
        if not item_created:
            cart_item.quantity += quantity
            cart_item.save()
        
        return JsonResponse({
            'success': True,
            'message': f'{product.name} added to cart!',
            'cart_items_count': cart.total_items,
            'cart_total': float(cart.total_amount)
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })


@login_required
@require_POST
def ajax_update_cart(request):
    """Update cart via AJAX"""
    try:
        data = json.loads(request.body)
        item_id = data.get('item_id')
        quantity = int(data.get('quantity'))
        
        cart_item = get_object_or_404(
            CartItem,
            id=item_id,
            cart__user=request.user
        )
        
        if quantity > 0:
            # Check stock
            if cart_item.variant:
                if cart_item.variant.stock_quantity < quantity:
                    return JsonResponse({
                        'success': False,
                        'error': 'Insufficient stock'
                    })
            else:
                if cart_item.product.stock_quantity < quantity:
                    return JsonResponse({
                        'success': False,
                        'error': 'Insufficient stock'
                    })
            
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()
        
        cart = cart_item.cart
        
        return JsonResponse({
            'success': True,
            'cart_items_count': cart.total_items,
            'cart_total': float(cart.total_amount),
            'item_total': float(cart_item.get_total_price()) if quantity > 0 else 0
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })


@login_required
@require_POST
def ajax_remove_from_cart(request):
    """Remove from cart via AJAX"""
    try:
        data = json.loads(request.body)
        item_id = data.get('item_id')
        
        cart_item = get_object_or_404(
            CartItem,
            id=item_id,
            cart__user=request.user
        )
        
        cart = cart_item.cart
        cart_item.delete()
        
        return JsonResponse({
            'success': True,
            'message': 'Item removed from cart',
            'cart_items_count': cart.total_items,
            'cart_total': float(cart.total_amount)
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })


@login_required
def ajax_get_cart_count(request):
    """Get cart items count via AJAX"""
    try:
        cart = Cart.objects.get(user=request.user)
        return JsonResponse({
            'success': True,
            'cart_items_count': cart.total_items,
            'cart_total': float(cart.total_amount)
        })
    except Cart.DoesNotExist:
        return JsonResponse({
            'success': True,
            'cart_items_count': 0,
            'cart_total': 0
        })
