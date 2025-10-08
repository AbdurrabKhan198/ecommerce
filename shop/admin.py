from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Category, SubCategory, Product, ProductImage, 
    ProductVariant, Review, Wishlist, RecentlyViewed, WhatsAppSubscription
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active', 'sort_order', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('is_active', 'sort_order')
    ordering = ('sort_order', 'name')


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'slug', 'is_active', 'sort_order', 'created_at')
    list_filter = ('category', 'is_active', 'created_at')
    search_fields = ('name', 'description', 'category__name')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('is_active', 'sort_order')
    ordering = ('category', 'sort_order', 'name')


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3
    fields = ('image', 'alt_text', 'is_primary', 'sort_order')


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 2
    fields = ('size', 'color', 'color_code', 'stock_quantity', 'additional_price', 'is_active')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'category', 'subcategory', 'selling_price', 'discount_percentage',
        'stock_quantity', 'is_active', 'is_featured', 'is_bestseller', 'created_at'
    )
    list_filter = (
        'category', 'subcategory', 'fabric', 'occasion', 
        'is_active', 'is_featured', 'is_bestseller', 'created_at'
    )
    search_fields = ('name', 'description', 'short_description')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('is_active', 'is_featured', 'is_bestseller', 'selling_price', 'stock_quantity')
    ordering = ('-created_at',)
    inlines = [ProductImageInline, ProductVariantInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'category', 'subcategory')
        }),
        ('Product Details', {
            'fields': ('description', 'short_description', 'fabric', 'occasion', 'care_instructions')
        }),
        ('Pricing & Inventory', {
            'fields': ('mrp', 'selling_price', 'stock_quantity')
        }),
        ('Status', {
            'fields': ('is_active', 'is_featured', 'is_bestseller')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        })
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('category', 'subcategory')
    
    def discount_percentage(self, obj):
        if obj.mrp > obj.selling_price:
            discount = ((obj.mrp - obj.selling_price) / obj.mrp) * 100
            return f"{discount:.0f}%"
        return "-"
    discount_percentage.short_description = "Discount"


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'alt_text', 'is_primary', 'sort_order')
    list_filter = ('is_primary', 'product__category')
    search_fields = ('product__name', 'alt_text')
    list_editable = ('is_primary', 'sort_order')


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('product', 'size', 'color', 'stock_quantity', 'additional_price', 'is_active')
    list_filter = ('size', 'color', 'is_active', 'product__category')
    search_fields = ('product__name', 'color')
    list_editable = ('stock_quantity', 'additional_price', 'is_active')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'title', 'is_approved', 'is_verified_purchase', 'created_at')
    list_filter = ('rating', 'is_approved', 'is_verified_purchase', 'created_at')
    search_fields = ('product__name', 'user__email', 'title', 'comment')
    list_editable = ('is_approved', 'is_verified_purchase')
    ordering = ('-created_at',)
    list_per_page = 25
    
    fieldsets = (
        ('Review Details', {
            'fields': ('product', 'user', 'rating', 'title', 'comment')
        }),
        ('Status', {
            'fields': ('is_approved', 'is_verified_purchase')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('product', 'user')
    
    actions = ['approve_reviews', 'disapprove_reviews']
    
    def approve_reviews(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f'{updated} reviews approved.')
    approve_reviews.short_description = "Approve selected reviews"
    
    def disapprove_reviews(self, request, queryset):
        updated = queryset.update(is_approved=False)
        self.message_user(request, f'{updated} reviews disapproved.')
    disapprove_reviews.short_description = "Disapprove selected reviews"


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'created_at')


@admin.register(WhatsAppSubscription)
class WhatsAppSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'name', 'is_active', 'source', 'subscribed_at')
    list_filter = ('is_active', 'source', 'subscribed_at')
    search_fields = ('phone_number', 'name')
    list_editable = ('is_active',)
    ordering = ('-subscribed_at',)
    list_per_page = 25
    
    fieldsets = (
        ('Subscription Details', {
            'fields': ('phone_number', 'name', 'is_active', 'source')
        }),
        ('Timestamps', {
            'fields': ('subscribed_at', 'unsubscribed_at'),
            'classes': ('collapse',)
        })
    )
    
    readonly_fields = ('subscribed_at',)
    
    actions = ['activate_subscriptions', 'deactivate_subscriptions']
    
    def activate_subscriptions(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} WhatsApp subscriptions activated.')
    activate_subscriptions.short_description = "Activate selected subscriptions"
    
    def deactivate_subscriptions(self, request, queryset):
        from django.utils import timezone
        updated = queryset.update(is_active=False, unsubscribed_at=timezone.now())
        self.message_user(request, f'{updated} WhatsApp subscriptions deactivated.')
    deactivate_subscriptions.short_description = "Deactivate selected subscriptions"


@admin.register(RecentlyViewed)
class RecentlyViewedAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'viewed_at')
    list_filter = ('viewed_at', 'product__category')
    search_fields = ('user__email', 'product__name')
    ordering = ('-viewed_at',)
