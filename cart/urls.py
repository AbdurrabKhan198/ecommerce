from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    # Cart views
    path('', views.cart_detail, name='cart_detail'),
    path('add/', views.add_to_cart, name='add_to_cart'),
    path('update/', views.update_cart, name='update_cart'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('clear/', views.clear_cart, name='clear_cart'),
    
    # AJAX endpoints
    path('ajax/add/', views.ajax_add_to_cart, name='ajax_add_to_cart'),
    path('ajax/update/', views.ajax_update_cart, name='ajax_update_cart'),
    path('ajax/remove/', views.ajax_remove_from_cart, name='ajax_remove_from_cart'),
    path('ajax/get-count/', views.ajax_get_cart_count, name='ajax_get_cart_count'),
    path('ajax/validate-promo/', views.validate_promo_code, name='validate_promo_code'),
    path('ajax/delivery-options/', views.get_delivery_options, name='get_delivery_options'),
]
