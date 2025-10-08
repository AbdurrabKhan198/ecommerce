from django.core.management.base import BaseCommand
from shop.models import Product, ProductVariant


class Command(BaseCommand):
    help = 'Create product variants with different sizes and colors'

    def handle(self, *args, **options):
        # Get all products
        products = Product.objects.all()
        
        if not products.exists():
            self.stdout.write(
                self.style.ERROR('No products found. Please run create_sample_products first.')
            )
            return

        # Color options with hex codes
        colors = [
            {'name': 'Black', 'code': '#000000'},
            {'name': 'White', 'code': '#FFFFFF'},
            {'name': 'Red', 'code': '#DC3545'},
            {'name': 'Blue', 'code': '#007BFF'},
            {'name': 'Green', 'code': '#28A745'},
            {'name': 'Pink', 'code': '#E91E63'},
            {'name': 'Purple', 'code': '#673AB7'},
            {'name': 'Orange', 'code': '#FF9800'},
            {'name': 'Brown', 'code': '#795548'},
            {'name': 'Navy', 'code': '#001F3F'},
            {'name': 'Grey', 'code': '#6C757D'},
            {'name': 'Yellow', 'code': '#FFC107'},
        ]

        # Size options
        sizes = ['XS', 'S', 'M', 'L', 'XL', 'XXL']

        created_count = 0
        
        for product in products:
            # Create variants for each product
            for size in sizes:
                # Select 2-4 random colors for each product
                import random
                product_colors = random.sample(colors, random.randint(2, 4))
                
                for color in product_colors:
                    variant, created = ProductVariant.objects.get_or_create(
                        product=product,
                        size=size,
                        color=color['name'],
                        defaults={
                            'color_code': color['code'],
                            'stock_quantity': random.randint(0, 50),
                            'additional_price': 0,
                            'is_active': True
                        }
                    )
                    
                    if created:
                        created_count += 1
                        self.stdout.write(
                            self.style.SUCCESS(f'Created variant: {product.name} - {size} - {color["name"]}')
                        )
                    else:
                        self.stdout.write(
                            self.style.WARNING(f'Variant already exists: {product.name} - {size} - {color["name"]}')
                        )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} product variants!')
        )
