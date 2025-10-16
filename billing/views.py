from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime, timedelta
from .models import CompanyProfile, Customer, Invoice, InvoiceItem
from .forms import CustomerForm, InvoiceForm, InvoiceItemForm, CompanyProfileForm
from .decorators import superuser_required_with_login

@superuser_required_with_login
def billing_dashboard(request):
    """Billing dashboard"""
    # Get or create company profile
    company, created = CompanyProfile.objects.get_or_create(
        id=1,
        defaults={
            'name': 'King Dupatta House',
            'gst_number': '09ABCDE1234F1Z5',
            'address': 'Akbari Gate, Near Nakkhas, Victoria Street, Nakkhas-226003, Lucknow, Uttar Pradesh',
            'phone': '+91-9876543210',
            'email': 'info@kingdupattahouse.com'
        }
    )
    
    # Get recent invoices
    recent_invoices = Invoice.objects.all()[:5]
    
    # Get stats
    total_invoices = Invoice.objects.count()
    paid_invoices = Invoice.objects.filter(status='paid').count()
    total_amount = sum(invoice.total_amount for invoice in Invoice.objects.filter(status='paid'))
    
    context = {
        'company': company,
        'recent_invoices': recent_invoices,
        'total_invoices': total_invoices,
        'paid_invoices': paid_invoices,
        'total_amount': total_amount,
    }
    return render(request, 'billing/advanced_dashboard.html', context)

@superuser_required_with_login
def customer_list(request):
    """Customer list"""
    customers = Customer.objects.all().order_by('-created_at')
    return render(request, 'billing/advanced_customer_list.html', {'customers': customers})

@superuser_required_with_login
def customer_add(request):
    """Add new customer"""
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Customer added successfully!')
            return redirect('billing:customer_list')
    else:
        form = CustomerForm()
    
    return render(request, 'billing/advanced_customer_list.html', {'form': form})

@superuser_required_with_login
def invoice_list(request):
    """Invoice list"""
    invoices = Invoice.objects.all().order_by('-created_at')
    return render(request, 'billing/advanced_invoice_list.html', {'invoices': invoices})

@superuser_required_with_login
def invoice_create(request):
    """Create new invoice"""
    if request.method == 'POST':
        try:
            # Get form data
            invoice_date = request.POST.get('date')
            notes = request.POST.get('notes', '')
            
            # Get or create a default company customer
            company = CompanyProfile.objects.get(id=1)
            customer, created = Customer.objects.get_or_create(
                name="Company Invoice",
                defaults={
                    'email': company.email,
                    'phone': company.phone,
                    'address': company.address,
                    'gst_number': company.gst_number
                }
            )
            
            # Create invoice
            invoice = Invoice(
                customer=customer,
                company=company,
                date=datetime.strptime(invoice_date, '%Y-%m-%d').date(),
                due_date=datetime.strptime(invoice_date, '%Y-%m-%d').date(),  # Same as invoice date
                notes=notes,
                status='draft'
            )
            invoice.save()
            
            # Handle invoice items
            items_data = request.POST.getlist('items')
            for item_data in items_data:
                if item_data:
                    item_json = json.loads(item_data)
                    from decimal import Decimal
                    InvoiceItem.objects.create(
                        invoice=invoice,
                        description=item_json['description'],
                        quantity=int(item_json['quantity']),
                        unit_price=Decimal(str(item_json['unit_price']))
                    )
            
            messages.success(request, f'Invoice {invoice.invoice_number} created successfully!')
            return redirect('billing:invoice_detail', invoice_id=invoice.id)
            
        except Exception as e:
            messages.error(request, f'Error creating invoice: {str(e)}')
    
    # Create a simple form for date and notes
    class SimpleInvoiceForm:
        def __init__(self):
            self.fields = {
                'date': type('Field', (), {'initial': datetime.now().date()}),
                'notes': type('Field', (), {'initial': ''})
            }
    
    invoice_form = SimpleInvoiceForm()
    return render(request, 'billing/advanced_invoice_create.html', {
        'invoice_form': invoice_form
    })

@superuser_required_with_login
def invoice_detail(request, invoice_id):
    """Invoice detail view"""
    invoice = get_object_or_404(Invoice, id=invoice_id)
    return render(request, 'billing/invoice_detail.html', {'invoice': invoice})

@superuser_required_with_login
def invoice_print(request, invoice_id):
    """Print invoice"""
    invoice = get_object_or_404(Invoice, id=invoice_id)
    return render(request, 'billing/professional_invoice_print.html', {'invoice': invoice})

@superuser_required_with_login
def company_profile(request):
    """Company profile management"""
    company = get_object_or_404(CompanyProfile, id=1)
    
    if request.method == 'POST':
        form = CompanyProfileForm(request.POST, request.FILES, instance=company)
        if form.is_valid():
            form.save()
            messages.success(request, 'Company profile updated successfully!')
            return redirect('billing:company_profile')
    else:
        form = CompanyProfileForm(instance=company)
    
    return render(request, 'billing/company_profile.html', {'form': form})

@superuser_required_with_login
@csrf_exempt
def add_invoice_item(request):
    """AJAX endpoint to add invoice item"""
    if request.method == 'POST':
        data = json.loads(request.body)
        
        # Validate data
        if not all(key in data for key in ['description', 'quantity', 'unit_price']):
            return JsonResponse({'error': 'Missing required fields'}, status=400)
        
        try:
            from decimal import Decimal
            quantity = int(data['quantity'])
            unit_price = Decimal(str(data['unit_price']))
            total_price = quantity * unit_price
            
            return JsonResponse({
                'success': True,
                'total_price': float(total_price)
            })
        except (ValueError, TypeError):
            return JsonResponse({'error': 'Invalid data format'}, status=400)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)