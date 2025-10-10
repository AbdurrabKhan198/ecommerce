#!/bin/bash

# AWS Deployment Script for King Dupatta House
# Domain: kingduppatahouse.in
# IP: 3.109.208.181

set -e

echo "🚀 Starting AWS deployment for King Dupatta House..."

# Update system
echo "📦 Updating system packages..."
sudo apt-get update
sudo apt-get upgrade -y

# Install Docker
echo "🐳 Installing Docker..."
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
echo "🔧 Installing Docker Compose..."
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Install Nginx
echo "🌐 Installing Nginx..."
sudo apt-get install -y nginx

# Install Certbot for SSL
echo "🔒 Installing Certbot for SSL..."
sudo apt-get install -y certbot python3-certbot-nginx

# Create application directory
echo "📁 Creating application directory..."
sudo mkdir -p /var/www/kingdupattahouse
sudo chown $USER:$USER /var/www/kingdupattahouse
cd /var/www/kingdupattahouse

# Clone repository (if not already present)
if [ ! -d ".git" ]; then
    echo "📥 Cloning repository..."
    git clone https://github.com/yourusername/kingdupattahouse.git .
fi

# Pull latest changes
echo "🔄 Pulling latest changes..."
git pull origin main

# Create environment file
echo "⚙️ Creating environment file..."
cat > .env << EOF
DEBUG=False
SECRET_KEY=your-secret-key-here
DB_NAME=kingdupattahouse
DB_USER=postgres
DB_PASSWORD=your-db-password
DB_HOST=localhost
DB_PORT=5432
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_STORAGE_BUCKET_NAME=kingdupattahouse-static
AWS_S3_REGION_NAME=ap-south-1
REDIS_URL=redis://localhost:6379/1
EMAIL_HOST=email-smtp.ap-south-1.amazonaws.com
EMAIL_HOST_USER=your-ses-user
EMAIL_HOST_PASSWORD=your-ses-password
DEFAULT_FROM_EMAIL=noreply@kingduppatahouse.in
EOF

# Build and start services
echo "🏗️ Building and starting services..."
docker-compose down
docker-compose build
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 30

# Run migrations
echo "🗄️ Running database migrations..."
docker-compose exec web python manage.py migrate --settings=womens_wear_ecommerce.settings_production

# Create superuser (optional)
echo "👤 Creating superuser..."
docker-compose exec web python manage.py createsuperuser --settings=womens_wear_ecommerce.settings_production || true

# Collect static files
echo "📁 Collecting static files..."
docker-compose exec web python manage.py collectstatic --noinput --settings=womens_wear_ecommerce.settings_production

# Configure Nginx
echo "🌐 Configuring Nginx..."
sudo cp nginx.conf /etc/nginx/sites-available/kingdupattahouse
sudo ln -sf /etc/nginx/sites-available/kingdupattahouse /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl reload nginx

# Setup SSL Certificate
echo "🔒 Setting up SSL certificate..."
sudo certbot --nginx -d kingduppatahouse.in -d www.kingduppatahouse.in --non-interactive --agree-tos --email admin@kingduppatahouse.in

# Setup log rotation
echo "📝 Setting up log rotation..."
sudo tee /etc/logrotate.d/kingdupattahouse << EOF
/var/log/django/*.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 644 www-data www-data
}
EOF

# Setup systemd service for auto-start
echo "🔄 Setting up systemd service..."
sudo tee /etc/systemd/system/kingdupattahouse.service << EOF
[Unit]
Description=King Dupatta House Django App
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/var/www/kingdupattahouse
ExecStart=/usr/local/bin/docker-compose up -d
ExecStop=/usr/local/bin/docker-compose down
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl enable kingdupattahouse.service
sudo systemctl start kingdupattahouse.service

# Setup monitoring
echo "📊 Setting up monitoring..."
sudo apt-get install -y htop iotop

# Create backup script
echo "💾 Creating backup script..."
sudo tee /usr/local/bin/backup_kingdupattahouse.sh << EOF
#!/bin/bash
DATE=\$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/var/backups/kingdupattahouse"
mkdir -p \$BACKUP_DIR

# Backup database
docker-compose exec -T db pg_dump -U postgres kingdupattahouse > \$BACKUP_DIR/db_\$DATE.sql

# Backup media files
tar -czf \$BACKUP_DIR/media_\$DATE.tar.gz /var/www/kingdupattahouse/media/

# Keep only last 7 days of backups
find \$BACKUP_DIR -name "*.sql" -mtime +7 -delete
find \$BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete
EOF

sudo chmod +x /usr/local/bin/backup_kingdupattahouse.sh

# Setup cron job for backups
echo "⏰ Setting up backup cron job..."
(crontab -l 2>/dev/null; echo "0 2 * * * /usr/local/bin/backup_kingdupattahouse.sh") | crontab -

echo "✅ Deployment completed successfully!"
echo "🌐 Your website is now available at:"
echo "   - https://kingduppatahouse.in"
echo "   - https://www.kingduppatahouse.in"
echo "   - http://3.109.208.181"
echo ""
echo "📊 Useful commands:"
echo "   - View logs: docker-compose logs -f"
echo "   - Restart services: docker-compose restart"
echo "   - Update code: git pull && docker-compose up -d --build"
echo "   - Database shell: docker-compose exec web python manage.py shell"
echo ""
echo "🔧 Next steps:"
echo "   1. Update .env file with your actual credentials"
echo "   2. Configure AWS S3 bucket for static/media files"
echo "   3. Setup AWS RDS database"
echo "   4. Configure domain DNS settings"
echo "   5. Test the website functionality"
