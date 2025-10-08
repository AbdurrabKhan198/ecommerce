from django.urls import path
from . import views

app_name = 'checkout'

urlpatterns = [
    # Checkout flow
    path('', views.checkout, name='checkout'),
    path('shipping/', views.shipping_info, name='shipping_info'),
    path('payment/', views.payment_info, name='payment_info'),
    path('confirmation/', views.order_confirmation, name='order_confirmation'),
    
    # Order tracking
    path('track/<str:order_number>/', views.track_order, name='track_order'),
    
    # Payment processing
    path('process-payment/', views.process_payment, name='process_payment'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('payment-failed/', views.payment_failed, name='payment_failed'),
    
    # Coupons
    path('apply-coupon/', views.apply_coupon, name='apply_coupon'),
    path('ajax/apply-coupon/', views.apply_coupon, name='apply_coupon_ajax'),
    path('ajax/remove-coupon/', views.remove_coupon, name='remove_coupon'),
    
    # Order placement
    path('place-order/', views.place_order, name='place_order'),
]
