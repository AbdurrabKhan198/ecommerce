from django.core.management.base import BaseCommand
from shop.models import Category, SubCategory, Product, ProductVariant
from decimal import Decimal


class Command(BaseCommand):
    help = 'Set specific products as bestsellers in sorted order'

    def handle(self, *args, **options):
        self.stdout.write('Setting specific bestseller products in sorted order...')
        
        try:
            # Clear all current bestsellers
            Product.objects.update(is_bestseller=False)
            self.stdout.write('✅ Cleared all current bestsellers')
            
            # Get or create categories
            dupattas_category = Category.objects.get(name='Dupattas')
            leggings_category = Category.objects.get(name='Leggings')
            
            # Get subcategories
            fancy_subcat = SubCategory.objects.get(category=dupattas_category, name='Fancy Dupatta')
            customised_subcat = SubCategory.objects.get(category=dupattas_category, name='Customised Dupatta')
            ankle_subcat = SubCategory.objects.get(category=leggings_category, name='Ankle Length')
            
            # 1. Customised Dupatta (Already exists)
            customised_product = Product.objects.get(name='Customised Dupatta - Made to Order')
            customised_product.is_bestseller = True
            customised_product.save()
            self.stdout.write('✅ 1. Customised Dupatta - Made to Order (Bestseller)')
            
            # 2. Fancy Dupatta (Already exists)
            fancy_product = Product.objects.get(name='Fancy Embroidered Dupatta - Special Occasions')
            fancy_product.is_bestseller = True
            fancy_product.save()
            self.stdout.write('✅ 2. Fancy Embroidered Dupatta - Special Occasions (Bestseller)')
            
            # 3. White Heavy Fancy Dupatta (Create new)
            white_heavy_product, created = Product.objects.get_or_create(
                name='White Heavy Fancy Dupatta',
                defaults={
                    'category': dupattas_category,
                    'subcategory': fancy_subcat,
                    'slug': 'white-heavy-fancy-dupatta',
                    'description': 'Beautiful white heavy fancy dupatta with intricate embroidery and embellishments. Perfect for weddings, parties, and special occasions. Premium quality fabric with elegant finish.',
                    'short_description': 'White heavy fancy dupatta with embroidery for special occasions.',
                    'fabric': 'silk',
                    'occasion': 'party',
                    'care_instructions': 'Dry clean only. Store in cool, dry place.',
                    'mrp': Decimal('2499.00'),
                    'selling_price': Decimal('1799.00'),
                    'stock_quantity': 25,
                    'is_active': True,
                    'is_featured': True,
                    'is_bestseller': True,
                    'meta_title': 'White Heavy Fancy Dupatta | King Dupatta House',
                    'meta_description': 'Beautiful white heavy fancy dupatta with embroidery. Perfect for weddings and special occasions.'
                }
            )
            
            if created:
                # Create variants
                ProductVariant.objects.create(
                    product=white_heavy_product,
                    size='One Size',
                    color='White',
                    color_code='#FFFFFF',
                    stock_quantity=25,
                    is_active=True
                )
                self.stdout.write('✅ 3. White Heavy Fancy Dupatta (Created & Bestseller)')
            else:
                white_heavy_product.is_bestseller = True
                white_heavy_product.save()
                self.stdout.write('✅ 3. White Heavy Fancy Dupatta (Bestseller)')
            
            # 4. Lyra Leggings (Create new)
            lyra_leggings, created = Product.objects.get_or_create(
                name='Lyra Leggings',
                defaults={
                    'category': leggings_category,
                    'subcategory': ankle_subcat,
                    'slug': 'lyra-leggings',
                    'description': 'Comfortable and stylish Lyra leggings perfect for daily wear, gym, and casual outings. Made with premium cotton blend fabric for comfort and durability.',
                    'short_description': 'Comfortable Lyra leggings perfect for daily wear and gym.',
                    'fabric': 'cotton_blend',
                    'occasion': 'casual',
                    'care_instructions': 'Machine wash cold. Tumble dry low.',
                    'mrp': Decimal('899.00'),
                    'selling_price': Decimal('599.00'),
                    'stock_quantity': 50,
                    'is_active': True,
                    'is_featured': True,
                    'is_bestseller': True,
                    'meta_title': 'Lyra Leggings - Comfortable Daily Wear | King Dupatta House',
                    'meta_description': 'Comfortable Lyra leggings perfect for daily wear and gym. Premium cotton blend fabric.'
                }
            )
            
            if created:
                # Create variants
                variants = [
                    {'size': 'S', 'color': 'Black', 'color_code': '#000000'},
                    {'size': 'M', 'color': 'Black', 'color_code': '#000000'},
                    {'size': 'L', 'color': 'Black', 'color_code': '#000000'},
                    {'size': 'S', 'color': 'Navy', 'color_code': '#000080'},
                    {'size': 'M', 'color': 'Navy', 'color_code': '#000080'},
                    {'size': 'L', 'color': 'Navy', 'color_code': '#000080'},
                ]
                
                for variant_data in variants:
                    ProductVariant.objects.create(
                        product=lyra_leggings,
                        size=variant_data['size'],
                        color=variant_data['color'],
                        color_code=variant_data['color_code'],
                        stock_quantity=50,
                        is_active=True
                    )
                self.stdout.write('✅ 4. Lyra Leggings (Created & Bestseller)')
            else:
                lyra_leggings.is_bestseller = True
                lyra_leggings.save()
                self.stdout.write('✅ 4. Lyra Leggings (Bestseller)')
            
            # Verify the bestsellers
            bestsellers = Product.objects.filter(is_bestseller=True).order_by('name')
            self.stdout.write(self.style.SUCCESS('\n🎉 Bestseller Products Set Successfully!'))
            self.stdout.write('\n📋 Current Bestsellers (in order):')
            for i, product in enumerate(bestsellers, 1):
                self.stdout.write(f'{i}. {product.name} - ₹{product.selling_price}')
            
            self.stdout.write('\n💡 Visit http://127.0.0.1:8000/ to see the changes on homepage!')
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error: {str(e)}'))
