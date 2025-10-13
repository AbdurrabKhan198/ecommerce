from django.urls import path
from . import advanced_views
from . import auth_views
from . import test_views

app_name = 'billing'

urlpatterns = [
    # Test routes
    path('test/', test_views.test_billing, name='test'),
    path('test-template/', test_views.test_template, name='test_template'),
    
    # Authentication
    path('login/', auth_views.billing_login, name='login'),
    path('logout/', auth_views.billing_logout, name='logout'),
    # Advanced Dashboard
    path('', advanced_views.advanced_dashboard, name='advanced_dashboard'),
    
    # Customer Management
    path('customers/', advanced_views.advanced_customer_list, name='advanced_customer_list'),
    path('customers/<uuid:customer_id>/', advanced_views.advanced_customer_detail, name='advanced_customer_detail'),
    
    # Invoice Management
    path('invoices/', advanced_views.advanced_invoice_list, name='advanced_invoice_list'),
    path('invoices/create/', advanced_views.advanced_invoice_create, name='advanced_invoice_create'),
    path('invoices/<uuid:invoice_id>/', advanced_views.advanced_invoice_detail, name='advanced_invoice_detail'),
    path('invoices/<uuid:invoice_id>/print/', advanced_views.advanced_invoice_print, name='advanced_invoice_print'),
    path('invoices/<uuid:invoice_id>/mark-paid/', advanced_views.mark_invoice_paid, name='mark_invoice_paid'),
    
    # Analytics
    path('analytics/', advanced_views.advanced_analytics, name='advanced_analytics'),
    
    # AJAX Endpoints
    path('api/calculate-totals/', advanced_views.ajax_calculate_totals, name='ajax_calculate_totals'),
]
