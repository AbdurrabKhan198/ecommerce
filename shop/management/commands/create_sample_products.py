from django.core.management.base import BaseCommand
from shop.models import Category, SubCategory, Product, ProductImage, ProductVariant
from decimal import Decimal


class Command(BaseCommand):
    help = 'Create sample products for King Dupatta House'

    def handle(self, *args, **options):
        # Get categories and subcategories
        try:
            leggings_category = Category.objects.get(slug='leggings')
            pants_category = Category.objects.get(slug='pants')
            dupattas_category = Category.objects.get(slug='dupattas')
        except Category.DoesNotExist:
            self.stdout.write(
                self.style.ERROR('Categories not found. Please run create_sample_categories first.')
            )
            return

        # Get subcategories
        ankle_length = SubCategory.objects.get(slug='ankle-length')
        full_length = SubCategory.objects.get(slug='full-length')
        capri = SubCategory.objects.get(slug='capri')
        palazzo = SubCategory.objects.get(slug='palazzo')
        straight_fit = SubCategory.objects.get(slug='straight-fit')
        tapered = SubCategory.objects.get(slug='tapered')
        silk = SubCategory.objects.get(slug='silk')
        cotton = SubCategory.objects.get(slug='cotton')
        georgette = SubCategory.objects.get(slug='georgette')

        # Sample products data
        products_data = [
            # Leggings
            {
                'name': 'Premium Cotton Ankle Length Leggings',
                'category': leggings_category,
                'subcategory': ankle_length,
                'description': 'Super comfortable ankle length leggings made from premium cotton blend. Perfect for everyday wear with excellent stretch and durability.',
                'short_description': 'Comfortable ankle length leggings in premium cotton blend',
                'fabric': 'cotton',
                'occasion': 'casual',
                'care_instructions': 'Machine wash cold, tumble dry low, do not bleach',
                'mrp': Decimal('899.00'),
                'selling_price': Decimal('599.00'),
                'stock_quantity': 50,
                'is_featured': True,
                'meta_title': 'Premium Cotton Ankle Length Leggings - King Dupatta House',
                'meta_description': 'Shop premium cotton ankle length leggings at King Dupatta House. Comfortable, durable, and perfect for everyday wear.',
            },
            {
                'name': 'Full Length Stretch Leggings',
                'category': leggings_category,
                'subcategory': full_length,
                'description': 'Full length leggings with excellent stretch and comfort. Made from high-quality fabric that maintains its shape wash after wash.',
                'short_description': 'Full length leggings with excellent stretch and comfort',
                'fabric': 'cotton_blend',
                'occasion': 'casual',
                'care_instructions': 'Machine wash cold, do not bleach, iron on low heat',
                'mrp': Decimal('799.00'),
                'selling_price': Decimal('549.00'),
                'stock_quantity': 35,
                'is_featured': True,
            },
            {
                'name': 'Capri Length Cotton Leggings',
                'category': leggings_category,
                'subcategory': capri,
                'description': 'Stylish capri length leggings perfect for summer wear. Lightweight and breathable cotton fabric.',
                'short_description': 'Stylish capri length leggings for summer',
                'fabric': 'cotton',
                'occasion': 'casual',
                'care_instructions': 'Machine wash cold, air dry',
                'mrp': Decimal('699.00'),
                'selling_price': Decimal('449.00'),
                'stock_quantity': 25,
            },
            
            # Pants
            {
                'name': 'Elegant Palazzo Pants Set',
                'category': pants_category,
                'subcategory': palazzo,
                'description': 'Beautiful palazzo pants set with matching top. Perfect for parties and special occasions. Premium fabric with elegant drape.',
                'short_description': 'Elegant palazzo pants set for special occasions',
                'fabric': 'silk',
                'occasion': 'party',
                'care_instructions': 'Dry clean only',
                'mrp': Decimal('1599.00'),
                'selling_price': Decimal('1299.00'),
                'stock_quantity': 20,
                'is_featured': True,
            },
            {
                'name': 'Professional Straight Fit Pants',
                'category': pants_category,
                'subcategory': straight_fit,
                'description': 'Professional straight fit pants perfect for office wear. Comfortable and stylish with a perfect fit.',
                'short_description': 'Professional straight fit pants for office wear',
                'fabric': 'polyester',
                'occasion': 'work',
                'care_instructions': 'Machine wash cold, tumble dry low',
                'mrp': Decimal('1199.00'),
                'selling_price': Decimal('899.00'),
                'stock_quantity': 30,
            },
            {
                'name': 'Modern Tapered Pants',
                'category': pants_category,
                'subcategory': tapered,
                'description': 'Modern tapered pants with contemporary styling. Perfect for casual and semi-formal occasions.',
                'short_description': 'Modern tapered pants with contemporary styling',
                'fabric': 'cotton_blend',
                'occasion': 'casual',
                'care_instructions': 'Machine wash cold, tumble dry low',
                'mrp': Decimal('999.00'),
                'selling_price': Decimal('749.00'),
                'stock_quantity': 40,
            },
            
            # Dupattas
            {
                'name': 'Luxurious Silk Dupatta',
                'category': dupattas_category,
                'subcategory': silk,
                'description': 'Beautiful silk dupatta with intricate work. Perfect for traditional occasions and festivals.',
                'short_description': 'Luxurious silk dupatta with intricate work',
                'fabric': 'silk',
                'occasion': 'traditional',
                'care_instructions': 'Dry clean only',
                'mrp': Decimal('999.00'),
                'selling_price': Decimal('799.00'),
                'stock_quantity': 15,
                'is_featured': True,
            },
            {
                'name': 'Cotton Printed Dupatta',
                'category': dupattas_category,
                'subcategory': cotton,
                'description': 'Comfortable cotton dupatta with beautiful prints. Perfect for daily wear and casual occasions.',
                'short_description': 'Comfortable cotton dupatta with beautiful prints',
                'fabric': 'cotton',
                'occasion': 'casual',
                'care_instructions': 'Machine wash cold, air dry',
                'mrp': Decimal('599.00'),
                'selling_price': Decimal('399.00'),
                'stock_quantity': 45,
            },
            {
                'name': 'Elegant Georgette Dupatta',
                'category': dupattas_category,
                'subcategory': georgette,
                'description': 'Elegant georgette dupatta with beautiful drape. Perfect for parties and special events.',
                'short_description': 'Elegant georgette dupatta with beautiful drape',
                'fabric': 'viscose',
                'occasion': 'party',
                'care_instructions': 'Dry clean only',
                'mrp': Decimal('799.00'),
                'selling_price': Decimal('599.00'),
                'stock_quantity': 25,
            },
        ]

        created_products = []
        
        for product_data in products_data:
            product, created = Product.objects.get_or_create(
                slug=product_data['name'].lower().replace(' ', '-').replace(',', ''),
                defaults=product_data
            )
            if created:
                created_products.append(product)
                self.stdout.write(
                    self.style.SUCCESS(f'Created product: {product.name}')
                )
                
                # Create product variants
                sizes = ['S', 'M', 'L', 'XL']
                colors = ['Black', 'White', 'Navy', 'Red', 'Pink']
                
                for size in sizes:
                    for color in colors[:3]:  # Limit to 3 colors per product
                        ProductVariant.objects.create(
                            product=product,
                            size=size,
                            color=color,
                            color_code='#000000' if color == 'Black' else '#FFFFFF' if color == 'White' else '#000080',
                            stock_quantity=10,
                            additional_price=Decimal('0.00')
                        )
                
                self.stdout.write(
                    self.style.SUCCESS(f'  → Created variants for {product.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Product already exists: {product.name}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'\n✅ Successfully created {len(created_products)} products with variants!')
        )
        self.stdout.write(
            self.style.SUCCESS('You can now manage these products from the Django admin panel.')
        )
        self.stdout.write(
            self.style.SUCCESS('Products will automatically appear on your website categories and subcategories.')
        )
