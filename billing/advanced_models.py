from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from datetime import timedelta
import uuid
import json

class AdvancedCompanyProfile(models.Model):
    """Advanced company profile with multiple locations"""
    name = models.CharField(max_length=200, default="King Dupatta House")
    gst_number = models.CharField(max_length=15, default="09ABCDE1234F1Z5")
    pan_number = models.CharField(max_length=10, default="ABCDE1234F")
    address = models.TextField(default="Akbari Gate, Near Nakkhas, Victoria Street, Nakkhas-226003, Lucknow, Uttar Pradesh")
    phone = models.CharField(max_length=15, default="+91-9876543210")
    email = models.EmailField(default="info@kingdupattahouse.com")
    website = models.URLField(blank=True, null=True)
    logo = models.ImageField(upload_to='billing/logos/', blank=True, null=True)
    
    # Banking details
    bank_name = models.CharField(max_length=100, default="State Bank of India")
    account_number = models.CharField(max_length=20, default="1234567890")
    ifsc_code = models.CharField(max_length=11, default="SBIN0001234")
    
    # Additional settings
    currency = models.CharField(max_length=3, default="INR")
    timezone = models.CharField(max_length=50, default="Asia/Kolkata")
    invoice_prefix = models.CharField(max_length=10, default="INV")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Advanced Company Profile"
        verbose_name_plural = "Advanced Company Profiles"

    def __str__(self):
        return self.name

    @property
    def full_address(self):
        return f"{self.address}\nPhone: {self.phone}\nEmail: {self.email}"

class AdvancedCustomer(models.Model):
    """Advanced customer with detailed information"""
    CUSTOMER_TYPE_CHOICES = [
        ('individual', 'Individual'),
        ('business', 'Business'),
        ('government', 'Government'),
    ]
    
    customer_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=200)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    alternate_phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    pincode = models.CharField(max_length=10, blank=True, null=True)
    country = models.CharField(max_length=50, default="India")
    
    # Business details
    customer_type = models.CharField(max_length=20, choices=CUSTOMER_TYPE_CHOICES, default='individual')
    gst_number = models.CharField(max_length=15, blank=True, null=True)
    pan_number = models.CharField(max_length=10, blank=True, null=True)
    
    # Additional info
    credit_limit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_terms = models.PositiveIntegerField(default=30)  # days
    notes = models.TextField(blank=True, null=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Advanced Customer"
        verbose_name_plural = "Advanced Customers"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.customer_id})"

    @property
    def full_address(self):
        address_parts = [self.address, self.city, self.state, self.pincode, self.country]
        return ", ".join(filter(None, address_parts))

    @property
    def total_invoices(self):
        return self.invoices.count()

    @property
    def total_amount(self):
        return sum(invoice.total_amount for invoice in self.invoices.filter(status='paid'))

