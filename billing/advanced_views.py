from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import datetime, timedelta
import json
import uuid
from decimal import Decimal

from .advanced_models import (
    AdvancedCompanyProfile, AdvancedCustomer, AdvancedInvoice, 
    AdvancedInvoiceItem, PaymentRecord, InvoiceTemplate
)
from .decorators import superuser_required_with_login

@superuser_required_with_login
def advanced_dashboard(request):
    """Advanced billing dashboard with analytics"""
    # Get company profile
    company = AdvancedCompanyProfile.objects.get_or_create(id=1)[0]
    
    # Analytics data
    total_invoices = AdvancedInvoice.objects.count()
    paid_invoices = AdvancedInvoice.objects.filter(status='paid').count()
    overdue_invoices = AdvancedInvoice.objects.filter(
        status__in=['sent', 'viewed'], 
        due_date__lt=timezone.now().date()
    ).count()
    
    # Financial analytics
    total_revenue = AdvancedInvoice.objects.filter(status='paid').aggregate(
        total=Sum('total_amount')
    )['total'] or 0
    
    pending_amount = AdvancedInvoice.objects.filter(
        status__in=['sent', 'viewed']
    ).aggregate(total=Sum('total_amount'))['total'] or 0
    
    # Recent activity
    recent_invoices = AdvancedInvoice.objects.select_related('customer').order_by('-created_at')[:10]
    
    # Monthly revenue (last 6 months)
    six_months_ago = timezone.now().date() - timedelta(days=180)
    monthly_data = []
    for i in range(6):
        month_start = six_months_ago + timedelta(days=30*i)
        month_end = month_start + timedelta(days=30)
        revenue = AdvancedInvoice.objects.filter(
            status='paid',
            paid_date__date__range=[month_start, month_end]
        ).aggregate(total=Sum('total_amount'))['total'] or 0
        monthly_data.append({
            'month': month_start.strftime('%b %Y'),
            'revenue': float(revenue)
        })
    
    # Top customers
    top_customers = AdvancedCustomer.objects.annotate(
        total_spent=Sum('invoices__total_amount', filter=Q(invoices__status='paid'))
    ).order_by('-total_spent')[:5]
    
    context = {
        'company': company,
        'total_invoices': total_invoices,
        'paid_invoices': paid_invoices,
        'overdue_invoices': overdue_invoices,
        'total_revenue': total_revenue,
        'pending_amount': pending_amount,
        'recent_invoices': recent_invoices,
        'monthly_data': monthly_data,
        'top_customers': top_customers,
    }
    return render(request, 'billing/advanced_dashboard.html', context)

@superuser_required_with_login
def advanced_customer_list(request):
    """Advanced customer management"""
    customers = AdvancedCustomer.objects.all().order_by('-created_at')
    
    # Search functionality
    search = request.GET.get('search')
    if search:
        customers = customers.filter(
            Q(name__icontains=search) | 
            Q(email__icontains=search) | 
            Q(phone__icontains=search)
        )
    
    # Filter by type
    customer_type = request.GET.get('type')
    if customer_type:
        customers = customers.filter(customer_type=customer_type)
    
    context = {
        'customers': customers,
        'search': search,
        'customer_type': customer_type,
    }
    return render(request, 'billing/advanced_customer_list.html', context)

@superuser_required_with_login
def advanced_customer_detail(request, customer_id):
    """Detailed customer view"""
    customer = get_object_or_404(AdvancedCustomer, customer_id=customer_id)
    invoices = customer.invoices.all().order_by('-created_at')
    
    # Customer statistics
    total_invoices = invoices.count()
    paid_invoices = invoices.filter(status='paid').count()
    total_spent = invoices.filter(status='paid').aggregate(
        total=Sum('total_amount')
    )['total'] or 0
    
    context = {
        'customer': customer,
        'invoices': invoices,
        'total_invoices': total_invoices,
        'paid_invoices': paid_invoices,
        'total_spent': total_spent,
    }
    return render(request, 'billing/advanced_customer_detail.html', context)

