#!/bin/bash

# Simple Deployment Script for King Dupatta House (Without Docker)
# Usage: curl -sSL https://raw.githubusercontent.com/AbdurrabKhan198/ecommerce/main/simple_deploy.sh | bash

set -e

echo "🚀 King Dupatta House - Simple Deployment (No Docker)"
echo "===================================================="
echo "Domain: kingduppatahouse.in"
echo "IP: 3.109.208.181"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    print_error "Please don't run this script as root. Run as a regular user."
    exit 1
fi

# Update system
print_info "Updating system packages..."
sudo apt-get update -y
sudo apt-get upgrade -y

# Install required packages
print_info "Installing required packages..."
sudo apt-get install -y python3 python3-pip python3-venv python3-dev postgresql postgresql-contrib nginx certbot python3-certbot-nginx redis-server git curl wget

# Install Python packages
print_info "Installing Python packages..."
pip3 install --user django pillow psycopg2-binary gunicorn

# Create application directory
print_info "Setting up application directory..."
APP_DIR="/var/www/kingdupattahouse"
sudo mkdir -p $APP_DIR
sudo chown $USER:$USER $APP_DIR
cd $APP_DIR

# Clone or update repository
print_info "Setting up repository..."
if [ -d ".git" ]; then
    print_info "Updating existing repository..."
    git pull origin main
else
    print_info "Cloning repository..."
    GITHUB_REPO="https://github.com/AbdurrabKhan198/ecommerce.git"
    git clone $GITHUB_REPO .
fi

# Create virtual environment
print_info "Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install requirements
print_info "Installing Python requirements..."
pip install -r requirements.txt

# Create environment file
print_info "Creating environment file..."
cat > .env << EOF
# Django Settings
DEBUG=False
SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_urlsafe(50))')
ALLOWED_HOSTS=kingduppatahouse.in,www.kingduppatahouse.in,3.109.208.181,localhost,127.0.0.1

# Database Configuration
DB_NAME=kingdupattahouse
DB_USER=postgres
DB_PASSWORD=postgres123
DB_HOST=localhost
DB_PORT=5432

# Site Settings
SITE_NAME=King Dupatta House
SITE_DOMAIN=kingduppatahouse.in
CURRENCY_SYMBOL=₹
FREE_SHIPPING_THRESHOLD=999

# Security Settings
SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
EOF

# Setup PostgreSQL database
print_info "Setting up PostgreSQL database..."
sudo -u postgres psql -c "CREATE DATABASE kingdupattahouse;" || true
sudo -u postgres psql -c "CREATE USER postgres WITH PASSWORD 'postgres123';" || true
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE kingdupattahouse TO postgres;" || true

# Run Django setup
print_info "Setting up Django application..."
export DJANGO_SETTINGS_MODULE=womens_wear_ecommerce.settings_production
python manage.py migrate
python manage.py collectstatic --noinput

# Create superuser
print_info "Creating superuser..."
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@kingduppatahouse.in', 'admin123') if not User.objects.filter(username='admin').exists() else None" | python manage.py shell

# Load sample data
print_info "Loading sample data..."
python manage.py create_sample_categories || true
python manage.py create_sample_products || true
python manage.py populate_diverse_images || true

# Create systemd service
print_info "Creating systemd service..."
sudo tee /etc/systemd/system/kingdupattahouse.service > /dev/null << EOF
[Unit]
Description=King Dupatta House Django App
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$APP_DIR
Environment=PATH=$APP_DIR/venv/bin
Environment=DJANGO_SETTINGS_MODULE=womens_wear_ecommerce.settings_production
ExecStart=$APP_DIR/venv/bin/gunicorn --bind 0.0.0.0:8000 womens_wear_ecommerce.wsgi:application
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Start the service
print_info "Starting application service..."
sudo systemctl daemon-reload
sudo systemctl enable kingdupattahouse.service
sudo systemctl start kingdupattahouse.service

# Configure Nginx
print_info "Configuring Nginx..."
sudo tee /etc/nginx/sites-available/kingdupattahouse > /dev/null << EOF
server {
    listen 80;
    server_name kingduppatahouse.in www.kingduppatahouse.in 3.109.208.181;

    location /static/ {
        alias $APP_DIR/staticfiles/;
    }

    location /media/ {
        alias $APP_DIR/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

# Enable the site
sudo ln -sf /etc/nginx/sites-available/kingdupattahouse /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl reload nginx

# Create SSL certificate
print_info "Setting up SSL certificate..."
sudo certbot --nginx -d kingduppatahouse.in -d www.kingduppatahouse.in --non-interactive --agree-tos --email admin@kingduppatahouse.in || true

# Final status check
print_info "Performing final checks..."
sleep 10

# Check if website is accessible
if curl -f -s http://localhost:8000/ > /dev/null; then
    print_status "Application is running successfully!"
else
    print_warning "Application might not be fully ready yet. Please wait a few minutes."
fi

# Display final information
echo ""
echo "🎉 DEPLOYMENT COMPLETED SUCCESSFULLY!"
echo "======================================"
echo ""
print_status "Your King Dupatta House website is now live!"
echo ""
echo "🌐 Access URLs:"
echo "   • Main Site: http://3.109.208.181"
echo "   • Domain: http://kingduppatahouse.in"
echo "   • Admin Panel: http://3.109.208.181/admin/"
echo ""
echo "👤 Admin Credentials:"
echo "   • Username: admin"
echo "   • Password: admin123"
echo "   • Email: admin@kingduppatahouse.in"
echo ""
echo "📊 Management Commands:"
echo "   • View logs: sudo journalctl -u kingdupattahouse -f"
echo "   • Restart: sudo systemctl restart kingdupattahouse"
echo "   • Update: cd $APP_DIR && git pull && sudo systemctl restart kingdupattahouse"
echo "   • Stop: sudo systemctl stop kingdupattahouse"
echo ""
print_status "Your client can now view the website at: http://3.109.208.181"
echo ""
echo "🚀 Ready for client showcase!"
