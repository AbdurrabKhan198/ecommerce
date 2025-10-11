#!/bin/bash

# Production Static Files Deployment Script
echo "🚀 Deploying static files to AWS production server..."

# Collect all static files
echo "📦 Collecting static files..."
python manage.py collectstatic --noinput --clear

# Set proper permissions
echo "🔐 Setting file permissions..."
chmod -R 755 staticfiles/
chmod -R 755 static/

# Restart web server (adjust based on your setup)
echo "🔄 Restarting web server..."
# For Apache:
# sudo systemctl restart apache2
# For Nginx + Gunicorn:
# sudo systemctl restart nginx
# sudo systemctl restart gunicorn

echo "✅ Static files deployment complete!"
echo "🌐 Your logo should now be visible at: https://kingdupattahouse.in/static/images/logo.png"