@superuser_required_with_login
def advanced_invoice_create(request):
    """Advanced invoice creation with multiple features"""
    if request.method == 'POST':
        try:
            # Get form data
            customer_id = request.POST.get('customer')
            invoice_date = request.POST.get('date')
            due_date = request.POST.get('due_date')
            notes = request.POST.get('notes', '')
            terms = request.POST.get('terms', '')
            discount_percentage = Decimal(request.POST.get('discount_percentage', 0))
            
            # Get customer and company
            customer = AdvancedCustomer.objects.get(customer_id=customer_id)
            company = AdvancedCompanyProfile.objects.get(id=1)
            
            # Create invoice first
            invoice = AdvancedInvoice(
                customer=customer,
                company=company,
                date=datetime.strptime(invoice_date, '%Y-%m-%d').date(),
                due_date=datetime.strptime(due_date, '%Y-%m-%d').date(),
                notes=notes,
                terms_conditions=terms,
                discount_percentage=discount_percentage,
                status='draft'
            )
            invoice.save()  # Save to get primary key
            
            # Add invoice items after invoice is saved
            items_data = request.POST.getlist('items')
            for item_data in items_data:
                if item_data:
                    item_json = json.loads(item_data)
                    AdvancedInvoiceItem.objects.create(
                        invoice=invoice,
                        item_code=item_json.get('item_code', ''),
                        description=item_json['description'],
                        category=item_json.get('category', ''),
                        quantity=Decimal(str(item_json['quantity'])),
                        unit=item_json.get('unit', 'pcs'),
                        unit_price=Decimal(str(item_json['unit_price'])),
                        discount_percentage=Decimal(str(item_json.get('discount_percentage', 0))),
                        tax_rate=Decimal(str(item_json.get('tax_rate', 18))),
                        notes=item_json.get('notes', '')
                    )
            
            # Recalculate totals after all items are added
            invoice.calculate_amounts()
            invoice.save()
            
            messages.success(request, f'Invoice {invoice.invoice_number} created successfully!')
            return redirect('billing:advanced_invoice_detail', invoice_id=invoice.invoice_id)
            
        except Exception as e:
            messages.error(request, f'Error creating invoice: {str(e)}')
    
    customers = AdvancedCustomer.objects.filter(is_active=True)
    company = AdvancedCompanyProfile.objects.get_or_create(id=1)[0]
    
    context = {
        'customers': customers,
        'company': company,
    }
    return render(request, 'billing/advanced_invoice_create.html', context)

@superuser_required_with_login
def advanced_invoice_detail(request, invoice_id):
    """Advanced invoice detail view"""
    invoice = get_object_or_404(AdvancedInvoice, invoice_id=invoice_id)
    payments = invoice.payments.all().order_by('-payment_date')
    
    context = {
        'invoice': invoice,
        'payments': payments,
    }
    return render(request, 'billing/advanced_invoice_detail.html', context)

@superuser_required_with_login
def advanced_invoice_print(request, invoice_id):
    """Advanced invoice printing with templates"""
    invoice = get_object_or_404(AdvancedInvoice, invoice_id=invoice_id)
    
    # Get template (you can extend this to use different templates)
    template = InvoiceTemplate.objects.filter(is_active=True).first()
    
    context = {
        'invoice': invoice,
        'template': template,
    }
    return render(request, 'billing/advanced_invoice_print.html', context)

@superuser_required_with_login
def advanced_invoice_list(request):
    """Advanced invoice listing with filters"""
    invoices = AdvancedInvoice.objects.select_related('customer').order_by('-created_at')
    
    # Filters
    status = request.GET.get('status')
    if status:
        invoices = invoices.filter(status=status)
    
    customer = request.GET.get('customer')
    if customer:
        invoices = invoices.filter(customer__name__icontains=customer)
    
    date_from = request.GET.get('date_from')
    if date_from:
        invoices = invoices.filter(date__gte=date_from)
    
    date_to = request.GET.get('date_to')
    if date_to:
        invoices = invoices.filter(date__lte=date_to)
    
    context = {
        'invoices': invoices,
        'status': status,
        'customer': customer,
        'date_from': date_from,
        'date_to': date_to,
    }
    return render(request, 'billing/advanced_invoice_list.html', context)

@superuser_required_with_login
def mark_invoice_paid(request, invoice_id):
    """Mark invoice as paid with payment details"""
    if request.method == 'POST':
        invoice = get_object_or_404(AdvancedInvoice, invoice_id=invoice_id)
        
        payment_method = request.POST.get('payment_method')
        payment_reference = request.POST.get('payment_reference', '')
        notes = request.POST.get('notes', '')
        
        # Create payment record
        PaymentRecord.objects.create(
            invoice=invoice,
            amount=invoice.total_amount,
            payment_method=payment_method,
            payment_reference=payment_reference,
            notes=notes
        )
        
        # Mark invoice as paid
        invoice.mark_as_paid(payment_method, payment_reference)
        
        messages.success(request, f'Invoice {invoice.invoice_number} marked as paid!')
        return redirect('billing:advanced_invoice_detail', invoice_id=invoice_id)
    
    invoice = get_object_or_404(AdvancedInvoice, invoice_id=invoice_id)
    return render(request, 'billing/mark_paid.html', {'invoice': invoice})

