from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.conf import settings
import json

from .models import Order, OrderItem, Coupon
from cart.models import Cart
from accounts.models import Address
from .forms import ShippingAddressForm, PaymentForm


@login_required
def checkout(request):
    """Main checkout page with dynamic data"""
    # Get user's cart
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = cart.items.all().select_related('product', 'variant').prefetch_related('product__images')
    except Cart.DoesNotExist:
        cart = None
        cart_items = []
    
    # Get user's saved addresses
    addresses = Address.objects.filter(user=request.user).order_by('-is_default', '-created_at')
    
    # Get delivery options from shop models
    from shop.models import DeliveryOption
    delivery_options = DeliveryOption.objects.filter(is_active=True).order_by('sort_order')
    
    # Get available promo codes
    from shop.models import PromoCode
    promo_codes = PromoCode.objects.filter(is_active=True).order_by('-discount_value')
    
    # Calculate totals
    cart_total = cart.total_amount if cart else 0
    cart_items_count = cart.total_items if cart else 0
    
    # Check for applied coupon in session
    applied_coupon = request.session.get('applied_coupon', None)
    discount_amount = 0
    if applied_coupon:
        discount_amount = applied_coupon.get('discount', 0)
    
    # Calculate final total
    final_total = cart_total - discount_amount
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'cart_total': cart_total,
        'cart_items_count': cart_items_count,
        'addresses': addresses,
        'delivery_options': delivery_options,
        'promo_codes': promo_codes,
        'applied_coupon': applied_coupon,
        'discount_amount': discount_amount,
        'final_total': final_total,
        'page_title': 'Checkout - Complete Your Order',
        'meta_description': 'Complete your order safely and securely',
    }
    return render(request, 'checkout/checkout.html', context)


@login_required
def shipping_info(request):
    """Shipping information step"""
    if request.method == 'POST':
        form = ShippingAddressForm(request.POST)
        if form.is_valid():
            # Store shipping info in session
            request.session['shipping_info'] = form.cleaned_data
            return redirect('checkout:payment_info')
    else:
        # Pre-fill with default address if available
        default_address = Address.objects.filter(user=request.user, is_default=True).first()
        initial_data = {}
        if default_address:
            initial_data = {
                'full_name': default_address.full_name,
                'phone': default_address.phone_number,
                'address_line_1': default_address.address_line_1,
                'address_line_2': default_address.address_line_2,
                'city': default_address.city,
                'state': default_address.state,
                'pin_code': default_address.pin_code,
            }
        form = ShippingAddressForm(initial=initial_data)
    
    context = {
        'form': form,
        'page_title': 'Shipping Information - Checkout',
    }
    return render(request, 'checkout/shipping_info.html', context)


@login_required
def payment_info(request):
    """Payment information step"""
    # Check if shipping info is in session
    if 'shipping_info' not in request.session:
        return redirect('checkout:shipping_info')
    
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        messages.error(request, 'Your cart is empty.')
        return redirect('cart:cart_detail')
    
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            # Process order
            order = create_order(request, cart, request.session['shipping_info'], form.cleaned_data)
            
            # Clear cart and session
            cart.items.all().delete()
            del request.session['shipping_info']
            
            return redirect('checkout:order_confirmation', order_number=order.order_number)
    else:
        form = PaymentForm()
    
    context = {
        'form': form,
        'cart': cart,
        'shipping_info': request.session['shipping_info'],
        'page_title': 'Payment Information - Checkout',
    }
    return render(request, 'checkout/payment_info.html', context)


