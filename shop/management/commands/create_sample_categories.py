from django.core.management.base import BaseCommand
from shop.models import Category, SubCategory


class Command(BaseCommand):
    help = 'Create sample categories for King Dupatta House'

    def handle(self, *args, **options):
        # Create main categories
        categories_data = [
            {
                'name': 'Leggings',
                'slug': 'leggings',
                'description': 'Comfort meets style in our premium leggings collection. Perfect for everyday wear with superior comfort and durability.',
                'sort_order': 1,
                'meta_title': 'Premium Leggings - King Dupatta House',
                'meta_description': 'Shop premium quality leggings at King Dupatta House. Comfortable, stylish, and perfect fit guaranteed.'
            },
            {
                'name': 'Pants',
                'slug': 'pants',
                'description': 'Versatile elegance for every occasion and style. From casual to formal, find your perfect fit.',
                'sort_order': 2,
                'meta_title': 'Stylish Pants - King Dupatta House',
                'meta_description': 'Discover our collection of stylish pants and trousers. Perfect for every occasion with premium quality fabrics.'
            },
            {
                'name': 'Dupattas',
                'slug': 'dupattas',
                'description': 'Traditional elegance redefined for modern women. Beautiful dupattas that complement your traditional and fusion wear.',
                'sort_order': 3,
                'meta_title': 'Beautiful Dupattas - King Dupatta House',
                'meta_description': 'Shop traditional and modern dupattas at King Dupatta House. Premium quality fabrics with beautiful designs.'
            }
        ]

        created_categories = []
        
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults=cat_data
            )
            if created:
                created_categories.append(category)
                self.stdout.write(
                    self.style.SUCCESS(f'Created category: {category.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Category already exists: {category.name}')
                )

        # Create subcategories for each main category
        subcategories_data = {
            'leggings': [
                {'name': 'Ankle Length', 'slug': 'ankle-length', 'description': 'Perfect ankle-length leggings for everyday comfort'},
                {'name': 'Full Length', 'slug': 'full-length', 'description': 'Full-length leggings for complete coverage'},
                {'name': 'Capri', 'slug': 'capri', 'description': 'Stylish capri leggings for a trendy look'},
            ],
            'pants': [
                {'name': 'Palazzo', 'slug': 'palazzo', 'description': 'Flowing palazzo pants for elegant comfort'},
                {'name': 'Straight Fit', 'slug': 'straight-fit', 'description': 'Classic straight-fit pants for formal occasions'},
                {'name': 'Tapered', 'slug': 'tapered', 'description': 'Modern tapered pants for a contemporary look'},
            ],
            'dupattas': [
                {'name': 'Silk', 'slug': 'silk', 'description': 'Luxurious silk dupattas for special occasions'},
                {'name': 'Cotton', 'slug': 'cotton', 'description': 'Comfortable cotton dupattas for daily wear'},
                {'name': 'Georgette', 'slug': 'georgette', 'description': 'Elegant georgette dupattas with beautiful drape'},
            ]
        }

        for category in created_categories:
            if category.slug in subcategories_data:
                for sub_data in subcategories_data[category.slug]:
                    subcategory, created = SubCategory.objects.get_or_create(
                        category=category,
                        slug=sub_data['slug'],
                        defaults={
                            'name': sub_data['name'],
                            'description': sub_data['description'],
                            'sort_order': subcategories_data[category.slug].index(sub_data) + 1
                        }
                    )
                    if created:
                        self.stdout.write(
                            self.style.SUCCESS(f'Created subcategory: {category.name} - {subcategory.name}')
                        )
                    else:
                        self.stdout.write(
                            self.style.WARNING(f'Subcategory already exists: {category.name} - {subcategory.name}')
                        )

        self.stdout.write(
            self.style.SUCCESS(f'\n✅ Successfully created {len(created_categories)} categories with subcategories!')
        )
        self.stdout.write(
            self.style.SUCCESS('You can now see these categories on your homepage and manage them from the Django admin panel.')
        )