class AdvancedInvoice(models.Model):
    """Advanced invoice with comprehensive features"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('viewed', 'Viewed'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
        ('cancelled', 'Cancelled'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('bank_transfer', 'Bank Transfer'),
        ('cheque', 'Cheque'),
        ('upi', 'UPI'),
        ('card', 'Card'),
        ('other', 'Other'),
    ]
    
    invoice_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    invoice_number = models.CharField(max_length=50, unique=True)
    customer = models.ForeignKey(AdvancedCustomer, on_delete=models.CASCADE, related_name='invoices')
    company = models.ForeignKey(AdvancedCompanyProfile, on_delete=models.CASCADE)
    
    # Dates
    date = models.DateField()
    due_date = models.DateField()
    sent_date = models.DateTimeField(blank=True, null=True)
    paid_date = models.DateTimeField(blank=True, null=True)
    
    # Status and payment
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, blank=True, null=True)
    payment_reference = models.CharField(max_length=100, blank=True, null=True)
    
    # Financial details
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0, 
                                           validators=[MinValueValidator(0), MaxValueValidator(100)])
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('18.00'))
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Additional fields
    notes = models.TextField(blank=True, null=True)
    terms_conditions = models.TextField(blank=True, null=True)
    internal_notes = models.TextField(blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Advanced Invoice"
        verbose_name_plural = "Advanced Invoices"
        ordering = ['-created_at']

    def __str__(self):
        return f"Invoice #{self.invoice_number} - {self.customer.name}"

    def save(self, *args, **kwargs):
        if not self.invoice_number:
            self.invoice_number = self.generate_invoice_number()
        
        # Calculate amounts
        self.calculate_amounts()
        super().save(*args, **kwargs)

    def generate_invoice_number(self):
        """Generate unique invoice number"""
        company = self.company
        prefix = company.invoice_prefix
        last_invoice = AdvancedInvoice.objects.filter(
            invoice_number__startswith=prefix
        ).order_by('-id').first()
        
        if last_invoice:
            try:
                last_num = int(last_invoice.invoice_number.split(prefix)[-1])
                return f"{prefix}{last_num + 1:04d}"
            except:
                return f"{prefix}0001"
        return f"{prefix}0001"

    def calculate_amounts(self):
        """Calculate all financial amounts"""
        from decimal import Decimal
        
        # Only calculate if invoice has a primary key
        if self.pk:
            # Calculate subtotal from items
            self.subtotal = sum(item.total_price for item in self.items.all())
            
            # Calculate discount
            self.discount_amount = (self.subtotal * self.discount_percentage) / Decimal('100')
            
            # Calculate taxable amount
            taxable_amount = self.subtotal - self.discount_amount
            
            # Calculate tax
            self.tax_amount = (taxable_amount * self.tax_rate) / Decimal('100')
            
            # Calculate total
            self.total_amount = taxable_amount + self.tax_amount

    @property
    def is_overdue(self):
        """Check if invoice is overdue"""
        return self.status not in ['paid', 'cancelled'] and timezone.now().date() > self.due_date

    @property
    def days_overdue(self):
        """Calculate days overdue"""
        if self.is_overdue:
            return (timezone.now().date() - self.due_date).days
        return 0

    def mark_as_sent(self):
        """Mark invoice as sent"""
        self.status = 'sent'
        self.sent_date = timezone.now()
        self.save()

    def mark_as_paid(self, payment_method=None, payment_reference=None):
        """Mark invoice as paid"""
        self.status = 'paid'
        self.paid_date = timezone.now()
        if payment_method:
            self.payment_method = payment_method
        if payment_reference:
            self.payment_reference = payment_reference
        self.save()

class AdvancedInvoiceItem(models.Model):
    """Advanced invoice items with detailed features"""
    invoice = models.ForeignKey(AdvancedInvoice, on_delete=models.CASCADE, related_name='items')
    
    # Item details
    item_code = models.CharField(max_length=50, blank=True, null=True)
    description = models.CharField(max_length=200)
    category = models.CharField(max_length=50, blank=True, null=True)
    
    # Quantities and pricing
    quantity = models.DecimalField(max_digits=10, decimal_places=3, default=1)
    unit = models.CharField(max_length=20, default="pcs")
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Discounts
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0,
                                           validators=[MinValueValidator(0), MaxValueValidator(100)])
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Tax
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('18.00'))
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Final amounts
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Additional info
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Advanced Invoice Item"
        verbose_name_plural = "Advanced Invoice Items"
        ordering = ['id']

    def __str__(self):
        if self.invoice and self.invoice.pk:
            return f"{self.description} - {self.invoice.invoice_number}"
        return f"{self.description} - New Item"

    def save(self, *args, **kwargs):
        self.calculate_amounts()
        super().save(*args, **kwargs)
        
        # Temporarily disable automatic invoice update to avoid circular issues
        # Update invoice totals only if invoice has a primary key and not during bulk creation
        # if self.invoice.pk and not kwargs.get('update_fields'):
        #     self.invoice.calculate_amounts()
        #     self.invoice.save()

    def calculate_amounts(self):
        """Calculate all amounts for this item"""
        from decimal import Decimal
        
        # Calculate subtotal
        self.subtotal = self.quantity * self.unit_price
        
        # Calculate discount
        self.discount_amount = (self.subtotal * self.discount_percentage) / Decimal('100')
        
        # Calculate taxable amount
        taxable_amount = self.subtotal - self.discount_amount
        
        # Calculate tax
        self.tax_amount = (taxable_amount * self.tax_rate) / Decimal('100')
        
        # Calculate total
        self.total_price = taxable_amount + self.tax_amount

class PaymentRecord(models.Model):
    """Track payments for invoices"""
    invoice = models.ForeignKey(AdvancedInvoice, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=AdvancedInvoice.PAYMENT_METHOD_CHOICES)
    payment_reference = models.CharField(max_length=100, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    payment_date = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Payment Record"
        verbose_name_plural = "Payment Records"
        ordering = ['-payment_date']

    def __str__(self):
        return f"Payment of ₹{self.amount} for {self.invoice.invoice_number}"

class InvoiceTemplate(models.Model):
    """Customizable invoice templates"""
    name = models.CharField(max_length=100)
    template_type = models.CharField(max_length=20, choices=[
        ('standard', 'Standard'),
        ('detailed', 'Detailed'),
        ('minimal', 'Minimal'),
    ], default='standard')
    
    # Template settings
    show_logo = models.BooleanField(default=True)
    show_company_details = models.BooleanField(default=True)
    show_customer_details = models.BooleanField(default=True)
    show_payment_terms = models.BooleanField(default=True)
    show_notes = models.BooleanField(default=True)
    
    # Styling
    primary_color = models.CharField(max_length=7, default="#c2185b")
    secondary_color = models.CharField(max_length=7, default="#512da8")
    font_family = models.CharField(max_length=50, default="Arial, sans-serif")
    
    # Content
    header_text = models.TextField(blank=True, null=True)
    footer_text = models.TextField(blank=True, null=True)
    terms_conditions = models.TextField(blank=True, null=True)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Invoice Template"
        verbose_name_plural = "Invoice Templates"

    def __str__(self):
        return self.name
