from django.core.management.base import BaseCommand
from shop.models import Category, SubCategory


class Command(BaseCommand):
    help = 'Create sample categories and subcategories for navbar testing'

    def handle(self, *args, **options):
        # Create main categories
        categories_data = [
            {
                'name': 'Leggings',
                'slug': 'leggings',
                'description': 'Comfortable and stylish leggings for every occasion',
                'sort_order': 1
            },
            {
                'name': 'Pants & Trousers',
                'slug': 'pants-trousers',
                'description': 'Elegant pants and trousers for modern women',
                'sort_order': 2
            },
            {
                'name': 'Dupattas',
                'slug': 'dupattas',
                'description': 'Beautiful dupattas to complete your traditional look',
                'sort_order': 3
            }
        ]

        # Create subcategories data
        subcategories_data = {
            'Leggings': [
                {'name': 'Ankle Length Leggings', 'slug': 'ankle-length-leggings'},
                {'name': 'Churidar Leggings', 'slug': 'churidar-leggings'},
                {'name': 'Jeggings', 'slug': 'jeggings'},
                {'name': 'Printed Leggings', 'slug': 'printed-leggings'},
                {'name': 'Solid Leggings', 'slug': 'solid-leggings'},
                {'name': 'Cotton Leggings', 'slug': 'cotton-leggings'},
            ],
            'Pants & Trousers': [
                {'name': 'Palazzo Pants', 'slug': 'palazzo-pants'},
                {'name': 'Formal Trousers', 'slug': 'formal-trousers'},
                {'name': 'Cigarette Pants', 'slug': 'cigarette-pants'},
                {'name': 'Wide Leg Pants', 'slug': 'wide-leg-pants'},
                {'name': 'Culottes', 'slug': 'culottes'},
                {'name': 'Cargo Pants', 'slug': 'cargo-pants'},
            ],
            'Dupattas': [
                {'name': 'Cotton Dupattas', 'slug': 'cotton-dupattas'},
                {'name': 'Silk Dupattas', 'slug': 'silk-dupattas'},
                {'name': 'Net Dupattas', 'slug': 'net-dupattas'},
                {'name': 'Printed Dupattas', 'slug': 'printed-dupattas'},
                {'name': 'Embroidered Dupattas', 'slug': 'embroidered-dupattas'},
                {'name': 'Georgette Dupattas', 'slug': 'georgette-dupattas'},
            ]
        }

        # Create categories
        created_categories = {}
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults={
                    'name': cat_data['name'],
                    'description': cat_data['description'],
                    'sort_order': cat_data['sort_order'],
                    'is_active': True
                }
            )
            created_categories[cat_data['name']] = category
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created category: {category.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Category already exists: {category.name}')
                )

        # Create subcategories
        for category_name, subcats in subcategories_data.items():
            category = created_categories[category_name]
            for i, subcat_data in enumerate(subcats):
                subcategory, created = SubCategory.objects.get_or_create(
                    category=category,
                    slug=subcat_data['slug'],
                    defaults={
                        'name': subcat_data['name'],
                        'description': f'Beautiful {subcat_data["name"].lower()} for every occasion',
                        'sort_order': i + 1,
                        'is_active': True
                    }
                )
                if created:
                    self.stdout.write(
                        self.style.SUCCESS(f'Created subcategory: {subcategory.name}')
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(f'Subcategory already exists: {subcategory.name}')
                    )

        self.stdout.write(
            self.style.SUCCESS('Successfully created categories and subcategories for navbar!')
        )
