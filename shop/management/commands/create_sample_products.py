from django.core.management.base import BaseCommand
from shop.models import Category, SubCategory, Product, ProductImage
from decimal import Decimal
import random


class Command(BaseCommand):
    help = 'Create sample products for testing shop functionality'

    def handle(self, *args, **options):
        # Get categories and subcategories
        try:
            leggings_category = Category.objects.get(slug='leggings')
            pants_category = Category.objects.get(slug='pants-trousers')
            dupattas_category = Category.objects.get(slug='dupattas')
        except Category.DoesNotExist:
            self.stdout.write(
                self.style.ERROR('Categories not found. Please run create_navbar_categories first.')
            )
            return

        # Sample products data
        products_data = [
            # Leggings
            {
                'name': 'Premium Cotton Leggings',
                'category': leggings_category,
                'subcategory': SubCategory.objects.get(slug='cotton-leggings'),
                'fabric': 'cotton',
                'occasion': 'casual',
                'mrp': Decimal('899.00'),
                'selling_price': Decimal('599.00'),
                'description': 'Comfortable and stylish cotton leggings perfect for everyday wear.',
                'short_description': 'Premium cotton leggings with perfect fit',
                'care_instructions': 'Machine wash cold, tumble dry low',
                'is_featured': True,
                'is_bestseller': True,
            },
            {
                'name': 'Printed Churidar Leggings',
                'category': leggings_category,
                'subcategory': SubCategory.objects.get(slug='churidar-leggings'),
                'fabric': 'cotton',
                'occasion': 'traditional',
                'mrp': Decimal('1299.00'),
                'selling_price': Decimal('999.00'),
                'description': 'Beautiful printed churidar leggings with traditional patterns.',
                'short_description': 'Traditional printed churidar leggings',
                'care_instructions': 'Hand wash recommended, air dry',
                'is_featured': True,
                'is_bestseller': False,
            },
            {
                'name': 'Solid Color Jeggings',
                'category': leggings_category,
                'subcategory': SubCategory.objects.get(slug='jeggings'),
                'fabric': 'cotton_blend',
                'occasion': 'casual',
                'mrp': Decimal('799.00'),
                'selling_price': Decimal('599.00'),
                'description': 'Versatile jeggings that combine comfort with style.',
                'short_description': 'Comfortable jeggings for everyday wear',
                'care_instructions': 'Machine wash cold, do not bleach',
                'is_featured': False,
                'is_bestseller': True,
            },
            
            # Pants
            {
                'name': 'Elegant Palazzo Pants',
                'category': pants_category,
                'subcategory': SubCategory.objects.get(slug='palazzo-pants'),
                'fabric': 'viscose',
                'occasion': 'party',
                'mrp': Decimal('1599.00'),
                'selling_price': Decimal('1299.00'),
                'description': 'Flowing palazzo pants perfect for parties and special occasions.',
                'short_description': 'Elegant palazzo pants for special events',
                'care_instructions': 'Dry clean recommended',
                'is_featured': True,
                'is_bestseller': True,
            },
            {
                'name': 'Formal Trousers',
                'category': pants_category,
                'subcategory': SubCategory.objects.get(slug='formal-trousers'),
                'fabric': 'polyester',
                'occasion': 'formal',
                'mrp': Decimal('1199.00'),
                'selling_price': Decimal('899.00'),
                'description': 'Professional formal trousers for office and business wear.',
                'short_description': 'Professional formal trousers',
                'care_instructions': 'Machine wash cold, iron on low heat',
                'is_featured': False,
                'is_bestseller': False,
            },
            {
                'name': 'Wide Leg Cigarette Pants',
                'category': pants_category,
                'subcategory': SubCategory.objects.get(slug='cigarette-pants'),
                'fabric': 'cotton',
                'occasion': 'casual',
                'mrp': Decimal('999.00'),
                'selling_price': Decimal('749.00'),
                'description': 'Trendy cigarette pants with wide leg design.',
                'short_description': 'Trendy wide leg cigarette pants',
                'care_instructions': 'Machine wash cold, tumble dry low',
                'is_featured': True,
                'is_bestseller': False,
            },
            
            # Dupattas
            {
                'name': 'Silk Dupatta with Embroidery',
                'category': dupattas_category,
                'subcategory': SubCategory.objects.get(slug='silk-dupattas'),
                'fabric': 'silk',
                'occasion': 'traditional',
                'mrp': Decimal('1999.00'),
                'selling_price': Decimal('1499.00'),
                'description': 'Luxurious silk dupatta with intricate embroidery work.',
                'short_description': 'Luxurious silk dupatta with embroidery',
                'care_instructions': 'Dry clean only',
                'is_featured': True,
                'is_bestseller': True,
            },
            {
                'name': 'Cotton Printed Dupatta',
                'category': dupattas_category,
                'subcategory': SubCategory.objects.get(slug='cotton-dupattas'),
                'fabric': 'cotton',
                'occasion': 'casual',
                'mrp': Decimal('599.00'),
                'selling_price': Decimal('399.00'),
                'description': 'Comfortable cotton dupatta with beautiful prints.',
                'short_description': 'Comfortable cotton printed dupatta',
                'care_instructions': 'Machine wash cold, air dry',
                'is_featured': False,
                'is_bestseller': True,
            },
            {
                'name': 'Net Dupatta with Sequins',
                'category': dupattas_category,
                'subcategory': SubCategory.objects.get(slug='net-dupattas'),
                'fabric': 'net',
                'occasion': 'party',
                'mrp': Decimal('899.00'),
                'selling_price': Decimal('699.00'),
                'description': 'Stylish net dupatta with sequin work for parties.',
                'short_description': 'Stylish net dupatta with sequins',
                'care_instructions': 'Hand wash, air dry',
                'is_featured': True,
                'is_bestseller': False,
            },
        ]

        # Create products
        created_count = 0
        for product_data in products_data:
            product, created = Product.objects.get_or_create(
                name=product_data['name'],
                defaults={
                    'category': product_data['category'],
                    'subcategory': product_data['subcategory'],
                    'fabric': product_data['fabric'],
                    'occasion': product_data['occasion'],
                    'mrp': product_data['mrp'],
                    'selling_price': product_data['selling_price'],
                    'description': product_data['description'],
                    'short_description': product_data['short_description'],
                    'care_instructions': product_data['care_instructions'],
                    'is_featured': product_data['is_featured'],
                    'is_bestseller': product_data['is_bestseller'],
                    'is_active': True,
                    'slug': product_data['name'].lower().replace(' ', '-').replace(',', ''),
                }
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created product: {product.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Product already exists: {product.name}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} sample products!')
        )