from django.core.management.base import BaseCommand
from shop.models import Review, Product
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Manage customer reviews for King Dupatta House'

    def add_arguments(self, parser):
        parser.add_argument(
            '--action',
            type=str,
            choices=['list', 'approve', 'disapprove', 'delete', 'stats'],
            default='list',
            help='Action to perform: list, approve, disapprove, delete, or stats'
        )
        parser.add_argument(
            '--review-id',
            type=int,
            help='Review ID to approve, disapprove, or delete'
        )
        parser.add_argument(
            '--all',
            action='store_true',
            help='Apply action to all reviews'
        )

    def handle(self, *args, **options):
        action = options['action']
        review_id = options.get('review_id')
        all_reviews = options.get('all', False)

        if action == 'list':
            self.list_reviews()
        elif action == 'approve':
            self.approve_reviews(review_id, all_reviews)
        elif action == 'disapprove':
            self.disapprove_reviews(review_id, all_reviews)
        elif action == 'delete':
            self.delete_reviews(review_id, all_reviews)
        elif action == 'stats':
            self.show_stats()

    def list_reviews(self):
        """List all reviews with their status"""
        reviews = Review.objects.select_related('user', 'product').order_by('-created_at')
        
        if reviews:
            self.stdout.write(self.style.SUCCESS(f'Found {reviews.count()} reviews:'))
            self.stdout.write('-' * 80)
            for review in reviews:
                status = "✅ Approved" if review.is_approved else "⏳ Pending"
                verified = "✓ Verified" if review.is_verified_purchase else "○ Regular"
                self.stdout.write(
                    f'ID: {review.id} | {review.rating}★ | {review.title[:30]}... | '
                    f'{review.user.get_full_name()} | {review.product.name[:20]}... | '
                    f'{status} | {verified} | {review.created_at.strftime("%Y-%m-%d")}'
                )
        else:
            self.stdout.write(self.style.WARNING('No reviews found.'))

    def approve_reviews(self, review_id, all_reviews):
        """Approve review(s)"""
        if all_reviews:
            count = Review.objects.filter(is_approved=False).update(is_approved=True)
            self.stdout.write(self.style.SUCCESS(f'Approved {count} reviews.'))
        elif review_id:
            try:
                review = Review.objects.get(id=review_id)
                if review.is_approved:
                    self.stdout.write(self.style.WARNING(f'Review {review_id} is already approved.'))
                else:
                    review.is_approved = True
                    review.save()
                    self.stdout.write(self.style.SUCCESS(f'Approved review {review_id}: "{review.title}"'))
            except Review.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Review with ID {review_id} not found.'))
        else:
            self.stdout.write(self.style.ERROR('Please provide --review-id or use --all flag.'))

    def disapprove_reviews(self, review_id, all_reviews):
        """Disapprove review(s)"""
        if all_reviews:
            count = Review.objects.filter(is_approved=True).update(is_approved=False)
            self.stdout.write(self.style.SUCCESS(f'Disapproved {count} reviews.'))
        elif review_id:
            try:
                review = Review.objects.get(id=review_id)
                if not review.is_approved:
                    self.stdout.write(self.style.WARNING(f'Review {review_id} is already disapproved.'))
                else:
                    review.is_approved = False
                    review.save()
                    self.stdout.write(self.style.SUCCESS(f'Disapproved review {review_id}: "{review.title}"'))
            except Review.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Review with ID {review_id} not found.'))
        else:
            self.stdout.write(self.style.ERROR('Please provide --review-id or use --all flag.'))

    def delete_reviews(self, review_id, all_reviews):
        """Delete review(s)"""
        if all_reviews:
            count = Review.objects.count()
            Review.objects.all().delete()
            self.stdout.write(self.style.SUCCESS(f'Deleted {count} reviews.'))
        elif review_id:
            try:
                review = Review.objects.get(id=review_id)
                title = review.title
                review.delete()
                self.stdout.write(self.style.SUCCESS(f'Deleted review {review_id}: "{title}"'))
            except Review.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Review with ID {review_id} not found.'))
        else:
            self.stdout.write(self.style.ERROR('Please provide --review-id or use --all flag.'))

    def show_stats(self):
        """Show review statistics"""
        total_reviews = Review.objects.count()
        approved_reviews = Review.objects.filter(is_approved=True).count()
        pending_reviews = Review.objects.filter(is_approved=False).count()
        verified_reviews = Review.objects.filter(is_verified_purchase=True).count()
        
        # Average rating
        from django.db.models import Avg
        avg_rating = Review.objects.filter(is_approved=True).aggregate(
            avg_rating=Avg('rating')
        )['avg_rating'] or 0
        
        # Rating distribution
        rating_dist = {}
        for rating in range(1, 6):
            count = Review.objects.filter(rating=rating).count()
            rating_dist[rating] = count
        
        self.stdout.write(self.style.SUCCESS('📊 Review Statistics:'))
        self.stdout.write('-' * 40)
        self.stdout.write(f'Total Reviews: {total_reviews}')
        self.stdout.write(f'Approved: {approved_reviews}')
        self.stdout.write(f'Pending: {pending_reviews}')
        self.stdout.write(f'Verified Purchases: {verified_reviews}')
        self.stdout.write(f'Average Rating: {avg_rating:.1f}/5')
        self.stdout.write('\nRating Distribution:')
        for rating in range(5, 0, -1):
            count = rating_dist[rating]
            percentage = (count / total_reviews * 100) if total_reviews > 0 else 0
            bar = '█' * int(percentage / 2)
            self.stdout.write(f'{rating}★: {count:3d} ({percentage:4.1f}%) {bar}')


# Usage examples:
# python manage.py manage_reviews --action list
# python manage.py manage_reviews --action approve --review-id 1
# python manage.py manage_reviews --action approve --all
# python manage.py manage_reviews --action stats
# python manage.py manage_reviews --action delete --review-id 1
