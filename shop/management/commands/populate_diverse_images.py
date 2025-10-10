from django.core.management.base import BaseCommand
from django.core.files import File
from shop.models import Product, ProductImage, Category, SubCategory
import requests
import os
from io import BytesIO
from PIL import Image as PILImage


class Command(BaseCommand):
    help = 'Populate database with diverse sample images for products'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=20,
            help='Number of products to add images to (default: 20)'
        )

    def handle(self, *args, **options):
        count = options['count']
        
        # Diverse Unsplash image URLs for women's fashion
        image_urls = [
            # Leggings
            'https://images.unsplash.com/photo-1594633312681-425c7b97ccd1?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
            'https://images.unsplash.com/photo-1551698618-1dfe5d97d256?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
            'https://images.unsplash.com/photo-1583391733956-6c78276477e3?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
            'https://images.unsplash.com/photo-1445205170230-053b83016050?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
            'https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
            'https://images.unsplash.com/photo-1571513723812-70c0a0a6b4b0?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
            
            # Pants
            'https://images.unsplash.com/photo-1594633312681-425c7b97ccd1?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
            'https://images.unsplash.com/photo-1551698618-1dfe5d97d256?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
            'https://images.unsplash.com/photo-1583391733956-6c78276477e3?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
            'https://images.unsplash.com/photo-1445205170230-053b83016050?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
            'https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
            'https://images.unsplash.com/photo-1571513723812-70c0a0a6b4b0?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
            
            # Dupattas
            'https://images.unsplash.com/photo-1594633312681-425c7b97ccd1?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
            'https://images.unsplash.com/photo-1551698618-1dfe5d97d256?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
            'https://images.unsplash.com/photo-1583391733956-6c78276477e3?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
            'https://images.unsplash.com/photo-1445205170230-053b83016050?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
            'https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
            'https://images.unsplash.com/photo-1571513723812-70c0a0a6b4b0?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
            
            # Additional diverse images
            'https://images.unsplash.com/photo-1594633312681-425c7b97ccd1?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
            'https://images.unsplash.com/photo-1551698618-1dfe5d97d256?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
            'https://images.unsplash.com/photo-1583391733956-6c78276477e3?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
            'https://images.unsplash.com/photo-1445205170230-053b83016050?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
            'https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
            'https://images.unsplash.com/photo-1571513723812-70c0a0a6b4b0?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
        ]

        products = Product.objects.filter(is_active=True)[:count]
        
        if not products.exists():
            self.stdout.write(
                self.style.WARNING('No active products found. Please create products first.')
            )
            return

        self.stdout.write(f'Adding diverse images to {products.count()} products...')

        for i, product in enumerate(products):
            try:
                # Clear existing images
                product.images.all().delete()
                
                # Add 2-4 images per product
                num_images = min(4, len(image_urls) - i * 2)
                start_idx = (i * 2) % len(image_urls)
                
                for j in range(num_images):
                    image_url = image_urls[(start_idx + j) % len(image_urls)]
                    
                    try:
                        # Download image
                        response = requests.get(image_url, timeout=10)
                        response.raise_for_status()
                        
                        # Create image file
                        image_file = BytesIO(response.content)
                        
                        # Create ProductImage instance
                        product_image = ProductImage.objects.create(
                            product=product,
                            is_primary=(j == 0)  # First image is primary
                        )
                        
                        # Save image file
                        product_image.image.save(
                            f'{product.slug}_image_{j+1}.jpg',
                            File(image_file),
                            save=True
                        )
                        
                        self.stdout.write(f'  ✓ Added image {j+1} to {product.name}')
                        
                    except Exception as e:
                        self.stdout.write(
                            self.style.WARNING(f'  ⚠ Failed to add image {j+1} to {product.name}: {str(e)}')
                        )
                        continue
                
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Updated images for {product.name}')
                )
                
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'✗ Failed to update {product.name}: {str(e)}')
                )
                continue

        self.stdout.write(
            self.style.SUCCESS(f'Successfully updated images for {products.count()} products!')
        )

