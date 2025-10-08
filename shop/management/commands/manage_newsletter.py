from django.core.management.base import BaseCommand
from shop.models import WhatsAppSubscription
from django.utils import timezone


class Command(BaseCommand):
    help = 'Manage WhatsApp subscriptions for King Dupatta House'

    def add_arguments(self, parser):
        parser.add_argument(
            '--action',
            type=str,
            choices=['list', 'stats', 'export', 'cleanup'],
            default='list',
            help='Action to perform: list, stats, export, or cleanup'
        )
        parser.add_argument(
            '--phone',
            type=str,
            help='Phone number to manage'
        )
        parser.add_argument(
            '--status',
            type=str,
            choices=['active', 'inactive'],
            help='Filter by subscription status'
        )

    def handle(self, *args, **options):
        action = options['action']
        phone = options.get('phone')
        status = options.get('status')

        if action == 'list':
            self.list_subscriptions(status, phone)
        elif action == 'stats':
            self.show_stats()
        elif action == 'export':
            self.export_subscriptions()
        elif action == 'cleanup':
            self.cleanup_subscriptions()

    def list_subscriptions(self, status=None, phone=None):
        """List WhatsApp subscriptions"""
        queryset = WhatsAppSubscription.objects.all()
        
        if status == 'active':
            queryset = queryset.filter(is_active=True)
        elif status == 'inactive':
            queryset = queryset.filter(is_active=False)
            
        if phone:
            queryset = queryset.filter(phone_number__icontains=phone)
        
        subscriptions = queryset.order_by('-subscribed_at')
        
        if subscriptions:
            self.stdout.write(self.style.SUCCESS(f'Found {subscriptions.count()} WhatsApp subscriptions:'))
            self.stdout.write('-' * 80)
            for sub in subscriptions:
                status_icon = "✅" if sub.is_active else "❌"
                name = sub.name if sub.name else "No name"
                self.stdout.write(
                    f'{status_icon} {sub.phone_number} | {name} | {sub.source} | {sub.subscribed_at.strftime("%Y-%m-%d %H:%M")}'
                )
        else:
            self.stdout.write(self.style.WARNING('No WhatsApp subscriptions found.'))

    def show_stats(self):
        """Show WhatsApp subscription statistics"""
        total_subscriptions = WhatsAppSubscription.objects.count()
        active_subscriptions = WhatsAppSubscription.objects.filter(is_active=True).count()
        inactive_subscriptions = WhatsAppSubscription.objects.filter(is_active=False).count()
        
        # Recent subscriptions (last 30 days)
        from datetime import timedelta
        thirty_days_ago = timezone.now() - timedelta(days=30)
        recent_subscriptions = WhatsAppSubscription.objects.filter(
            subscribed_at__gte=thirty_days_ago
        ).count()
        
        # Source breakdown
        source_stats = {}
        for source in WhatsAppSubscription.objects.values_list('source', flat=True).distinct():
            count = WhatsAppSubscription.objects.filter(source=source).count()
            source_stats[source] = count
        
        self.stdout.write(self.style.SUCCESS('📱 WhatsApp Subscription Statistics:'))
        self.stdout.write('-' * 50)
        self.stdout.write(f'Total Subscriptions: {total_subscriptions}')
        self.stdout.write(f'Active Subscriptions: {active_subscriptions}')
        self.stdout.write(f'Inactive Subscriptions: {inactive_subscriptions}')
        self.stdout.write(f'Recent (30 days): {recent_subscriptions}')
        self.stdout.write('\nSource Breakdown:')
        for source, count in source_stats.items():
            percentage = (count / total_subscriptions * 100) if total_subscriptions > 0 else 0
            self.stdout.write(f'  {source}: {count} ({percentage:.1f}%)')

    def export_subscriptions(self):
        """Export active subscriptions to CSV format"""
        active_subscriptions = WhatsAppSubscription.objects.filter(is_active=True)
        
        if not active_subscriptions.exists():
            self.stdout.write(self.style.WARNING('No active subscriptions to export.'))
            return
        
        self.stdout.write('Phone Number,Name,Subscribed Date,Source')
        for sub in active_subscriptions:
            name = sub.name if sub.name else "No name"
            self.stdout.write(f'{sub.phone_number},{name},{sub.subscribed_at.strftime("%Y-%m-%d")},{sub.source}')
        
        self.stdout.write(self.style.SUCCESS(f'\nExported {active_subscriptions.count()} active subscriptions.'))

    def cleanup_subscriptions(self):
        """Clean up old inactive subscriptions (older than 1 year)"""
        from datetime import timedelta
        one_year_ago = timezone.now() - timedelta(days=365)
        
        old_inactive = WhatsAppSubscription.objects.filter(
            is_active=False,
            unsubscribed_at__lt=one_year_ago
        )
        
        count = old_inactive.count()
        if count > 0:
            old_inactive.delete()
            self.stdout.write(self.style.SUCCESS(f'Cleaned up {count} old inactive subscriptions.'))
        else:
            self.stdout.write(self.style.WARNING('No old inactive subscriptions to clean up.'))


# Usage examples:
# python manage.py manage_newsletter --action list
# python manage.py manage_newsletter --action stats
# python manage.py manage_newsletter --action export
# python manage.py manage_newsletter --action list --status active
# python manage.py manage_newsletter --action list --phone "9876543210"
