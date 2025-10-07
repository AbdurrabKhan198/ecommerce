from django.core.management.base import BaseCommand
from shop.models import Product


class Command(BaseCommand):
    help = 'Manage bestseller products for King Dupatta House'

    def add_arguments(self, parser):
        parser.add_argument(
            '--action',
            type=str,
            choices=['list', 'add', 'remove', 'clear'],
            default='list',
            help='Action to perform: list, add, remove, or clear bestsellers'
        )
        parser.add_argument(
            '--product-id',
            type=int,
            help='Product ID to add or remove from bestsellers'
        )
        parser.add_argument(
            '--product-name',
            type=str,
            help='Product name to add or remove from bestsellers'
        )

    def handle(self, *args, **options):
        action = options['action']
        product_id = options.get('product_id')
        product_name = options.get('product_name')

        if action == 'list':
            self.list_bestsellers()
        elif action == 'add':
            self.add_bestseller(product_id, product_name)
        elif action == 'remove':
            self.remove_bestseller(product_id, product_name)
        elif action == 'clear':
            self.clear_bestsellers()

    def list_bestsellers(self):
        """List all current bestseller products"""
        bestsellers = Product.objects.filter(is_bestseller=True, is_active=True)
        
        if bestsellers:
            self.stdout.write(self.style.SUCCESS(f'Found {bestsellers.count()} bestseller products:'))
            for product in bestsellers:
                self.stdout.write(f'  • {product.name} (ID: {product.id}) - ₹{product.selling_price}')
        else:
            self.stdout.write(self.style.WARNING('No bestseller products found.'))

    def add_bestseller(self, product_id, product_name):
        """Add a product to bestsellers"""
        if not product_id and not product_name:
            self.stdout.write(self.style.ERROR('Please provide either --product-id or --product-name'))
            return

        try:
            if product_id:
                product = Product.objects.get(id=product_id, is_active=True)
            else:
                product = Product.objects.get(name__icontains=product_name, is_active=True)
            
            if product.is_bestseller:
                self.stdout.write(self.style.WARNING(f'Product "{product.name}" is already a bestseller.'))
            else:
                product.is_bestseller = True
                product.save()
                self.stdout.write(self.style.SUCCESS(f'Added "{product.name}" to bestsellers.'))
                
        except Product.DoesNotExist:
            self.stdout.write(self.style.ERROR('Product not found.'))
        except Product.MultipleObjectsReturned:
            self.stdout.write(self.style.ERROR('Multiple products found. Please use --product-id instead.'))

    def remove_bestseller(self, product_id, product_name):
        """Remove a product from bestsellers"""
        if not product_id and not product_name:
            self.stdout.write(self.style.ERROR('Please provide either --product-id or --product-name'))
            return

        try:
            if product_id:
                product = Product.objects.get(id=product_id)
            else:
                product = Product.objects.get(name__icontains=product_name)
            
            if not product.is_bestseller:
                self.stdout.write(self.style.WARNING(f'Product "{product.name}" is not a bestseller.'))
            else:
                product.is_bestseller = False
                product.save()
                self.stdout.write(self.style.SUCCESS(f'Removed "{product.name}" from bestsellers.'))
                
        except Product.DoesNotExist:
            self.stdout.write(self.style.ERROR('Product not found.'))
        except Product.MultipleObjectsReturned:
            self.stdout.write(self.style.ERROR('Multiple products found. Please use --product-id instead.'))

    def clear_bestsellers(self):
        """Clear all bestsellers"""
        count = Product.objects.filter(is_bestseller=True).count()
        Product.objects.filter(is_bestseller=True).update(is_bestseller=False)
        self.stdout.write(self.style.SUCCESS(f'Cleared {count} bestseller products.'))


# Usage examples:
# python manage.py manage_bestsellers --action list
# python manage.py manage_bestsellers --action add --product-name "Premium Cotton"
# python manage.py manage_bestsellers --action remove --product-id 1
# python manage.py manage_bestsellers --action clear
