from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

class CompanyProfile(models.Model):
    """Company profile for billing"""
    name = models.CharField(max_length=200, default="King Dupatta House")
    gst_number = models.CharField(max_length=15, default="09ABCDE1234F1Z5")
    address = models.TextField(default="Akbari Gate, Near Nakkhas, Victoria Street, Nakkhas-226003, Lucknow, Uttar Pradesh")
    phone = models.CharField(max_length=15, default="+91-9876543210")
    email = models.EmailField(default="info@kingdupattahouse.com")
    logo = models.ImageField(upload_to='billing/logos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Company Profile"
        verbose_name_plural = "Company Profiles"

    def __str__(self):
        return self.name

class Customer(models.Model):
    """Customer for billing"""
    name = models.CharField(max_length=200)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    gst_number = models.CharField(max_length=15, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"

    def __str__(self):
        return self.name

class Invoice(models.Model):
    """Invoice model"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
    ]

    invoice_number = models.CharField(max_length=50, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE)
    date = models.DateField()
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=18.00)  # GST 18%
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Invoice"
        verbose_name_plural = "Invoices"
        ordering = ['-created_at']

    def __str__(self):
        return f"Invoice #{self.invoice_number} - {self.customer.name}"

    def save(self, *args, **kwargs):
        if not self.invoice_number:
            # Generate invoice number
            last_invoice = Invoice.objects.order_by('-id').first()
            if last_invoice:
                last_num = int(last_invoice.invoice_number.split('#')[-1])
                self.invoice_number = f"INV#{last_num + 1:04d}"
            else:
                self.invoice_number = "INV#0001"
        
        # Calculate tax and total
        from decimal import Decimal
        self.tax_amount = (self.subtotal * Decimal(str(self.tax_rate))) / 100
        self.total_amount = self.subtotal + self.tax_amount
        
        super().save(*args, **kwargs)

class InvoiceItem(models.Model):
    """Invoice items"""
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    description = models.CharField(max_length=200)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Invoice Item"
        verbose_name_plural = "Invoice Items"

    def __str__(self):
        return f"{self.description} - {self.invoice.invoice_number}"

    def save(self, *args, **kwargs):
        from decimal import Decimal
        self.total_price = Decimal(str(self.quantity)) * self.unit_price
        super().save(*args, **kwargs)
        
        # Update invoice subtotal
        self.invoice.subtotal = sum(item.total_price for item in self.invoice.items.all())
        self.invoice.save()