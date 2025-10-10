#!/bin/bash

# Quick Deployment Script for King Dupatta House
# For immediate deployment to AWS server

echo "🚀 Quick Deployment to AWS Server"
echo "Domain: kingduppatahouse.in"
echo "IP: 3.109.208.181"
echo ""

# Make deployment script executable
chmod +x deploy_aws.sh

# Create necessary directories
mkdir -p ssl
mkdir -p logs

# Create a simple SSL certificate for testing (replace with real certificate later)
echo "🔒 Creating temporary SSL certificate..."
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout ssl/key.pem \
    -out ssl/cert.pem \
    -subj "/C=IN/ST=UP/L=Lucknow/O=King Dupatta House/CN=kingduppatahouse.in"

echo "📦 Building Docker images..."
docker-compose build

echo "🗄️ Starting services..."
docker-compose up -d

echo "⏳ Waiting for services to start..."
sleep 30

echo "🔧 Running database migrations..."
docker-compose exec web python manage.py migrate --settings=womens_wear_ecommerce.settings_production

echo "👤 Creating superuser (optional)..."
echo "You can create a superuser by running:"
echo "docker-compose exec web python manage.py createsuperuser --settings=womens_wear_ecommerce.settings_production"

echo "📁 Collecting static files..."
docker-compose exec web python manage.py collectstatic --noinput --settings=womens_wear_ecommerce.settings_production

echo "🌱 Loading sample data..."
docker-compose exec web python manage.py create_sample_categories --settings=womens_wear_ecommerce.settings_production
docker-compose exec web python manage.py create_sample_products --settings=womens_wear_ecommerce.settings_production
docker-compose exec web python manage.py populate_diverse_images --settings=womens_wear_ecommerce.settings_production

echo "✅ Deployment completed!"
echo ""
echo "🌐 Your website should now be accessible at:"
echo "   - http://3.109.208.181"
echo "   - https://kingduppatahouse.in (after DNS setup)"
echo ""
echo "📊 Useful commands:"
echo "   - View logs: docker-compose logs -f"
echo "   - Restart: docker-compose restart"
echo "   - Stop: docker-compose down"
echo "   - Update: git pull && docker-compose up -d --build"
echo ""
echo "🔧 Next steps:"
echo "   1. Update .env file with your actual credentials"
echo "   2. Configure your domain DNS to point to 3.109.208.181"
echo "   3. Get a real SSL certificate from Let's Encrypt"
echo "   4. Configure AWS S3 for static files"
echo "   5. Setup AWS RDS database"
echo ""
echo "🎉 Your King Dupatta House website is ready for client showcase!"
