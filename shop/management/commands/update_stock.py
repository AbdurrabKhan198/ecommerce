from django.core.management.base import BaseCommand
from shop.models import Product, ProductVariant


class Command(BaseCommand):
    help = 'Update stock quantities for products and variants'

    def handle(self, *args, **options):
        # Update product stock quantities
        products_updated = 0
        for product in Product.objects.all():
            product.stock_quantity = 50
            product.save()
            products_updated += 1
            self.stdout.write(f'Updated {product.name} stock to 50')

        # Update variant stock quantities  
        variants_updated = 0
        for variant in ProductVariant.objects.all():
            variant.stock_quantity = 25
            variant.save()
            variants_updated += 1
            self.stdout.write(f'Updated variant {variant.color} {variant.size} stock to 25')

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully updated {products_updated} products and {variants_updated} variants!'
            )
        )
