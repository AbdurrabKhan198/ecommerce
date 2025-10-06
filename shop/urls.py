from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    # Homepage
    path('', views.homepage, name='homepage'),
    
    # Shop pages
    path('shop/', views.shop, name='shop'),
    path('shop/<slug:category_slug>/', views.category_view, name='category'),
    path('shop/<slug:category_slug>/<slug:subcategory_slug>/', views.subcategory_view, name='subcategory'),
    
    # Product pages
    path('product/<slug:product_slug>/', views.product_detail, name='product_detail'),
    
    # Search
    path('search/', views.search, name='search'),
    
    # About and Contact
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    
    # AJAX endpoints
    path('ajax/add-to-wishlist/', views.add_to_wishlist, name='add_to_wishlist'),
    path('ajax/remove-from-wishlist/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('ajax/product-quick-view/', views.product_quick_view, name='product_quick_view'),
]
