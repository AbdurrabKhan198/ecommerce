from django.core.management.base import BaseCommand
from shop.models import Category, SubCategory, Product, ProductVariant
from decimal import Decimal


class Command(BaseCommand):
    help = 'Add sample products for Dupattas subcategories'

    def handle(self, *args, **options):
        self.stdout.write('Adding sample products for Dupattas subcategories...')
        
        try:
            # Get Dupattas category
            dupattas_category = Category.objects.get(name='Dupattas')
            
            # Get subcategories
            cotton_plain = SubCategory.objects.get(category=dupattas_category, name='Cotton Plain Dupatta')
            cotton_printed = SubCategory.objects.get(category=dupattas_category, name='Cotton Printed Dupatta')
            banarasi = SubCategory.objects.get(category=dupattas_category, name='Banarasi Dupatta')
            chiffon = SubCategory.objects.get(category=dupattas_category, name='Chiffon Dupatta')
            fancy = SubCategory.objects.get(category=dupattas_category, name='Fancy Dupatta')
            red_bridal = SubCategory.objects.get(category=dupattas_category, name='Red Bridal Dupatta')
            customised = SubCategory.objects.get(category=dupattas_category, name='Customised Dupatta')
            
            # Sample Dupatta Products
            dupatta_products = [
                {
                    'name': 'Pure Cotton Plain Dupatta - Solid Colors',
                    'slug': 'pure-cotton-plain-dupatta-solid-colors',
                    'description': 'Soft and comfortable pure cotton dupatta in solid colors. Perfect for daily wear, office, and casual occasions. Easy to care for and maintain.',
                    'short_description': 'Soft cotton dupatta in solid colors, perfect for daily wear.',
                    'fabric': 'cotton',
                    'occasion': 'casual',
                    'care_instructions': 'Machine wash cold. Iron on medium heat.',
                    'mrp': Decimal('599.00'),
                    'selling_price': Decimal('399.00'),
                    'stock_quantity': 100,
                    'subcategory': cotton_plain,
                    'variants': [
                        {'size': 'One Size', 'color': 'White', 'color_code': '#FFFFFF'},
                        {'size': 'One Size', 'color': 'Pink', 'color_code': '#FFB6C1'},
                        {'size': 'One Size', 'color': 'Blue', 'color_code': '#87CEEB'},
                        {'size': 'One Size', 'color': 'Green', 'color_code': '#98FB98'},
                    ]
                },
                {
                    'name': 'Cotton Printed Dupatta - Floral Design',
                    'slug': 'cotton-printed-dupatta-floral-design',
                    'description': 'Beautiful cotton dupatta with delicate floral prints. Perfect for casual and semi-formal occasions. Comfortable fabric with attractive patterns.',
                    'short_description': 'Cotton dupatta with floral prints, perfect for casual wear.',
                    'fabric': 'cotton',
                    'occasion': 'casual',
                    'care_instructions': 'Machine wash cold. Iron on low heat.',
                    'mrp': Decimal('799.00'),
                    'selling_price': Decimal('549.00'),
                    'stock_quantity': 80,
                    'subcategory': cotton_printed,
                    'variants': [
                        {'size': 'One Size', 'color': 'Pink Floral', 'color_code': '#FFB6C1'},
                        {'size': 'One Size', 'color': 'Blue Floral', 'color_code': '#87CEEB'},
                        {'size': 'One Size', 'color': 'Green Floral', 'color_code': '#98FB98'},
                    ]
                },
                {
                    'name': 'Luxury Banarasi Dupatta - Zari Work',
                    'slug': 'luxury-banarasi-dupatta-zari-work',
                    'description': 'Exquisite Banarasi dupatta with intricate zari work and traditional patterns. Perfect for weddings, festivals, and special occasions. Premium quality fabric.',
                    'short_description': 'Luxury Banarasi dupatta with zari work for special occasions.',
                    'fabric': 'silk',
                    'occasion': 'traditional',
                    'care_instructions': 'Dry clean only. Store in cool, dry place.',
                    'mrp': Decimal('2999.00'),
                    'selling_price': Decimal('1999.00'),
                    'stock_quantity': 25,
                    'subcategory': banarasi,
                    'variants': [
                        {'size': 'One Size', 'color': 'Gold', 'color_code': '#FFD700'},
                        {'size': 'One Size', 'color': 'Maroon', 'color_code': '#800000'},
                        {'size': 'One Size', 'color': 'Purple', 'color_code': '#800080'},
                    ]
                },
                {
                    'name': 'Elegant Chiffon Dupatta - Party Wear',
                    'slug': 'elegant-chiffon-dupatta-party-wear',
                    'description': 'Beautiful chiffon dupatta with elegant drape and flow. Perfect for parties, formal occasions, and special events. Luxurious feel and graceful appearance.',
                    'short_description': 'Elegant chiffon dupatta perfect for parties and formal wear.',
                    'fabric': 'chiffon',
                    'occasion': 'party',
                    'care_instructions': 'Dry clean only. Iron on low heat.',
                    'mrp': Decimal('1299.00'),
                    'selling_price': Decimal('899.00'),
                    'stock_quantity': 50,
                    'subcategory': chiffon,
                    'variants': [
                        {'size': 'One Size', 'color': 'Black', 'color_code': '#000000'},
                        {'size': 'One Size', 'color': 'Navy', 'color_code': '#000080'},
                        {'size': 'One Size', 'color': 'Burgundy', 'color_code': '#800020'},
                    ]
                },
                {
                    'name': 'Fancy Embroidered Dupatta - Special Occasions',
                    'slug': 'fancy-embroidered-dupatta-special-occasions',
                    'description': 'Stylish fancy dupatta with beautiful embroidery and embellishments. Perfect for parties, celebrations, and special occasions. Eye-catching designs.',
                    'short_description': 'Fancy embroidered dupatta perfect for special occasions.',
                    'fabric': 'silk',
                    'occasion': 'party',
                    'care_instructions': 'Dry clean only. Store carefully.',
                    'mrp': Decimal('1999.00'),
                    'selling_price': Decimal('1299.00'),
                    'stock_quantity': 35,
                    'subcategory': fancy,
                    'variants': [
                        {'size': 'One Size', 'color': 'Gold Embroidered', 'color_code': '#FFD700'},
                        {'size': 'One Size', 'color': 'Silver Embroidered', 'color_code': '#C0C0C0'},
                        {'size': 'One Size', 'color': 'Multi Color', 'color_code': '#FF6B6B'},
                    ]
                },
                {
                    'name': 'Traditional Red Bridal Dupatta - Wedding',
                    'slug': 'traditional-red-bridal-dupatta-wedding',
                    'description': 'Traditional red bridal dupatta perfect for weddings and bridal ceremonies. Rich red fabric with traditional designs and embellishments. Made for special moments.',
                    'short_description': 'Traditional red bridal dupatta for weddings and ceremonies.',
                    'fabric': 'silk',
                    'occasion': 'traditional',
                    'care_instructions': 'Dry clean only. Handle with care.',
                    'mrp': Decimal('3999.00'),
                    'selling_price': Decimal('2499.00'),
                    'stock_quantity': 20,
                    'subcategory': red_bridal,
                    'variants': [
                        {'size': 'One Size', 'color': 'Deep Red', 'color_code': '#8B0000'},
                        {'size': 'One Size', 'color': 'Bright Red', 'color_code': '#FF0000'},
                        {'size': 'One Size', 'color': 'Maroon Red', 'color_code': '#800000'},
                    ]
                },
                {
                    'name': 'Customised Dupatta - Made to Order',
                    'slug': 'customised-dupatta-made-to-order',
                    'description': 'Customized dupatta made to your specifications. Choose your fabric, color, design, and get a unique dupatta tailored just for you. Perfect for special requirements.',
                    'short_description': 'Customised dupatta made to your specifications and requirements.',
                    'fabric': 'custom',
                    'occasion': 'custom',
                    'care_instructions': 'As per fabric type. Contact for specific care instructions.',
                    'mrp': Decimal('1999.00'),
                    'selling_price': Decimal('1499.00'),
                    'stock_quantity': 10,
                    'subcategory': customised,
                    'variants': [
                        {'size': 'One Size', 'color': 'Custom Color', 'color_code': '#FF6B6B'},
                        {'size': 'One Size', 'color': 'Custom Design', 'color_code': '#4ECDC4'},
                        {'size': 'One Size', 'color': 'Custom Fabric', 'color_code': '#45B7D1'},
                    ]
                }
            ]
            
            # Create products
            created_count = 0
            for product_data in dupatta_products:
                product, created = Product.objects.get_or_create(
                    name=product_data['name'],
                    defaults={
                        'category': dupattas_category,
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
                    created_count += 1
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
                else:
                    self.stdout.write(f'ℹ️  Product "{product_data["name"]}" already exists')
            
            self.stdout.write(self.style.SUCCESS(f'\n🎉 Successfully added {created_count} Dupatta products!'))
            self.stdout.write('\n📋 Dupatta Products Added:')
            for product_data in dupatta_products:
                self.stdout.write(f'• {product_data["name"]} - ₹{product_data["selling_price"]}')
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error: {str(e)}'))
            self.stdout.write('Make sure to run "python manage.py add_dupatta_subcategories" first!')
