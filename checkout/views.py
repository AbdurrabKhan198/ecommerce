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


def checkout(request):
    """Main checkout page"""
    # For demo purposes, show sample checkout
    context = {
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