def create_order(request, cart, shipping_info, payment_info):
    """Create order from cart"""
    order = Order.objects.create(
        user=request.user,
        # Shipping address
        shipping_full_name=shipping_info['full_name'],
        shipping_phone=shipping_info['phone'],
        shipping_address_line_1=shipping_info['address_line_1'],
        shipping_address_line_2=shipping_info.get('address_line_2', ''),
        shipping_city=shipping_info['city'],
        shipping_state=shipping_info['state'],
        shipping_pin_code=shipping_info['pin_code'],
        # Payment info
        payment_method=payment_info['payment_method'],
        # Totals
        subtotal=cart.total_amount,
        shipping_cost=0 if cart.is_eligible_for_free_shipping else settings.EXPRESS_SHIPPING_COST,
        total_amount=cart.total_amount + (0 if cart.is_eligible_for_free_shipping else settings.EXPRESS_SHIPPING_COST),
    )
    
    # Create order items
    for cart_item in cart.items.all():
        OrderItem.objects.create(
            order=order,
            product=cart_item.product,
            variant=cart_item.variant,
            product_name=cart_item.product.name,
            product_price=cart_item.product.selling_price,
            variant_info=f"{cart_item.variant.size} - {cart_item.variant.color}" if cart_item.variant else "",
            quantity=cart_item.quantity,
            total_price=cart_item.get_total_price(),
        )
    
    return order


@login_required
def order_confirmation(request, order_number):
    """Order confirmation page"""
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    
    context = {
        'order': order,
        'page_title': f'Order Confirmation - {order.order_number}',
    }
    return render(request, 'checkout/order_confirmation.html', context)


def track_order(request, order_number):
    """Order tracking page"""
    if request.user.is_authenticated:
        order = get_object_or_404(Order, order_number=order_number, user=request.user)
    else:
        order = get_object_or_404(Order, order_number=order_number)
    
    context = {
        'order': order,
        'page_title': f'Track Order - {order.order_number}',
    }
    return render(request, 'checkout/track_order.html', context)


@login_required
def process_payment(request):
    """Process payment (placeholder for payment gateway integration)"""
    # This would integrate with payment gateways like Razorpay, Stripe, etc.
    if request.method == 'POST':
        # Payment processing logic here
        return JsonResponse({'success': True, 'message': 'Payment processed successfully'})
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})


def payment_success(request):
    """Payment success callback"""
    context = {
        'page_title': 'Payment Successful',
    }
    return render(request, 'checkout/payment_success.html', context)


def payment_failed(request):
    """Payment failed callback"""
    context = {
        'page_title': 'Payment Failed',
    }
    return render(request, 'checkout/payment_failed.html', context)


@login_required
@require_POST
def apply_coupon(request):
    """Apply coupon code via AJAX"""
    try:
        data = json.loads(request.body)
        coupon_code = data.get('coupon_code', '').upper()
        
        try:
            # Try PromoCode first (new model)
            from shop.models import PromoCode
            coupon = PromoCode.objects.get(code=coupon_code)
            
            if not coupon.is_valid:
                return JsonResponse({
                    'success': False,
                    'error': 'This coupon is not valid or has expired.'
                })
            
            # Get cart total
            try:
                cart = Cart.objects.get(user=request.user)
                cart_total = cart.total_amount
            except Cart.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'error': 'Your cart is empty.'
                })
            
            # Calculate discount
            discount = coupon.calculate_discount(cart_total)
            
            if discount == 0:
                return JsonResponse({
                    'success': False,
                    'error': f'Minimum order amount is ₹{coupon.min_order_amount}'
                })
            
            # Store in session
            request.session['applied_coupon'] = {
                'code': coupon.code,
                'discount': float(discount),
                'type': coupon.discount_type,
                'value': float(coupon.discount_value)
            }
            
            return JsonResponse({
                'success': True,
                'discount': discount,
                'new_total': cart_total - discount,
                'message': f'Coupon applied! You saved ₹{discount}'
            })
            
        except PromoCode.DoesNotExist:
            # Fallback to old Coupon model
            try:
                coupon = Coupon.objects.get(code=coupon_code)
                
                if not coupon.is_valid:
                    return JsonResponse({
                        'success': False,
                        'error': 'This coupon is not valid or has expired.'
                    })
                
                # Get cart total
                try:
                    cart = Cart.objects.get(user=request.user)
                    cart_total = cart.total_amount
                except Cart.DoesNotExist:
                    return JsonResponse({
                        'success': False,
                        'error': 'Your cart is empty.'
                    })
                
                # Calculate discount
                discount = coupon.calculate_discount(cart_total)
                
                if discount == 0:
                    return JsonResponse({
                        'success': False,
                        'error': f'Minimum order amount is ₹{coupon.minimum_order_amount}'
                    })
                
                # Store in session
                request.session['applied_coupon'] = {
                    'code': coupon.code,
                    'discount': float(discount),
                    'type': coupon.discount_type,
                    'value': float(coupon.discount_value)
                }
                
                return JsonResponse({
                    'success': True,
                    'discount': discount,
                    'new_total': cart_total - discount,
                    'message': f'Coupon applied! You saved ₹{discount}'
                })
                
            except Coupon.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'error': 'Invalid coupon code.'
                })
            
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': 'Something went wrong. Please try again.'
        })


