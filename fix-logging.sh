#!/bin/bash

# Quick fix for the logging directory issue
echo "🔧 Fixing logging directory issue..."

# Create log directory
sudo mkdir -p /var/log/django
sudo chown ubuntu:ubuntu /var/log/django

# Navigate to project directory
cd /home/ubuntu/kingdupattahouse

# Activate virtual environment
source venv/bin/activate

# Set environment
export DJANGO_SETTINGS_MODULE=womens_wear_ecommerce.settings_production

# Now run Django commands
echo "🚀 Running Django setup..."
python manage.py collectstatic --noinput
python manage.py migrate

# Create superuser
echo "👤 Creating admin user..."
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@kingduppatahouse.in', 'admin123') if not User.objects.filter(username='admin').exists() else None" | python manage.py shell

# Load sample data
echo "📊 Loading sample data..."
python manage.py create_sample_categories || true
python manage.py create_sample_products || true
python manage.py populate_diverse_images || true

# Restart the service
echo "🔄 Restarting service..."
sudo systemctl restart kingdupattahouse

echo "✅ Fixed! Your website should now be working at:"
echo "🌐 http://3.109.208.181"
echo "👤 Admin: http://3.109.208.181/admin/ (admin/admin123)"
