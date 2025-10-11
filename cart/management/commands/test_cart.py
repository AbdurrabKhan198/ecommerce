from django.core.management.base import BaseCommand
from django.test import Client
from django.contrib.auth import get_user_model
from shop.models import Product

class Command(BaseCommand):
    help = 'Test cart functionality for both authenticated and anonymous users'

    def handle(self, *args, **options):
        self.stdout.write("🧪 Testing Cart Functionality...")
        
        # Create test client
        client = Client()
        
        # Test 1: Anonymous user cart
        self.stdout.write("\n1️⃣ Testing Anonymous User Cart...")
        
        # Get a product
        try:
            product = Product.objects.filter(is_active=True).first()
            if not product:
                self.stdout.write(self.style.ERROR("❌ No active products found!"))
                return
            
            self.stdout.write(f"✅ Found product: {product.name}")
            
            # Test adding to cart via AJAX
            response = client.post('/cart/ajax/add/', 
                                 data='{"product_id": ' + str(product.id) + ', "quantity": 1}',
                                 content_type='application/json')
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    self.stdout.write(f"✅ Anonymous user can add to cart: {data.get('message')}")
                    self.stdout.write(f"✅ Cart count: {data.get('cart_count')}")
                else:
                    self.stdout.write(f"❌ Failed to add to cart: {data.get('error')}")
                    return
            else:
                self.stdout.write(f"❌ AJAX request failed with status: {response.status_code}")
                return
            
            # Test cart detail page
            response = client.get('/cart/')
            if response.status_code == 200:
                self.stdout.write("✅ Anonymous user can view cart page")
            else:
                self.stdout.write(f"❌ Cart page failed with status: {response.status_code}")
                return
                
        except Exception as e:
            self.stdout.write(f"❌ Anonymous user test failed: {str(e)}")
            return
        
        # Test 2: Authenticated user cart
        self.stdout.write("\n2️⃣ Testing Authenticated User Cart...")
        
        try:
            # Create or get test user
            User = get_user_model()
            user, created = User.objects.get_or_create(
                email='test@example.com',
                defaults={
                    'username': 'testuser',
                    'first_name': 'Test',
                    'last_name': 'User'
                }
            )
            if created:
                user.set_password('testpass123')
                user.save()
                self.stdout.write("✅ Created test user")
            else:
                self.stdout.write("✅ Using existing test user")
            
            # Login
            login_success = client.login(email='test@example.com', password='testpass123')
            if not login_success:
                self.stdout.write("❌ Failed to login test user")
                return
            
            self.stdout.write("✅ Test user logged in")
            
            # Test adding to cart via AJAX
            response = client.post('/cart/ajax/add/', 
                                 data='{"product_id": ' + str(product.id) + ', "quantity": 2}',
                                 content_type='application/json')
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    self.stdout.write(f"✅ Authenticated user can add to cart: {data.get('message')}")
                    self.stdout.write(f"✅ Cart count: {data.get('cart_count')}")
                else:
                    self.stdout.write(f"❌ Failed to add to cart: {data.get('error')}")
                    return
            else:
                self.stdout.write(f"❌ AJAX request failed with status: {response.status_code}")
                return
            
            # Test cart detail page
            response = client.get('/cart/')
            if response.status_code == 200:
                self.stdout.write("✅ Authenticated user can view cart page")
            else:
                self.stdout.write(f"❌ Cart page failed with status: {response.status_code}")
                return
                
        except Exception as e:
            self.stdout.write(f"❌ Authenticated user test failed: {str(e)}")
            return
        
        self.stdout.write("\n🎉 All cart functionality tests passed!")
        self.stdout.write("✅ Cart functionality is working for both anonymous and authenticated users!")
