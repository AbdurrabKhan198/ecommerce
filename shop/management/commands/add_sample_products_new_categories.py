from django.core.management.base import BaseCommand
from shop.models import Category, SubCategory, Product, ProductImage, ProductVariant
from decimal import Decimal


class Command(BaseCommand):
    help = 'Add sample products for new categories: Scarfs and Stoles'

    def handle(self, *args, **options):
        self.stdout.write('Adding sample products for Scarfs and Stoles...')
        
        try:
            # Get categories
            scarfs_category = Category.objects.get(name='Scarfs')
            stoles_category = Category.objects.get(name='Stoles')
            
            # Get subcategories
            georgette_subcat = SubCategory.objects.get(category=scarfs_category, name='Georgette')
            cotton_subcat = SubCategory.objects.get(category=scarfs_category, name='Cotton')
            plain_subcat = SubCategory.objects.get(category=stoles_category, name='Plain')
            fancy_subcat = SubCategory.objects.get(category=stoles_category, name='Fancy')
            
            # Sample Scarfs Products
            scarfs_products = [
                {
                    'name': 'Elegant Georgette Scarf - Floral Print',
                    'slug': 'elegant-georgette-scarf-floral-print',
                    'description': 'Beautiful georgette scarf with delicate floral print. Perfect for special occasions and formal wear. Luxurious feel and elegant drape.',
                    'short_description': 'Luxurious georgette scarf with floral print for special occasions.',
                    'fabric': 'georgette',
                    'occasion': 'party',
                    'care_instructions': 'Dry clean only. Iron on low heat.',
                    'mrp': Decimal('899.00'),
                    'selling_price': Decimal('599.00'),
                    'stock_quantity': 50,
                    'subcategory': georgette_subcat,
                    'variants': [
                        {'size': 'One Size', 'color': 'Pink', 'color_code': '#FFB6C1'},
                        {'size': 'One Size', 'color': 'Blue', 'color_code': '#87CEEB'},
                        {'size': 'One Size', 'color': 'Green', 'color_code': '#98FB98'},
                    ]
                },
                {
                    'name': 'Comfortable Cotton Scarf - Solid Color',
                    'slug': 'comfortable-cotton-scarf-solid-color',
                    'description': 'Soft and comfortable cotton scarf in solid colors. Perfect for daily wear, office, and casual outings. Easy to care for.',
                    'short_description': 'Soft cotton scarf in solid colors, perfect for daily wear.',
                    'fabric': 'cotton',
                    'occasion': 'casual',
                    'care_instructions': 'Machine wash cold. Tumble dry low.',
                    'mrp': Decimal('399.00'),
                    'selling_price': Decimal('299.00'),
                    'stock_quantity': 75,
                    'subcategory': cotton_subcat,
                    'variants': [
                        {'size': 'One Size', 'color': 'White', 'color_code': '#FFFFFF'},
                        {'size': 'One Size', 'color': 'Black', 'color_code': '#000000'},
                        {'size': 'One Size', 'color': 'Navy', 'color_code': '#000080'},
                    ]
                }
            ]
            
            # Sample Stoles Products
            stoles_products = [
                {
                    'name': 'Simple Plain Stole - Office Wear',
                    'slug': 'simple-plain-stole-office-wear',
                    'description': 'Simple and elegant plain stole perfect for office wear and daily use. Comfortable fabric with clean finish.',
                    'short_description': 'Simple plain stole perfect for office and daily wear.',
                    'fabric': 'cotton',
                    'occasion': 'work',
                    'care_instructions': 'Machine wash cold. Iron on medium heat.',
                    'mrp': Decimal('499.00'),
                    'selling_price': Decimal('349.00'),
                    'stock_quantity': 60,
                    'subcategory': plain_subcat,
                    'variants': [
                        {'size': 'One Size', 'color': 'Beige', 'color_code': '#F5F5DC'},
                        {'size': 'One Size', 'color': 'Grey', 'color_code': '#808080'},
                        {'size': 'One Size', 'color': 'Brown', 'color_code': '#8B4513'},
                    ]
                },
                {
                    'name': 'Fancy Embroidered Stole - Party Wear',
                    'slug': 'fancy-embroidered-stole-party-wear',
                    'description': 'Beautiful fancy stole with intricate embroidery work. Perfect for parties, weddings, and special occasions. Premium quality fabric.',
                    'short_description': 'Fancy embroidered stole perfect for parties and special occasions.',
                    'fabric': 'silk',
                    'occasion': 'party',
                    'care_instructions': 'Dry clean only. Store in cool, dry place.',
                    'mrp': Decimal('1299.00'),
                    'selling_price': Decimal('899.00'),
                    'stock_quantity': 30,
                    'subcategory': fancy_subcat,
                    'variants': [
                        {'size': 'One Size', 'color': 'Gold', 'color_code': '#FFD700'},
                        {'size': 'One Size', 'color': 'Maroon', 'color_code': '#800000'},
                        {'size': 'One Size', 'color': 'Purple', 'color_code': '#800080'},
                    ]
                }
            ]
            
            # Create products
            all_products = scarfs_products + stoles_products
            
            for product_data in all_products:
                product, created = Product.objects.get_or_create(
                    name=product_data['name'],
                    defaults={
                        'category': product_data['subcategory'].category,
                        'subcategory': product_data['subcategory'],
                        'slug': product_data['slug'],
                        'description': product_data['description'],
                        'short_description': product_data['short_description'],
                        'fabric': product_data['fabric'],
                        'occasion': product_data['occasion'],
                        'care_instructions': product_data['care_instructions'],
                        'mrp': product_data['mrp'],
                        'selling_price': product_data['selling_price'],
                        'stock_quantity': product_data['stock_quantity'],
                        'is_active': True,
                        'is_featured': True,
                        'meta_title': f"{product_data['name']} | King Dupatta House",
                        'meta_description': product_data['short_description']
                    }
                )
                
                if created:
                    self.stdout.write(self.style.SUCCESS(f'✅ Created product: {product_data["name"]}'))
                    
                    # Create variants
                    for variant_data in product_data['variants']:
                        ProductVariant.objects.create(
                            product=product,
                            size=variant_data['size'],
                            color=variant_data['color'],
                            color_code=variant_data['color_code'],
                            stock_quantity=product_data['stock_quantity'],
                            is_active=True
                        )
                    
                    # Note: Product images will be added through admin panel
                    # ProductImage.objects.create(
                    #     product=product,
                    #     image='products/placeholder-scarf.jpg',
                    #     alt_text=product_data['name'],
                    #     is_primary=True,
                    #     sort_order=1
                    # )
                else:
                    self.stdout.write(f'ℹ️  Product "{product_data["name"]}" already exists')
            
            self.stdout.write(self.style.SUCCESS('\n🎉 Successfully added sample products for new categories!'))
            self.stdout.write('\n📋 Summary:')
            self.stdout.write('• 2 Scarfs products (Georgette & Cotton)')
            self.stdout.write('• 2 Stoles products (Plain & Fancy)')
            self.stdout.write('• Each product has 3 color variants')
            self.stdout.write('• All products are featured and active')
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error: {str(e)}'))
            self.stdout.write('Make sure to run "python manage.py add_new_categories" first!')
