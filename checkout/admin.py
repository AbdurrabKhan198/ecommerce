from django.contrib import admin
from .models import Order, OrderItem, Coupon


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product_name', 'product_price', 'total_price')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'order_number', 'user', 'status', 'payment_status', 
        'total_amount', 'created_at'
    )
    list_filter = ('status', 'payment_status', 'payment_method', 'created_at')
    search_fields = ('order_number', 'user__email', 'user__first_name', 'user__last_name')
    readonly_fields = ('order_number', 'created_at', 'updated_at')
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('Order Information', {
            'fields': ('order_number', 'user', 'status', 'payment_status', 'payment_method')
        }),
        ('Shipping Address', {
            'fields': (
                'shipping_full_name', 'shipping_phone', 'shipping_address_line_1',
                'shipping_address_line_2', 'shipping_city', 'shipping_state', 'shipping_pin_code'
            )
        }),
        ('Billing Address', {
            'fields': (
                'billing_same_as_shipping', 'billing_full_name', 'billing_phone',
                'billing_address_line_1', 'billing_address_line_2',
                'billing_city', 'billing_state', 'billing_pin_code'
            ),
            'classes': ('collapse',)
        }),
        ('Order Totals', {
            'fields': ('subtotal', 'shipping_cost', 'discount_amount', 'total_amount')
        }),
        ('Tracking', {
            'fields': ('tracking_number', 'shipped_at', 'delivered_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = (
        'code', 'discount_type', 'discount_value', 'minimum_order_amount',
        'used_count', 'usage_limit', 'is_active', 'valid_from', 'valid_to'
    )
    list_filter = ('discount_type', 'is_active', 'valid_from', 'valid_to')
    search_fields = ('code', 'description')
    readonly_fields = ('used_count',)
