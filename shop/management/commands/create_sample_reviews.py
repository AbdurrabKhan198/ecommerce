from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from shop.models import Product, Review
import random
from datetime import datetime, timedelta

User = get_user_model()


class Command(BaseCommand):
    help = 'Create sample customer reviews for King Dupatta House'

    def handle(self, *args, **options):
        # Sample review data
        review_data = [
            {
                'title': 'Amazing quality and perfect fit!',
                'comment': 'The leggings are so comfortable and the fabric quality is excellent. I\'ve ordered multiple pieces and they all exceeded my expectations. The fit is perfect and the material feels premium. Will definitely order again!',
                'rating': 5,
                'customer_name': 'Priya Sharma'
            },
            {
                'title': 'Fast delivery and beautiful products',
                'comment': 'Ordered palazzo pants and dupatta set. Both are gorgeous! The delivery was super fast and packaging was premium. The quality is outstanding and the colors are exactly as shown in the pictures.',
                'rating': 5,
                'customer_name': 'Sneha Patel'
            },
            {
                'title': 'Highly recommend for quality',
                'comment': 'Great fit and the material feels premium. Will definitely order again. The customer service is also excellent! The dupatta is so soft and the embroidery work is beautiful.',
                'rating': 5,
                'customer_name': 'Kavya Reddy'
            },
            {
                'title': 'Perfect for office wear',
                'comment': 'The straight fit pants are exactly what I needed for office. Comfortable all day long and the fabric doesn\'t wrinkle easily. Great value for money!',
                'rating': 4,
                'customer_name': 'Anita Singh'
            },
            {
                'title': 'Beautiful silk dupatta',
                'comment': 'The silk dupatta is absolutely gorgeous! The workmanship is excellent and the colors are vibrant. Perfect for special occasions. Highly recommended!',
                'rating': 5,
                'customer_name': 'Meera Joshi'
            },
            {
                'title': 'Comfortable and stylish',
                'comment': 'Love the capri leggings! They are so comfortable for daily wear and the fit is perfect. The fabric is breathable and doesn\'t fade after washing.',
                'rating': 4,
                'customer_name': 'Ritu Agarwal'
            },
            {
                'title': 'Excellent customer service',
                'comment': 'Had a small issue with my order but the customer service team resolved it immediately. The products are of great quality and the service is top-notch!',
                'rating': 5,
                'customer_name': 'Sunita Gupta'
            },
            {
                'title': 'Great value for money',
                'comment': 'The cotton printed dupatta is beautiful and the price is very reasonable. The print quality is excellent and the fabric is soft. Will order more!',
                'rating': 4,
                'customer_name': 'Pooja Verma'
            },
            {
                'title': 'Perfect fit and quality',
                'comment': 'The palazzo pants fit perfectly and the quality is excellent. The fabric drapes beautifully and the stitching is neat. Very satisfied with my purchase!',
                'rating': 5,
                'customer_name': 'Shilpa Kumar'
            },
            {
                'title': 'Love the collection',
                'comment': 'Ordered multiple items and all are of great quality. The variety is amazing and the prices are reasonable. The packaging was also very nice.',
                'rating': 5,
                'customer_name': 'Neha Sharma'
            },
            {
                'title': 'Soft and comfortable',
                'comment': 'The cotton leggings are so soft and comfortable. Perfect for everyday wear. The color is exactly as shown and the fit is great.',
                'rating': 4,
                'customer_name': 'Deepika Singh'
            },
            {
                'title': 'Beautiful embroidery work',
                'comment': 'The dupatta has beautiful embroidery work. The thread work is neat and the design is elegant. Perfect for traditional occasions.',
                'rating': 5,
                'customer_name': 'Rekha Patel'
            },
            {
                'title': 'Fast shipping',
                'comment': 'Received my order within 2 days! The product quality is excellent and matches the description perfectly. Will definitely shop again.',
                'rating': 5,
                'customer_name': 'Sushma Reddy'
            },
            {
                'title': 'Great fabric quality',
                'comment': 'The fabric quality is excellent and the stitching is neat. The pants are comfortable and the fit is perfect. Very happy with my purchase!',
                'rating': 4,
                'customer_name': 'Lakshmi Devi'
            },
            {
                'title': 'Exceeded expectations',
                'comment': 'The product exceeded my expectations! The quality is much better than I anticipated. The colors are vibrant and the fabric is soft.',
                'rating': 5,
                'customer_name': 'Vijaya Kumari'
            },
            {
                'title': 'Perfect for parties',
                'comment': 'The georgette dupatta is perfect for parties. The drape is beautiful and the color is stunning. Received many compliments!',
                'rating': 5,
                'customer_name': 'Swati Agarwal'
            },
            {
                'title': 'Good quality fabric',
                'comment': 'The fabric quality is good and the fit is comfortable. The price is reasonable for the quality provided. Would recommend to others.',
                'rating': 4,
                'customer_name': 'Jyoti Singh'
            },
            {
                'title': 'Beautiful colors',
                'comment': 'Love the color combinations! The products are exactly as shown in the pictures. The quality is good and the delivery was fast.',
                'rating': 4,
                'customer_name': 'Manju Sharma'
            },
            {
                'title': 'Excellent packaging',
                'comment': 'The packaging was excellent and the product arrived in perfect condition. The quality is great and the fit is perfect. Very satisfied!',
                'rating': 5,
                'customer_name': 'Sarita Gupta'
            },
            {
                'title': 'Worth the money',
                'comment': 'The products are worth every penny! The quality is excellent and the designs are beautiful. Will definitely order more items.',
                'rating': 5,
                'customer_name': 'Usha Patel'
            },
            {
                'title': 'Comfortable all day',
                'comment': 'The leggings are so comfortable that I can wear them all day. The fabric is breathable and the fit is perfect. Highly recommended!',
                'rating': 5,
                'customer_name': 'Geeta Verma'
            },
            {
                'title': 'Beautiful traditional wear',
                'comment': 'The dupatta is perfect for traditional occasions. The workmanship is excellent and the colors are vibrant. Love it!',
                'rating': 5,
                'customer_name': 'Kamala Devi'
            },
            {
                'title': 'Great customer support',
                'comment': 'Had a query about sizing and the customer support team was very helpful. The product quality is excellent and the service is great!',
                'rating': 5,
                'customer_name': 'Indira Singh'
            },
            {
                'title': 'Perfect fit',
                'comment': 'The fit is perfect and the quality is excellent. The fabric is soft and comfortable. Very happy with my purchase!',
                'rating': 4,
                'customer_name': 'Radha Sharma'
            },
            {
                'title': 'Love the designs',
                'comment': 'The designs are beautiful and the quality is excellent. The colors are exactly as shown and the fabric is soft. Will order more!',
                'rating': 5,
                'customer_name': 'Sita Patel'
            }
        ]

        # Get all products
        products = Product.objects.filter(is_active=True)
        if not products.exists():
            self.stdout.write(
                self.style.ERROR('No active products found. Please create products first.')
            )
            return

        created_reviews = []
        
        # Create reviews for each product
        for product in products:
            # Create 2-4 reviews per product
            num_reviews = random.randint(2, 4)
            selected_reviews = random.sample(review_data, num_reviews)
            
            for review_info in selected_reviews:
                # Create a fake user for the review
                user, created = User.objects.get_or_create(
                    username=f"customer_{random.randint(1000, 9999)}",
                    defaults={
                        'email': f"customer{random.randint(1000, 9999)}@example.com",
                        'first_name': review_info['customer_name'].split()[0],
                        'last_name': review_info['customer_name'].split()[1] if len(review_info['customer_name'].split()) > 1 else '',
                    }
                )
                
                # Create review
                review, created = Review.objects.get_or_create(
                    product=product,
                    user=user,
                    defaults={
                        'rating': review_info['rating'],
                        'title': review_info['title'],
                        'comment': review_info['comment'],
                        'is_approved': True,
                        'is_verified_purchase': random.choice([True, False]),
                        'created_at': datetime.now() - timedelta(days=random.randint(1, 90))
                    }
                )
                
                if created:
                    created_reviews.append(review)
                    self.stdout.write(
                        self.style.SUCCESS(f'Created review: "{review.title}" for {product.name}')
                    )

        self.stdout.write(
            self.style.SUCCESS(f'\n✅ Successfully created {len(created_reviews)} customer reviews!')
        )
        self.stdout.write(
            self.style.SUCCESS('Reviews are now visible on your homepage and product pages.')
        )
        self.stdout.write(
            self.style.SUCCESS('You can manage reviews from the Django admin panel.')
        )
