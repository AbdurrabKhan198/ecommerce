from django.contrib import admin
from .models import CompanyProfile, Customer, Invoice, InvoiceItem

@admin.register(CompanyProfile)
class CompanyProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'gst_number', 'phone', 'email']
    list_editable = ['gst_number', 'phone', 'email']

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'gst_number', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'email', 'phone']

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['invoice_number', 'customer', 'date', 'status', 'total_amount']
    list_filter = ['status', 'date', 'created_at']
    search_fields = ['invoice_number', 'customer__name']
    readonly_fields = ['invoice_number', 'subtotal', 'tax_amount', 'total_amount', 'created_at', 'updated_at']

@admin.register(InvoiceItem)
class InvoiceItemAdmin(admin.ModelAdmin):
    list_display = ['invoice', 'description', 'quantity', 'unit_price', 'total_price']
    list_filter = ['invoice__status']
    search_fields = ['description', 'invoice__invoice_number']