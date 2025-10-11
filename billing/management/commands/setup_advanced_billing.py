from django.core.management.base import BaseCommand
from billing.advanced_models import AdvancedCompanyProfile, AdvancedCustomer, AdvancedInvoice, AdvancedInvoiceItem
from decimal import Decimal
import uuid

class Command(BaseCommand):
    help = 'Sets up the advanced billing system with sample data.'

    def handle(self, *args, **kwargs):
        self.stdout.write('Setting up advanced billing system...')

        # Create advanced company profile
        company, created = AdvancedCompanyProfile.objects.get_or_create(
            id=1,
            defaults={
                'name': 'King Dupatta House',
                'gst_number': '098TQPA7336F1ZI',
                'pan_number': 'TQPA7336F',
                'address': 'AKBARI GATE, NAKHAS CHOWK, LUCKNOW',
                'phone': '7860247786',
                'email': 'kingdupattahouse@gmail.com',
                'website': 'https://kingdupattahouse.com',
                'bank_name': 'HDFC BANK, LUCKNOW CHOWK - UTTAR PRADESH',
                'account_number': '50200016138197',
                'ifsc_code': 'HDFC0000596',
                'currency': 'INR',
                'timezone': 'Asia/Kolkata',
                'invoice_prefix': 'INV'
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS('✅ Created advanced company profile'))
        else:
            self.stdout.write('ℹ️  Advanced company profile already exists')

        # Create sample customers
        customers_data = [
            {
                'name': 'Mrs. Priya Sharma',
                'email': 'priya.sharma@email.com',
                'phone': '+91-9876543211',
                'address': '123 Main Street, Sector 5',
                'city': 'Lucknow',
                'state': 'Uttar Pradesh',
                'pincode': '226001',
                'customer_type': 'individual',
                'credit_limit': 50000,
                'payment_terms': 30
            },
            {
                'name': 'Fashion Store Pvt Ltd',
                'email': 'orders@fashionstore.com',
                'phone': '+91-9876543212',
                'address': '456 Business Park, Industrial Area',
                'city': 'Delhi',
                'state': 'Delhi',
                'pincode': '110001',
                'customer_type': 'business',
                'gst_number': '07XYZ1234A1B2C3',
                'pan_number': 'XYZ1234A1B',
                'credit_limit': 200000,
                'payment_terms': 45
            },
            {
                'name': 'Government Department',
                'email': 'purchase@gov.in',
                'phone': '+91-9876543213',
                'address': '789 Government Complex',
                'city': 'Mumbai',
                'state': 'Maharashtra',
                'pincode': '400001',
                'customer_type': 'government',
                'gst_number': '27GOV1234A1B2C3',
                'credit_limit': 500000,
                'payment_terms': 60
            }
        ]

        for customer_data in customers_data:
            customer, created = AdvancedCustomer.objects.get_or_create(
                name=customer_data['name'],
                defaults=customer_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✅ Created customer: {customer.name}'))
            else:
                self.stdout.write(f'ℹ️  Customer "{customer.name}" already exists')

        # Create sample invoice
        try:
            sample_customer = AdvancedCustomer.objects.first()
            if sample_customer:
                # Create invoice first
                invoice = AdvancedInvoice(
                    customer=sample_customer,
                    company=company,
                    date='2025-01-01',
                    due_date='2025-01-31',
                    status='paid',
                    payment_method='bank_transfer',
                    payment_reference='TXN123456',
                    notes='Thank you for your business!',
                    terms_conditions='Payment due within 30 days. Late payments may incur additional charges.'
                )
                invoice.save()  # Save to get primary key
                
                # Create items without triggering the save method that updates invoice
                items_data = [
                    {
                        'description': 'Premium Silk Dupatta - Red',
                        'category': 'Dupattas',
                        'quantity': Decimal('2'),
                        'unit': 'pcs',
                        'unit_price': Decimal('1500.00'),
                        'tax_rate': Decimal('18.00')
                    },
                    {
                        'description': 'Cotton Leggings - Black',
                        'category': 'Leggings',
                        'quantity': Decimal('5'),
                        'unit': 'pcs',
                        'unit_price': Decimal('299.00'),
                        'tax_rate': Decimal('18.00')
                    },
                    {
                        'description': 'Designer Stole - Gold',
                        'category': 'Stoles',
                        'quantity': Decimal('1'),
                        'unit': 'pcs',
                        'unit_price': Decimal('899.00'),
                        'discount_percentage': Decimal('10.00'),
                        'tax_rate': Decimal('18.00')
                    }
                ]
                
                # Create items using regular create
                for item_data in items_data:
                    AdvancedInvoiceItem.objects.create(
                        invoice=invoice,
                        **item_data
                    )
                
                # Recalculate totals
                invoice.calculate_amounts()
                invoice.save()
                
                self.stdout.write(self.style.SUCCESS('✅ Created sample invoice with items'))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'⚠️  Could not create sample invoice: {e}'))

        self.stdout.write(self.style.SUCCESS('\n🎉 Advanced billing system setup complete!'))
        self.stdout.write('\n📋 What\'s been set up:')
        self.stdout.write('• Advanced company profile with banking details')
        self.stdout.write('• 3 sample customers (Individual, Business, Government)')
        self.stdout.write('• Sample invoice with multiple items')
        self.stdout.write('• Advanced features: analytics, reporting, payment tracking')
        self.stdout.write('\n💡 Access advanced billing at: http://127.0.0.1:8000/bill/')
        self.stdout.write('🔐 Login required - use your admin credentials')
        self.stdout.write('\n🚀 Features available:')
        self.stdout.write('• Advanced dashboard with analytics')
        self.stdout.write('• Customer management with detailed profiles')
        self.stdout.write('• Invoice creation with multiple items')
        self.stdout.write('• Payment tracking and status management')
        self.stdout.write('• Professional invoice printing')
        self.stdout.write('• Revenue analytics and reporting')
