from django.contrib import admin
from django.db.models import Count, Sum
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Product, Category, SubCategory, ProductImage


class ProductAdminDashboard:
    """Enhanced admin dashboard for product management"""
    
    @staticmethod
    def get_product_stats():
        """Get product statistics for admin dashboard"""
        total_products = Product.objects.count()
        active_products = Product.objects.filter(is_active=True).count()
        featured_products = Product.objects.filter(is_featured=True).count()
        out_of_stock = Product.objects.filter(stock_quantity=0).count()
        
        return {
            'total_products': total_products,
            'active_products': active_products,
            'featured_products': featured_products,
            'out_of_stock': out_of_stock,
        }
    
    @staticmethod
    def get_category_stats():
        """Get category statistics"""
        categories = Category.objects.annotate(
            product_count=Count('products')
        ).values('name', 'product_count')
        
        return list(categories)
    
    @staticmethod
    def get_low_stock_products():
        """Get products with low stock"""
        return Product.objects.filter(
            stock_quantity__lte=10,
            is_active=True
        ).order_by('stock_quantity')
    
    @staticmethod
    def get_recent_products():
        """Get recently added products"""
        return Product.objects.order_by('-created_at')[:5]


# Add custom admin site configuration
admin.site.site_header = "King Dupatta House - Admin Panel"
admin.site.site_title = "King Dupatta House Admin"
admin.site.index_title = "Welcome to King Dupatta House Admin Panel"
