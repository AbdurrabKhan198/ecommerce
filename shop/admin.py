from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Category, SubCategory, Product, ProductImage, 
    ProductVariant, Review, Wishlist, RecentlyViewed
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
    list_editable = ('is_approved',)
    ordering = ('-created_at',)
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('product', 'user')


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'created_at')
    list_filter = ('created_at', 'product__category')
    search_fields = ('user__email', 'product__name')
    ordering = ('-created_at',)


@admin.register(RecentlyViewed)
class RecentlyViewedAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'viewed_at')
    list_filter = ('viewed_at', 'product__category')
    search_fields = ('user__email', 'product__name')
    ordering = ('-viewed_at',)
