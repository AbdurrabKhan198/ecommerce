from django.core.management.base import BaseCommand
from shop.models import Category, SubCategory


class Command(BaseCommand):
    help = 'Add new categories: Scarfs and Stoles with their subcategories'

    def handle(self, *args, **options):
        self.stdout.write('Adding new categories: Scarfs and Stoles...')
        
        # Create Scarfs Category
        scarfs_category, created = Category.objects.get_or_create(
            name='Scarfs',
            defaults={
                'slug': 'scarfs',
                'description': 'Beautiful and elegant scarfs for every occasion. From casual cotton scarfs to luxurious georgette pieces, find the perfect scarf to complement your style.',
                'meta_title': 'Scarfs - Elegant & Stylish Scarfs for Women | King Dupatta House',
                'meta_description': 'Shop premium scarfs online. Cotton scarfs, georgette scarfs, and more. Perfect for every occasion. Free shipping above ₹999.',
                'is_active': True,
                'sort_order': 4
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS('✅ Created Scarfs category'))
        else:
            self.stdout.write('ℹ️  Scarfs category already exists')
        
        # Create Stoles Category
        stoles_category, created = Category.objects.get_or_create(
            name='Stoles',
            defaults={
                'slug': 'stoles',
                'description': 'Elegant stoles to add grace to your outfit. From plain stoles for daily wear to fancy stoles for special occasions.',
                'meta_title': 'Stoles - Plain & Fancy Stoles for Women | King Dupatta House',
                'meta_description': 'Shop beautiful stoles online. Plain stoles for daily wear, fancy stoles for special occasions. Premium quality fabrics.',
                'is_active': True,
                'sort_order': 5
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS('✅ Created Stoles category'))
        else:
            self.stdout.write('ℹ️  Stoles category already exists')
        
        # Create Scarfs Subcategories
        scarfs_subcategories = [
            {
                'name': 'Georgette',
                'slug': 'georgette',
                'description': 'Luxurious georgette scarfs with beautiful drape and elegant finish. Perfect for special occasions and formal wear.',
                'meta_title': 'Georgette Scarfs - Premium Quality | King Dupatta House',
                'meta_description': 'Shop premium georgette scarfs online. Beautiful drape, elegant finish. Perfect for special occasions.',
                'sort_order': 1
            },
            {
                'name': 'Cotton',
                'slug': 'cotton',
                'description': 'Comfortable and breathable cotton scarfs. Perfect for daily wear, office, and casual outings.',
                'meta_title': 'Cotton Scarfs - Comfortable Daily Wear | King Dupatta House',
                'meta_description': 'Shop comfortable cotton scarfs online. Breathable, easy care, perfect for daily wear and office.',
                'sort_order': 2
            }
        ]
        
        for subcat_data in scarfs_subcategories:
            subcategory, created = SubCategory.objects.get_or_create(
                category=scarfs_category,
                name=subcat_data['name'],
                defaults={
                    'slug': subcat_data['slug'],
                    'description': subcat_data['description'],
                    'meta_title': subcat_data['meta_title'],
                    'meta_description': subcat_data['meta_description'],
                    'is_active': True,
                    'sort_order': subcat_data['sort_order']
                }
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'✅ Created Scarfs subcategory: {subcat_data["name"]}'))
            else:
                self.stdout.write(f'ℹ️  Scarfs subcategory "{subcat_data["name"]}" already exists')
        
        # Create Stoles Subcategories
        stoles_subcategories = [
            {
                'name': 'Plain',
                'slug': 'plain',
                'description': 'Simple and elegant plain stoles. Perfect for daily wear, office, and casual occasions.',
                'meta_title': 'Plain Stoles - Simple & Elegant | King Dupatta House',
                'meta_description': 'Shop plain stoles online. Simple, elegant, perfect for daily wear and office.',
                'sort_order': 1
            },
            {
                'name': 'Fancy',
                'slug': 'fancy',
                'description': 'Beautiful fancy stoles with intricate designs and embellishments. Perfect for parties, weddings, and special occasions.',
                'meta_title': 'Fancy Stoles - Party & Wedding Wear | King Dupatta House',
                'meta_description': 'Shop fancy stoles online. Intricate designs, perfect for parties, weddings, and special occasions.',
                'sort_order': 2
            }
        ]
        
        for subcat_data in stoles_subcategories:
            subcategory, created = SubCategory.objects.get_or_create(
                category=stoles_category,
                name=subcat_data['name'],
                defaults={
                    'slug': subcat_data['slug'],
                    'description': subcat_data['description'],
                    'meta_title': subcat_data['meta_title'],
                    'meta_description': subcat_data['meta_description'],
                    'is_active': True,
                    'sort_order': subcat_data['sort_order']
                }
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'✅ Created Stoles subcategory: {subcat_data["name"]}'))
            else:
                self.stdout.write(f'ℹ️  Stoles subcategory "{subcat_data["name"]}" already exists')
        
        self.stdout.write(self.style.SUCCESS('\n🎉 Successfully added new categories and subcategories!'))
        self.stdout.write('\n📋 Summary:')
        self.stdout.write('• Scarfs category with subcategories: Georgette, Cotton')
        self.stdout.write('• Stoles category with subcategories: Plain, Fancy')
        self.stdout.write('\n💡 Run "python manage.py runserver" to see the changes on your website!')
