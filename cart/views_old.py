from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings
import json

from .models import Cart, CartItem
from shop.models import Product, ProductVariant, PromoCode, DeliveryOption


def cart_detail(request):
    """Cart detail view"""
    cart = None
    cart_items = []
    cart_total = 0
    cart_items_count = 0
    
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            cart_items = cart.items.all().select_related('product', 'variant').prefetch_related('product__images')
            cart_total = cart.total_amount
            cart_items_count = cart.total_items
        except Cart.DoesNotExist:
            cart = None
    
    # Get active promo codes and delivery options
    promo_codes = PromoCode.objects.filter(is_active=True)
    delivery_options = DeliveryOption.objects.filter(is_active=True)
    
    context = {
        'cart': cart,
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
            # Check stock (with more flexible validation)
            if cart_item.variant:
                # If variant has stock, check it; otherwise allow up to 10
                max_quantity = cart_item.variant.stock_quantity if cart_item.variant.stock_quantity > 0 else 10
                if max_quantity < quantity:
                    return JsonResponse({
                        'success': False,
                        'error': f'Maximum {max_quantity} items allowed'
                    })
            else:
                # If product has stock, check it; otherwise allow up to 10
                max_quantity = cart_item.product.stock_quantity if cart_item.product.stock_quantity > 0 else 10
                if max_quantity < quantity:
                    return JsonResponse({
                        'success': False,
                        'error': f'Maximum {max_quantity} items allowed'
                    })
            
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()
        
        cart = cart_item.cart
        
        return JsonResponse({
            'success': True,
            'message': f'Quantity updated to {quantity}' if quantity > 0 else 'Item removed from cart',
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


@login_required
@require_POST
def validate_promo_code(request):
    """Validate promo code via AJAX"""
    try:
        data = json.loads(request.body)
        code = data.get('code', '').strip().upper()
        
        if not code:
            return JsonResponse({
                'success': False,
                'error': 'Please enter a promo code'
            })
        
        try:
            promo = PromoCode.objects.get(code=code)
        except PromoCode.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Invalid promo code'
            })
        
        if not promo.is_valid:
            return JsonResponse({
                'success': False,
                'error': 'Promo code is not valid or has expired'
            })
        
        # Get cart total for validation
        cart = Cart.objects.get(user=request.user)
        cart_total = float(cart.total_amount)
        
        if cart_total < float(promo.min_order_amount):
            return JsonResponse({
                'success': False,
                'error': f'Minimum order amount of ₹{promo.min_order_amount} required'
            })
        
        # Calculate discount
        discount_amount = promo.calculate_discount(cart_total)
        
        return JsonResponse({
            'success': True,
            'discount_amount': float(discount_amount),
            'description': promo.description,
            'discount_type': promo.discount_type,
            'discount_value': float(promo.discount_value)
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })


@login_required
@require_POST
def get_delivery_options(request):
    """Get delivery options via AJAX"""
    try:
        delivery_options = DeliveryOption.objects.filter(is_active=True)
        
        options = []
        for option in delivery_options:
            options.append({
                'id': option.id,
                'name': option.name,
                'description': option.description,
                'price': float(option.price),
                'estimated_days': option.estimated_days
            })
        
        return JsonResponse({
            'success': True,
            'options': options
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })
