#!/bin/bash

# One-Command Auto Deployment Script for King Dupatta House
# Usage: curl -sSL https://raw.githubusercontent.com/yourusername/kingdupattahouse/main/auto_deploy.sh | bash

set -e

echo "🚀 King Dupatta House - Auto Deployment Script"
echo "=============================================="
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
sudo apt-get install -y curl wget git nginx certbot python3-certbot-nginx postgresql-client

# Install Docker
print_info "Installing Docker..."
if ! command -v docker &> /dev/null; then
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
    rm get-docker.sh
    print_status "Docker installed successfully"
    
    # Fix Docker permissions
    print_info "Fixing Docker permissions..."
    sudo chmod 666 /var/run/docker.sock
    sudo systemctl restart docker
    sleep 5
else
    print_status "Docker already installed"
    # Fix Docker permissions
    sudo chmod 666 /var/run/docker.sock
fi

# Install Docker Compose
print_info "Installing Docker Compose..."
if ! command -v docker-compose &> /dev/null; then
    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    print_status "Docker Compose installed successfully"
else
    print_status "Docker Compose already installed"
fi

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
    # Your actual GitHub repository URL
    GITHUB_REPO="https://github.com/AbdurrabKhan198/ecommerce.git"
    git clone $GITHUB_REPO .
fi

# Create environment file if it doesn't exist
if [ ! -f ".env" ]; then
    print_info "Creating environment file..."
    cat > .env << EOF
# Django Settings
DEBUG=False
SECRET_KEY=$(python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
ALLOWED_HOSTS=kingduppatahouse.in,www.kingduppatahouse.in,3.109.208.181,localhost,127.0.0.1

# Database Configuration
DB_NAME=kingdupattahouse
DB_USER=postgres
DB_PASSWORD=postgres123
DB_HOST=db
DB_PORT=5432

# Redis Configuration
REDIS_URL=redis://redis:6379/1

# Site Settings
SITE_NAME=King Dupatta House
SITE_DOMAIN=kingduppatahouse.in
CURRENCY_SYMBOL=₹
FREE_SHIPPING_THRESHOLD=999

# Security Settings (for production, set these to True)
SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
EOF
    print_status "Environment file created"
else
    print_status "Environment file already exists"
fi

# Create SSL directory
mkdir -p ssl

# Create temporary SSL certificate for initial setup
print_info "Creating temporary SSL certificate..."
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout ssl/key.pem \
    -out ssl/cert.pem \
    -subj "/C=IN/ST=UP/L=Lucknow/O=King Dupatta House/CN=kingduppatahouse.in" \
    -addext "subjectAltName=DNS:kingduppatahouse.in,DNS:www.kingduppatahouse.in,IP:3.109.208.181" 2>/dev/null || true

# Build and start services
print_info "Building and starting services..."
docker-compose down 2>/dev/null || true
docker-compose build --no-cache
docker-compose up -d

# Wait for services to be ready
print_info "Waiting for services to start..."
sleep 30

# Check if services are running
if ! docker-compose ps | grep -q "Up"; then
    print_error "Services failed to start. Checking logs..."
    docker-compose logs
    exit 1
fi

# Run database migrations
print_info "Running database migrations..."
docker-compose exec -T web python manage.py migrate --settings=womens_wear_ecommerce.settings_production

# Create superuser (optional)
print_info "Creating superuser..."
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@kingduppatahouse.in', 'admin123') if not User.objects.filter(username='admin').exists() else None" | docker-compose exec -T web python manage.py shell --settings=womens_wear_ecommerce.settings_production

# Collect static files
print_info "Collecting static files..."
docker-compose exec -T web python manage.py collectstatic --noinput --settings=womens_wear_ecommerce.settings_production

# Load sample data
print_info "Loading sample data..."
docker-compose exec -T web python manage.py create_sample_categories --settings=womens_wear_ecommerce.settings_production || true
docker-compose exec -T web python manage.py create_sample_products --settings=womens_wear_ecommerce.settings_production || true
docker-compose exec -T web python manage.py populate_diverse_images --settings=womens_wear_ecommerce.settings_production || true

# Configure Nginx
print_info "Configuring Nginx..."
sudo cp nginx.conf /etc/nginx/sites-available/kingdupattahouse
sudo ln -sf /etc/nginx/sites-available/kingdupattahouse /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl reload nginx

# Setup SSL with Let's Encrypt (optional)
print_info "Setting up SSL certificate..."
if command -v certbot &> /dev/null; then
    print_warning "To get a real SSL certificate, run:"
    print_warning "sudo certbot --nginx -d kingduppatahouse.in -d www.kingduppatahouse.in"
fi

# Create systemd service for auto-start
print_info "Setting up auto-start service..."
sudo tee /etc/systemd/system/kingdupattahouse.service > /dev/null << EOF
[Unit]
Description=King Dupatta House Django App
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=$APP_DIR
ExecStart=/usr/local/bin/docker-compose up -d
ExecStop=/usr/local/bin/docker-compose down
TimeoutStartSec=0
User=$USER

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl enable kingdupattahouse.service
sudo systemctl start kingdupattahouse.service

# Create backup script
print_info "Setting up backup system..."
sudo tee /usr/local/bin/backup_kingdupattahouse.sh > /dev/null << EOF
#!/bin/bash
DATE=\$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/var/backups/kingdupattahouse"
mkdir -p \$BACKUP_DIR

# Backup database
cd $APP_DIR
docker-compose exec -T db pg_dump -U postgres kingdupattahouse > \$BACKUP_DIR/db_\$DATE.sql

# Backup media files
tar -czf \$BACKUP_DIR/media_\$DATE.tar.gz media/ 2>/dev/null || true

# Keep only last 7 days of backups
find \$BACKUP_DIR -name "*.sql" -mtime +7 -delete
find \$BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete
EOF

sudo chmod +x /usr/local/bin/backup_kingdupattahouse.sh

# Setup cron job for backups
(crontab -l 2>/dev/null; echo "0 2 * * * /usr/local/bin/backup_kingdupattahouse.sh") | crontab -

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
echo "   • Domain: http://kingduppatahouse.in (after DNS setup)"
echo "   • Admin Panel: http://3.109.208.181/admin/"
echo ""
echo "👤 Admin Credentials:"
echo "   • Username: admin"
echo "   • Password: admin123"
echo "   • Email: admin@kingduppatahouse.in"
echo ""
echo "📊 Management Commands:"
echo "   • View logs: cd $APP_DIR && docker-compose logs -f"
echo "   • Restart: cd $APP_DIR && docker-compose restart"
echo "   • Update: cd $APP_DIR && git pull && docker-compose up -d --build"
echo "   • Stop: cd $APP_DIR && docker-compose down"
echo ""
echo "🔧 Next Steps:"
echo "   1. Configure your domain DNS to point to 3.109.208.181"
echo "   2. Get SSL certificate: sudo certbot --nginx -d kingduppatahouse.in"
echo "   3. Update .env file with your production credentials"
echo "   4. Configure AWS S3 for static files (optional)"
echo "   5. Setup AWS RDS database (optional)"
echo ""
print_status "Your client can now view the website at: http://3.109.208.181"
echo ""
echo "🚀 Ready for client showcase!"
