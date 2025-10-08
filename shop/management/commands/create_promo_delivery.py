from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from shop.models import PromoCode, DeliveryOption


class Command(BaseCommand):
    help = 'Create sample promo codes and delivery options'

    def handle(self, *args, **options):
        # Create promo codes
        promo_codes = [
            {
                'code': 'WELCOME10',
                'description': '10% off for new customers',
                'discount_type': 'percentage',
                'discount_value': 10,
                'min_order_amount': 500,
                'max_discount': 200,
                'usage_limit': 100,
                'valid_from': timezone.now(),
                'valid_until': timezone.now() + timedelta(days=30)
            },
            {
                'code': 'SAVE20',
                'description': '20% off on orders above ₹1000',
                'discount_type': 'percentage',
                'discount_value': 20,
                'min_order_amount': 1000,
                'max_discount': 500,
                'usage_limit': 50,
                'valid_from': timezone.now(),
                'valid_until': timezone.now() + timedelta(days=15)
            },
            {
                'code': 'FLAT100',
                'description': '₹100 off on orders above ₹800',
                'discount_type': 'fixed',
                'discount_value': 100,
                'min_order_amount': 800,
                'usage_limit': 200,
                'valid_from': timezone.now(),
                'valid_until': timezone.now() + timedelta(days=45)
            },
            {
                'code': 'FIRST50',
                'description': '₹50 off for first order',
                'discount_type': 'fixed',
                'discount_value': 50,
                'min_order_amount': 300,
                'usage_limit': 500,
                'valid_from': timezone.now(),
                'valid_until': timezone.now() + timedelta(days=60)
            }
        ]

        for promo_data in promo_codes:
            promo, created = PromoCode.objects.get_or_create(
                code=promo_data['code'],
                defaults=promo_data
            )
            if created:
                self.stdout.write(f'Created promo code: {promo.code}')
            else:
                self.stdout.write(f'Promo code already exists: {promo.code}')

        # Create delivery options
        delivery_options = [
            {
                'name': 'Standard Delivery',
                'description': 'Regular delivery service',
                'price': 0,
                'estimated_days': '3-5 days',
                'sort_order': 1
            },
            {
                'name': 'Express Delivery',
                'description': 'Fast delivery service',
                'price': 50,
                'estimated_days': '1-2 days',
                'sort_order': 2
            },
            {
                'name': 'Same Day Delivery',
                'description': 'Delivery on the same day',
                'price': 100,
                'estimated_days': 'Same day',
                'sort_order': 3
            },
            {
                'name': 'Premium Delivery',
                'description': 'Premium service with tracking',
                'price': 150,
                'estimated_days': '2-3 days',
                'sort_order': 4
            }
        ]

        for delivery_data in delivery_options:
            delivery, created = DeliveryOption.objects.get_or_create(
                name=delivery_data['name'],
                defaults=delivery_data
            )
            if created:
                self.stdout.write(f'Created delivery option: {delivery.name}')
            else:
                self.stdout.write(f'Delivery option already exists: {delivery.name}')

        self.stdout.write(
            self.style.SUCCESS(
                'Successfully created promo codes and delivery options!'
            )
        )