@superuser_required_with_login
def advanced_analytics(request):
    """Advanced analytics and reports - Simplified version"""
    try:
        # Provide sample data for demonstration
        monthly_revenue = [
            {'month': 'Jan', 'revenue': 0},
            {'month': 'Feb', 'revenue': 0},
            {'month': 'Mar', 'revenue': 0},
            {'month': 'Apr', 'revenue': 0},
            {'month': 'May', 'revenue': 0},
            {'month': 'Jun', 'revenue': 0},
            {'month': 'Jul', 'revenue': 0},
            {'month': 'Aug', 'revenue': 0},
            {'month': 'Sep', 'revenue': 0},
            {'month': 'Oct', 'revenue': 0},
            {'month': 'Nov', 'revenue': 0},
            {'month': 'Dec', 'revenue': 0}
        ]
        
        customer_stats = []
        status_stats = []
        
        context = {
            'monthly_revenue': monthly_revenue,
            'customer_stats': customer_stats,
            'status_stats': status_stats,
        }
        return render(request, 'billing/advanced_analytics.html', context)
    except Exception as e:
        # If there's any error, return a simple error page
        from django.http import HttpResponse
        return HttpResponse(f"Analytics page error: {str(e)}")

@superuser_required_with_login
@csrf_exempt
def ajax_calculate_totals(request):
    """AJAX endpoint for real-time calculations"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            items = data.get('items', [])
            
            subtotal = Decimal('0')
            total_tax = Decimal('0')
            total_discount = Decimal('0')
            
            for item in items:
                quantity = Decimal(str(item['quantity']))
                unit_price = Decimal(str(item['unit_price']))
                discount_pct = Decimal(str(item.get('discount_percentage', 0)))
                tax_rate = Decimal(str(item.get('tax_rate', 18)))
                
                item_subtotal = quantity * unit_price
                item_discount = (item_subtotal * discount_pct) / 100
                item_taxable = item_subtotal - item_discount
                item_tax = (item_taxable * tax_rate) / 100
                
                subtotal += item_subtotal
                total_discount += item_discount
                total_tax += item_tax
            
            # Apply invoice-level discount
            invoice_discount_pct = Decimal(str(data.get('invoice_discount_percentage', 0)))
            invoice_discount = (subtotal * invoice_discount_pct) / 100
            final_subtotal = subtotal - invoice_discount
            
            total_amount = final_subtotal + total_tax
            
            return JsonResponse({
                'success': True,
                'subtotal': float(subtotal),
                'discount': float(total_discount + invoice_discount),
                'tax': float(total_tax),
                'total': float(total_amount)
            })
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Invalid request'}, status=405)


@superuser_required_with_login
def company_profile(request):
    """Company profile management"""
    try:
        company = AdvancedCompanyProfile.objects.get_or_create(id=1)[0]
        
        if request.method == 'POST':
            # Update company profile
            company.company_name = request.POST.get('company_name', company.company_name)
            company.address = request.POST.get('address', company.address)
            company.city = request.POST.get('city', company.city)
            company.state = request.POST.get('state', company.state)
            company.pincode = request.POST.get('pincode', company.pincode)
            company.phone = request.POST.get('phone', company.phone)
            company.email = request.POST.get('email', company.email)
            company.gst_number = request.POST.get('gst_number', company.gst_number)
            company.pan_number = request.POST.get('pan_number', company.pan_number)
            company.bank_name = request.POST.get('bank_name', company.bank_name)
            company.account_number = request.POST.get('account_number', company.account_number)
            company.ifsc_code = request.POST.get('ifsc_code', company.ifsc_code)
            company.save()
            
            messages.success(request, 'Company profile updated successfully!')
            return redirect('billing:company_profile')
        
        context = {
            'company': company,
        }
        return render(request, 'billing/company_profile.html', context)
        
    except Exception as e:
        messages.error(request, f'Error loading company profile: {str(e)}')
        return render(request, 'billing/company_profile.html', {'company': None})
