from django.core.management.base import BaseCommand
from billing.models import CompanyProfile, Customer

class Command(BaseCommand):
    help = 'Sets up the billing system with default company profile and sample customer.'

    def handle(self, *args, **kwargs):
        self.stdout.write('Setting up billing system...')

        # Create or update company profile
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
        
        if created:
            self.stdout.write(self.style.SUCCESS('✅ Created company profile'))
        else:
            self.stdout.write('ℹ️  Company profile already exists')

        # Create sample customer
        sample_customer, created = Customer.objects.get_or_create(
            name='Sample Customer',
            defaults={
                'email': 'customer@example.com',
                'phone': '+91-9876543211',
                'address': '123 Main Street, City, State',
                'gst_number': '09XYZ1234A1B2C3'
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS('✅ Created sample customer'))
        else:
            self.stdout.write('ℹ️  Sample customer already exists')

        self.stdout.write(self.style.SUCCESS('\n🎉 Billing system setup complete!'))
        self.stdout.write('\n📋 What\'s been set up:')
        self.stdout.write('• Company profile with GST details')
        self.stdout.write('• Sample customer for testing')
        self.stdout.write('\n💡 Access billing at: http://127.0.0.1:8000/bill/')
        self.stdout.write('🔐 Login required - use your admin credentials')
