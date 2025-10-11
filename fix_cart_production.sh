#!/bin/bash

# Fix Cart AJAX Issues on Production
echo "🛒 Fixing cart functionality on production server..."

# 1. Update settings for production
echo "📝 Updating Django settings for production..."

# 2. Collect static files
echo "📦 Collecting static files..."
python manage.py collectstatic --noinput --clear

# 3. Set proper permissions
echo "🔐 Setting file permissions..."
chmod -R 755 staticfiles/
chmod -R 755 static/

# 4. Clear cache and sessions
echo "🧹 Clearing cache and sessions..."
python manage.py clearsessions
python manage.py shell -c "from django.core.cache import cache; cache.clear()"

# 5. Restart services
echo "🔄 Restarting services..."
sudo systemctl restart nginx
sudo systemctl restart kingdupattahouse

# 6. Test cart functionality
echo "🧪 Testing cart functionality..."
echo "✅ Production cart fix complete!"
echo "🌐 Test your cart at: https://kingdupattahouse.in"
echo ""
echo "🔍 If cart still doesn't work, check:"
echo "1. Browser console for JavaScript errors (F12)"
echo "2. Network tab for failed AJAX requests"
echo "3. CSRF token in cookies"