@login_required
@require_POST
def remove_coupon(request):
    """Remove applied coupon via AJAX"""
    try:
        if 'applied_coupon' in request.session:
            del request.session['applied_coupon']
        
        # Get new total
        try:
            cart = Cart.objects.get(user=request.user)
            cart_total = cart.total_amount
        except Cart.DoesNotExist:
            cart_total = 0
        
        return JsonResponse({
            'success': True,
            'new_total': cart_total,
            'message': 'Coupon removed.'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': 'Something went wrong. Please try again.'
        })


@login_required
@require_POST
def place_order(request):
    """Place order via AJAX"""
    try:
        data = json.loads(request.body)
        
        # Get user's cart
        try:
            cart = Cart.objects.get(user=request.user)
            cart_items = cart.items.all()
        except Cart.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Your cart is empty.'
            })
        
        if not cart_items.exists():
            return JsonResponse({
                'success': False,
                'error': 'Your cart is empty.'
            })
        
        # Get selected address
        address_id = data.get('selected_address')
        if address_id:
            try:
                from accounts.models import Address
                address = Address.objects.get(id=address_id, user=request.user)
            except Address.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'error': 'Selected address not found.'
                })
        else:
            return JsonResponse({
                'success': False,
                'error': 'Please select a shipping address.'
            })
        
        # Get applied coupon
        applied_coupon = request.session.get('applied_coupon', None)
        discount_amount = applied_coupon.get('discount', 0) if applied_coupon else 0
        
        # Calculate totals
        subtotal = cart.total_amount
        shipping_cost = 0  # Free shipping for now
        total_amount = subtotal - discount_amount + shipping_cost
        
        # Create order
        order = Order.objects.create(
            user=request.user,
            # Shipping address
            shipping_full_name=f"{data.get('first_name', '')} {data.get('last_name', '')}".strip(),
            shipping_phone=data.get('phone', ''),
            shipping_address_line_1=address.address_line_1,
            shipping_address_line_2=address.address_line_2 or '',
            shipping_city=address.city,
            shipping_state=address.state,
            shipping_pin_code=address.pin_code,
            # Payment info
            payment_method='cod',  # Default to COD for now
            # Totals
            subtotal=subtotal,
            shipping_cost=shipping_cost,
            discount_amount=discount_amount,
            total_amount=total_amount,
        )
        
        # Create order items
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                variant=cart_item.variant,
                product_name=cart_item.product.name,
                product_price=cart_item.product.selling_price,
                variant_info=f"{cart_item.variant.size} - {cart_item.variant.color}" if cart_item.variant else "Default",
                quantity=cart_item.quantity,
                total_price=cart_item.get_total_price(),
            )
        
        # Clear cart
        cart.items.all().delete()
        
        # Clear applied coupon
        if 'applied_coupon' in request.session:
            del request.session['applied_coupon']
        
        return JsonResponse({
            'success': True,
            'order_number': order.order_number,
            'redirect_url': f'/checkout/confirmation/{order.order_number}/',
            'message': 'Order placed successfully!'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Something went wrong: {str(e)}'
        })
