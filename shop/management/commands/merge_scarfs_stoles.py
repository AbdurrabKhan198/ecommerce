from django.core.management.base import BaseCommand
from shop.models import Category, SubCategory, Product


class Command(BaseCommand):
    help = 'Merge Scarfs and Stoles into a single "Scarfs & Stoles" category'

    def handle(self, *args, **options):
        self.stdout.write('Merging Scarfs and Stoles into single category...')
        
        try:
            # Get existing categories
            scarfs_category = Category.objects.get(name='Scarfs')
            stoles_category = Category.objects.get(name='Stoles')
            
            # Create new merged category
            merged_category, created = Category.objects.get_or_create(
                name='Scarfs & Stoles',
                defaults={
                    'slug': 'scarfs-stoles',
                    'description': 'Beautiful scarfs and elegant stoles for every occasion. From casual cotton scarfs to luxurious stoles, find the perfect accessory to complement your style.',
                    'meta_title': 'Scarfs & Stoles - Elegant Accessories | King Dupatta House',
                    'meta_description': 'Shop premium scarfs and stoles online. Cotton scarfs, georgette scarfs, plain stoles, fancy stoles. Perfect for every occasion.',
                    'is_active': True,
                    'sort_order': 4
                }
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS('✅ Created merged category: Scarfs & Stoles'))
            else:
                self.stdout.write('ℹ️  Merged category "Scarfs & Stoles" already exists')
            
            # Get all subcategories from both categories
            scarfs_subcategories = SubCategory.objects.filter(category=scarfs_category)
            stoles_subcategories = SubCategory.objects.filter(category=stoles_category)
            
            # Move Scarfs subcategories to merged category
            for subcat in scarfs_subcategories:
                subcat.category = merged_category
                subcat.save()
                self.stdout.write(f'✅ Moved Scarfs subcategory: {subcat.name}')
            
            # Move Stoles subcategories to merged category
            for subcat in stoles_subcategories:
                subcat.category = merged_category
                subcat.save()
                self.stdout.write(f'✅ Moved Stoles subcategory: {subcat.name}')
            
            # Update products to use merged category
            scarfs_products = Product.objects.filter(category=scarfs_category)
            stoles_products = Product.objects.filter(category=stoles_category)
            
            for product in scarfs_products:
                product.category = merged_category
                product.save()
                self.stdout.write(f'✅ Updated product: {product.name}')
            
            for product in stoles_products:
                product.category = merged_category
                product.save()
                self.stdout.write(f'✅ Updated product: {product.name}')
            
            # Delete old categories
            scarfs_category.delete()
            self.stdout.write('✅ Deleted old Scarfs category')
            
            stoles_category.delete()
            self.stdout.write('✅ Deleted old Stoles category')
            
            self.stdout.write(self.style.SUCCESS('\n🎉 Successfully merged Scarfs and Stoles!'))
            self.stdout.write('\n📋 New Category Structure:')
            self.stdout.write('• Scarfs & Stoles')
            self.stdout.write('  ├── Georgette (from Scarfs)')
            self.stdout.write('  ├── Cotton (from Scarfs)')
            self.stdout.write('  ├── Plain (from Stoles)')
            self.stdout.write('  └── Fancy (from Stoles)')
            
            self.stdout.write('\n💡 Run "python manage.py runserver" to see the changes!')
            
        except Category.DoesNotExist as e:
            self.stdout.write(self.style.ERROR(f'❌ Category not found: {str(e)}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error: {str(e)}'))
