#!/bin/bash

# King Dupatta House - One Click Setup
echo "🚀 King Dupatta House - One Click Setup"
echo "========================================"

# Update system
echo "📦 Updating system..."
sudo apt update && sudo apt upgrade -y

# Install required packages
echo "📦 Installing packages..."
sudo apt install -y python3 python3-pip python3-venv nginx git curl postgresql postgresql-contrib

# Create project directory
echo "📁 Creating project directory..."
sudo mkdir -p /home/ubuntu/kingdupattahouse
sudo chown ubuntu:ubuntu /home/ubuntu/kingdupattahouse
cd /home/ubuntu/kingdupattahouse

# Clone repository
echo "📥 Cloning repository..."
git clone https://github.com/AbdurrabKhan198/ecommerce.git .

# Create virtual environment
echo "🐍 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install requirements
echo "📦 Installing Python packages..."
venv/bin/pip install --upgrade pip
venv/bin/pip install Django==5.2.5 gunicorn==21.2.0 whitenoise==6.6.0 psycopg2-binary==2.9.9 Pillow==10.4.0 django-environ==0.11.2

# Setup database
echo "🗄️ Setting up database..."
sudo -u postgres psql -c "CREATE DATABASE kingdupattahouse;" || true
sudo -u postgres psql -c "ALTER USER postgres PASSWORD 'postgres123';" || true
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE kingdupattahouse TO postgres;" || true

# Run Django setup
echo "🚀 Setting up Django..."
export DJANGO_SETTINGS_MODULE=womens_wear_ecommerce.settings
venv/bin/python manage.py migrate
venv/bin/python manage.py collectstatic --noinput

# Create admin user
echo "👤 Creating admin user..."
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@kingduppatahouse.in', 'admin123') if not User.objects.filter(username='admin').exists() else None" | venv/bin/python manage.py shell

# Load sample data
echo "📊 Loading sample data..."
venv/bin/python manage.py create_navbar_categories || true
venv/bin/python manage.py create_sample_products || true
venv/bin/python manage.py populate_diverse_images || true

# Create systemd service
echo "⚙️ Creating service..."
sudo tee /etc/systemd/system/kingdupattahouse.service > /dev/null << EOF
[Unit]
Description=King Dupatta House Django App
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/kingdupattahouse
Environment="PATH=/home/ubuntu/kingdupattahouse/venv/bin"
Environment="DJANGO_SETTINGS_MODULE=womens_wear_ecommerce.settings"
ExecStart=/home/ubuntu/kingdupattahouse/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:8000 womens_wear_ecommerce.wsgi:application

[Install]
WantedBy=multi-user.target
EOF

# Create Nginx config
echo "🌐 Configuring Nginx..."
sudo tee /etc/nginx/sites-available/kingdupattahouse > /dev/null << EOF
server {
    listen 80;
    server_name kingduppatahouse.in www.kingduppatahouse.in 3.109.208.181;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/ubuntu/kingdupattahouse;
    }
    location /media/ {
        root /home/ubuntu/kingdupattahouse;
    }
    location / {
        include proxy_params;
        proxy_pass http://127.0.0.1:8000;
    }
}
EOF

# Enable site
sudo ln -s /etc/nginx/sites-available/kingdupattahouse /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Set permissions
sudo chown -R ubuntu:www-data /home/ubuntu/kingdupattahouse
sudo chmod -R 755 /home/ubuntu/kingdupattahouse

# Start services
echo "🚀 Starting services..."
sudo systemctl daemon-reload
sudo systemctl enable kingdupattahouse
sudo systemctl start kingdupattahouse
sudo systemctl restart nginx

# Configure firewall
sudo ufw allow 'Nginx Full'
sudo ufw allow ssh
sudo ufw --force enable

echo ""
echo "✅ Setup completed successfully!"
echo "🌐 Your website is now available at:"
echo "   • Main Site: http://3.109.208.181"
echo "   • Admin Panel: http://3.109.208.181/admin/"
echo ""
echo "👤 Admin credentials:"
echo "   • Username: admin"
echo "   • Password: admin123"
echo ""
echo "🎉 King Dupatta House is ready for your client showcase!"
