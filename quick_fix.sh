#!/bin/bash

# Quick fix for the current deployment issue
echo "🔧 Quick Fix for King Dupatta House Deployment"
echo "=============================================="

# Install required packages
echo "📦 Installing required packages..."
sudo apt-get update
sudo apt-get install -y python3-full python3-venv python3-pip postgresql postgresql-contrib nginx

# Create application directory
APP_DIR="/var/www/kingdupattahouse"
sudo mkdir -p $APP_DIR
sudo chown $USER:$USER $APP_DIR
cd $APP_DIR

# Clone repository if not exists
if [ ! -d ".git" ]; then
    echo "📥 Cloning repository..."
    git clone https://github.com/AbdurrabKhan198/ecommerce.git .
fi

# Create virtual environment
echo "🐍 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install requirements
echo "📦 Installing Python packages..."
venv/bin/pip install --upgrade pip
venv/bin/pip install -r requirements.txt

# Setup database
echo "🗄️ Setting up database..."
sudo -u postgres psql -c "CREATE DATABASE kingdupattahouse;" || true
sudo -u postgres psql -c "ALTER USER postgres PASSWORD 'postgres123';" || true

# Run Django setup
echo "🚀 Setting up Django..."
export DJANGO_SETTINGS_MODULE=womens_wear_ecommerce.settings_production
venv/bin/python manage.py migrate
venv/bin/python manage.py collectstatic --noinput

# Create superuser
echo "👤 Creating admin user..."
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@kingduppatahouse.in', 'admin123') if not User.objects.filter(username='admin').exists() else None" | venv/bin/python manage.py shell

# Load sample data
echo "📊 Loading sample data..."
venv/bin/python manage.py create_sample_categories || true
venv/bin/python manage.py create_sample_products || true
venv/bin/python manage.py populate_diverse_images || true

# Start the application
echo "🌐 Starting application..."
venv/bin/gunicorn --bind 0.0.0.0:8000 womens_wear_ecommerce.wsgi:application &

echo ""
echo "✅ Quick fix completed!"
echo "🌐 Your website should now be accessible at:"
echo "   • http://3.109.208.181:8000"
echo "   • Admin: http://3.109.208.191:8000/admin/"
echo ""
echo "👤 Admin credentials:"
echo "   • Username: admin"
echo "   • Password: admin123"
echo ""
echo "🔧 To stop the application: pkill -f gunicorn"
echo "🔧 To restart: venv/bin/gunicorn --bind 0.0.0.0:8000 womens_wear_ecommerce.wsgi:application &"
