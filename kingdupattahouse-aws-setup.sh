#!/bin/bash

# King Dupatta House - AWS Console Setup Script
# Run this directly on your AWS EC2 instance through the console

echo "🚀 Setting up King Dupatta House on AWS..."
echo "Domain: kingduppatahouse.in"
echo "IP: 3.109.208.181"

# Update system
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install -y python3 python3-pip python3-venv nginx git curl postgresql postgresql-contrib

# Create project directory
mkdir -p /home/ubuntu/kingdupattahouse
cd /home/ubuntu/kingdupattahouse

# Clone your project from GitHub
echo "📁 Cloning King Dupatta House project from GitHub..."
git clone https://github.com/AbdurrabKhan198/ecommerce.git .

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install --upgrade pip
pip install Django==5.2.5 gunicorn==21.2.0 whitenoise==6.6.0 psycopg2-binary==2.9.9 Pillow==10.4.0 django-environ==0.11.2

# Create .env file
cat > .env << EOF
DEBUG=False
SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
ALLOWED_HOSTS=kingduppatahouse.in,www.kingduppatahouse.in,3.109.208.181
DB_NAME=kingdupattahouse
DB_USER=postgres
DB_PASSWORD=postgres123
DB_HOST=localhost
DB_PORT=5432
SITE_NAME=King Dupatta House
SITE_DOMAIN=kingduppatahouse.in
CURRENCY_SYMBOL=₹
FREE_SHIPPING_THRESHOLD=999
EOF

# Setup PostgreSQL database
echo "🗄️ Setting up PostgreSQL database..."
sudo -u postgres psql -c "CREATE DATABASE kingdupattahouse;" || true
sudo -u postgres psql -c "ALTER USER postgres PASSWORD 'postgres123';" || true
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE kingdupattahouse TO postgres;" || true

# Run Django setup
echo "🚀 Setting up Django application..."
export DJANGO_SETTINGS_MODULE=womens_wear_ecommerce.settings_production
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

# Create Gunicorn service
sudo tee /etc/systemd/system/kingdupattahouse.service > /dev/null << EOF
[Unit]
Description=King Dupatta House Django App
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/kingdupattahouse
Environment="PATH=/home/ubuntu/kingdupattahouse/venv/bin"
Environment="DJANGO_SETTINGS_MODULE=womens_wear_ecommerce.settings_production"
ExecStart=/home/ubuntu/kingdupattahouse/venv/bin/gunicorn --workers 3 --bind unix:/home/ubuntu/kingdupattahouse/kingdupattahouse.sock womens_wear_ecommerce.wsgi:application

[Install]
WantedBy=multi-user.target
EOF

# Create Nginx config
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
        proxy_pass http://unix:/home/ubuntu/kingdupattahouse/kingdupattahouse.sock;
    }
}
EOF

# Enable site
sudo ln -s /etc/nginx/sites-available/kingdupattahouse /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default

# Set permissions
sudo chown -R ubuntu:www-data /home/ubuntu/kingdupattahouse
sudo chmod -R 755 /home/ubuntu/kingdupattahouse

# Start services
sudo systemctl daemon-reload
sudo systemctl enable kingdupattahouse
sudo systemctl start kingdupattahouse
sudo systemctl restart nginx

# Configure firewall
sudo ufw allow 'Nginx Full'
sudo ufw allow ssh
sudo ufw --force enable

# Install SSL
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d kingduppatahouse.in -d www.kingduppatahouse.in --non-interactive --agree-tos --email admin@kingduppatahouse.in

echo "✅ Setup completed! Your King Dupatta House website should be available at:"
echo "🌐 http://3.109.208.181"
echo "🌐 https://kingduppatahouse.in (after DNS setup)"
echo ""
echo "👤 Admin Panel:"
echo "   • URL: http://3.109.208.181/admin/"
echo "   • Username: admin"
echo "   • Password: admin123"
echo ""
echo "📋 Management Commands:"
echo "   • View logs: sudo journalctl -u kingdupattahouse -f"
echo "   • Restart: sudo systemctl restart kingdupattahouse"
echo "   • Update: cd /home/ubuntu/kingdupattahouse && git pull && sudo systemctl restart kingdupattahouse"
echo ""
echo "🎉 Your King Dupatta House e-commerce website is ready for client showcase!"
