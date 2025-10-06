from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from shop.models import Category, SubCategory, Product, ProductImage, ProductVariant
from accounts.models import Address
from decimal import Decimal

User = get_user_model()


class Command(BaseCommand):
    help = 'Seed the database with sample data for women\'s wear e-commerce'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting data seeding...'))
        
        # Create superuser if not exists
        self.create_superuser()
        
        # Create categories and subcategories
        self.create_categories()
        
        # Create sample products
        self.create_products()
        
        self.stdout.write(self.style.SUCCESS('Data seeding completed successfully!'))

    def create_superuser(self):
        """Create a superuser if it doesn't exist"""
        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123',
                first_name='Admin',
                last_name='User'
            )
            self.stdout.write('Created superuser: admin@example.com / admin123')

    def create_categories(self):
        """Create categories and subcategories"""
        categories_data = {
            'Leggings': {
                'description': 'Comfortable and stylish leggings for all occasions',
                'subcategories': [
                    ('Ankle Length', 'Perfect for everyday wear with ankle-length coverage'),
                    ('Churidar', 'Traditional style with gathered ankle design'),
                    ('Jeggings', 'Denim look with legging comfort'),
                    ('Printed', 'Vibrant patterns and designs'),
                    ('Solid', 'Classic solid colors for versatile styling'),
                ]
            },
            'Pants': {
                'description': 'Versatile pants and trousers for modern women',
                'subcategories': [
                    ('Palazzo', 'Flowy wide-leg pants for comfort'),
                    ('Trousers', 'Classic formal and casual trousers'),
                    ('Cigarette', 'Slim tapered fit for modern look'),
                    ('Wide-leg', 'Contemporary wide-leg designs'),
                    ('Formal', 'Professional wear for office'),
                ]
            },
            'Dupattas': {
                'description': 'Traditional dupattas in various fabrics and designs',
                'subcategories': [
                    ('Cotton', 'Pure cotton for daily wear'),
                    ('Silk', 'Luxurious silk for special occasions'),
                    ('Net', 'Delicate net fabric designs'),
                    ('Printed', 'Beautiful printed patterns'),
                    ('Embroidered', 'Intricate embroidery work'),
                ]
            }
        }
        
        for cat_name, cat_data in categories_data.items():
            category, created = Category.objects.get_or_create(
                name=cat_name,
                defaults={
                    'slug': cat_name.lower(),
                    'description': cat_data['description'],
                    'is_active': True,
                    'sort_order': list(categories_data.keys()).index(cat_name)
                }
            )
            
            if created:
                self.stdout.write(f'Created category: {cat_name}')
            
            # Create subcategories
            for idx, (subcat_name, subcat_desc) in enumerate(cat_data['subcategories']):
                subcategory, created = SubCategory.objects.get_or_create(
                    category=category,
                    name=subcat_name,
                    defaults={
                        'slug': subcat_name.lower().replace(' ', '-'),
                        'description': subcat_desc,
                        'is_active': True,
                        'sort_order': idx
                    }
                )
                
                if created:
                    self.stdout.write(f'  Created subcategory: {subcat_name}')

    def create_products(self):
        """Create sample products"""
        categories = Category.objects.all()
        
        sample_products = [
            {
                'name': 'Premium Black Ankle Length Leggings',
                'category': 'Leggings',
                'subcategory': 'Ankle Length',
                'description': 'Ultra-soft cotton blend leggings with high-rise waistband for all-day comfort.',
                'short_description': 'Comfortable ankle length leggings in premium cotton blend',
                'fabric': 'cotton_blend',
                'occasion': 'casual',
                'mrp': Decimal('899.00'),
                'selling_price': Decimal('649.00'),
                'stock_quantity': 50,
                'is_featured': True,
                'sizes': ['S', 'M', 'L', 'XL'],
                'colors': [('Black', '#000000'), ('Navy', '#000080'), ('Grey', '#808080')]
            },
            {
                'name': 'Floral Print Palazzo Pants',
                'category': 'Pants',
                'subcategory': 'Palazzo',
                'description': 'Beautiful floral print palazzo pants perfect for summer styling.',
                'short_description': 'Flowy palazzo pants with elegant floral print',
                'fabric': 'viscose',
                'occasion': 'casual',
                'mrp': Decimal('1299.00'),
                'selling_price': Decimal('999.00'),
                'stock_quantity': 30,
                'is_featured': True,
                'sizes': ['S', 'M', 'L', 'XL', 'XXL'],
                'colors': [('Blue', '#0000FF'), ('Pink', '#FFC0CB'), ('Green', '#008000')]
            },
            {
                'name': 'Silk Embroidered Dupatta',
                'category': 'Dupattas',
                'subcategory': 'Embroidered',
                'description': 'Luxurious silk dupatta with intricate embroidery work for special occasions.',
                'short_description': 'Premium silk dupatta with beautiful embroidery',
                'fabric': 'silk',
                'occasion': 'traditional',
                'mrp': Decimal('2499.00'),
                'selling_price': Decimal('1999.00'),
                'stock_quantity': 20,
                'is_featured': True,
                'sizes': ['One Size'],
                'colors': [('Gold', '#FFD700'), ('Silver', '#C0C0C0'), ('Red', '#FF0000')]
            },
            {
                'name': 'High Waist Jeggings',
                'category': 'Leggings',
                'subcategory': 'Jeggings',
                'description': 'Stylish jeggings with denim look and legging comfort.',
                'short_description': 'Comfortable jeggings with denim styling',
                'fabric': 'cotton_blend',
                'occasion': 'casual',
                'mrp': Decimal('799.00'),
                'selling_price': Decimal('599.00'),
                'stock_quantity': 40,
                'is_featured': False,
                'sizes': ['XS', 'S', 'M', 'L', 'XL'],
                'colors': [('Blue', '#0000FF'), ('Black', '#000000')]
            },
            {
                'name': 'Formal Office Trousers',
                'category': 'Pants',
                'subcategory': 'Formal',
                'description': 'Professional formal trousers perfect for office wear.',
                'short_description': 'Smart formal trousers for professional wear',
                'fabric': 'polyester',
                'occasion': 'formal',
                'mrp': Decimal('1599.00'),
                'selling_price': Decimal('1299.00'),
                'stock_quantity': 25,
                'is_featured': False,
                'sizes': ['S', 'M', 'L', 'XL'],
                'colors': [('Black', '#000000'), ('Navy', '#000080'), ('Grey', '#808080')]
            }
        ]
        
        for product_data in sample_products:
            category = Category.objects.get(name=product_data['category'])
            subcategory = SubCategory.objects.get(
                category=category, 
                name=product_data['subcategory']
            )
            
            product, created = Product.objects.get_or_create(
                name=product_data['name'],
                defaults={
                    'slug': product_data['name'].lower().replace(' ', '-'),
                    'category': category,
                    'subcategory': subcategory,
                    'description': product_data['description'],
                    'short_description': product_data['short_description'],
                    'fabric': product_data['fabric'],
                    'occasion': product_data['occasion'],
                    'mrp': product_data['mrp'],
                    'selling_price': product_data['selling_price'],
                    'stock_quantity': product_data['stock_quantity'],
                    'is_featured': product_data['is_featured'],
                    'care_instructions': 'Machine wash cold, tumble dry low',
                    'is_active': True
                }
            )
            
            if created:
                self.stdout.write(f'Created product: {product_data["name"]}')
                
                # Create product variants
                for size in product_data['sizes']:
                    for color_name, color_code in product_data['colors']:
                        ProductVariant.objects.create(
                            product=product,
                            size=size,
                            color=color_name,
                            color_code=color_code,
                            stock_quantity=10,
                            is_active=True
                        )
        
        self.stdout.write(f'Created {Product.objects.count()} products with variants')
