from django.core.management.base import BaseCommand
from shop.models import Category, SubCategory


class Command(BaseCommand):
    help = 'Add subcategories for Dupattas category'

    def handle(self, *args, **options):
        self.stdout.write('Adding subcategories for Dupattas category...')
        
        try:
            # Get Dupattas category
            dupattas_category = Category.objects.get(name='Dupattas')
            self.stdout.write(f'✅ Found Dupattas category')
            
            # Define subcategories for Dupattas
            dupatta_subcategories = [
                {
                    'name': 'Cotton Plain Dupatta',
                    'slug': 'cotton-plain-dupatta',
                    'description': 'Simple and elegant cotton dupattas in solid colors. Perfect for daily wear, office, and casual occasions. Comfortable and easy to care for.',
                    'meta_title': 'Cotton Plain Dupattas - Simple & Elegant | King Dupatta House',
                    'meta_description': 'Shop cotton plain dupattas online. Simple, elegant, perfect for daily wear and office. Comfortable fabric.',
                    'sort_order': 1
                },
                {
                    'name': 'Cotton Printed Dupatta',
                    'slug': 'cotton-printed-dupatta',
                    'description': 'Beautiful cotton dupattas with various prints and patterns. From floral to geometric designs, perfect for casual and semi-formal occasions.',
                    'meta_title': 'Cotton Printed Dupattas - Beautiful Patterns | King Dupatta House',
                    'meta_description': 'Shop cotton printed dupattas online. Beautiful patterns, floral designs, perfect for casual wear.',
                    'sort_order': 2
                },
                {
                    'name': 'Banarasi Dupatta',
                    'slug': 'banarasi-dupatta',
                    'description': 'Luxurious Banarasi dupattas with intricate zari work and traditional patterns. Perfect for weddings, festivals, and special occasions.',
                    'meta_title': 'Banarasi Dupattas - Traditional Zari Work | King Dupatta House',
                    'meta_description': 'Shop Banarasi dupattas online. Traditional zari work, perfect for weddings and festivals. Premium quality.',
                    'sort_order': 3
                },
                {
                    'name': 'Chiffon Dupatta',
                    'slug': 'chiffon-dupatta',
                    'description': 'Elegant chiffon dupattas with beautiful drape and flow. Perfect for parties, formal occasions, and special events.',
                    'meta_title': 'Chiffon Dupattas - Elegant & Flowing | King Dupatta House',
                    'meta_description': 'Shop chiffon dupattas online. Beautiful drape, elegant finish, perfect for parties and formal wear.',
                    'sort_order': 4
                },
                {
                    'name': 'Fancy Dupatta',
                    'slug': 'fancy-dupatta',
                    'description': 'Stylish fancy dupattas with embellishments, embroidery, and decorative elements. Perfect for parties and special occasions.',
                    'meta_title': 'Fancy Dupattas - Embellished & Stylish | King Dupatta House',
                    'meta_description': 'Shop fancy dupattas online. Embellished, embroidered, perfect for parties and special occasions.',
                    'sort_order': 5
                },
                {
                    'name': 'Red Bridal Dupatta',
                    'slug': 'red-bridal-dupatta',
                    'description': 'Traditional red bridal dupattas for weddings and bridal ceremonies. Rich fabrics with traditional designs and embellishments.',
                    'meta_title': 'Red Bridal Dupattas - Wedding Collection | King Dupatta House',
                    'meta_description': 'Shop red bridal dupattas online. Traditional designs, perfect for weddings and bridal ceremonies.',
                    'sort_order': 6
                },
                {
                    'name': 'Customised Dupatta',
                    'slug': 'customised-dupatta',
                    'description': 'Customized dupattas made to your specifications. Choose your fabric, color, design, and get a unique dupatta tailored just for you.',
                    'meta_title': 'Customised Dupattas - Made to Order | King Dupatta House',
                    'meta_description': 'Order customised dupattas online. Choose fabric, color, design. Made to your specifications.',
                    'sort_order': 7
                }
            ]
            
            # Create subcategories
            created_count = 0
            for subcat_data in dupatta_subcategories:
                subcategory, created = SubCategory.objects.get_or_create(
                    category=dupattas_category,
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
                    created_count += 1
                    self.stdout.write(self.style.SUCCESS(f'✅ Created Dupattas subcategory: {subcat_data["name"]}'))
                else:
                    self.stdout.write(f'ℹ️  Dupattas subcategory "{subcat_data["name"]}" already exists')
            
            self.stdout.write(self.style.SUCCESS(f'\n🎉 Successfully added {created_count} new Dupattas subcategories!'))
            self.stdout.write('\n📋 Dupattas Subcategories Added:')
            for subcat_data in dupatta_subcategories:
                self.stdout.write(f'• {subcat_data["name"]}')
            
            self.stdout.write('\n💡 Run "python manage.py runserver" to see the changes on your website!')
            
        except Category.DoesNotExist:
            self.stdout.write(self.style.ERROR('❌ Dupattas category not found!'))
            self.stdout.write('Please make sure the Dupattas category exists in your database.')
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error: {str(e)}'))
