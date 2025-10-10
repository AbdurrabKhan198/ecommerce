# AWS Deployment Guide for King Dupatta House

## 🌐 Domain & Server Information
- **Domain**: kingduppatahouse.in
- **IP Address**: 3.109.208.181
- **Server**: Amazon AWS EC2

## 📋 Prerequisites

### 1. AWS Services Setup
- **EC2 Instance**: Ubuntu 22.04 LTS
- **RDS Database**: PostgreSQL 15
- **S3 Bucket**: For static and media files
- **Route 53**: DNS management
- **Certificate Manager**: SSL certificates

### 2. Required AWS Resources
```bash
# EC2 Instance (t3.medium recommended)
- Instance Type: t3.medium
- Storage: 20GB GP3
- Security Groups: HTTP (80), HTTPS (443), SSH (22)

# RDS Database
- Engine: PostgreSQL 15
- Instance: db.t3.micro
- Storage: 20GB GP2
- Security Group: Allow access from EC2

# S3 Bucket
- Bucket Name: kingdupattahouse-static
- Region: ap-south-1
- Public Read Access for static files
```

## 🚀 Deployment Steps

### Step 1: Server Setup
```bash
# Connect to your AWS server
ssh -i your-key.pem ubuntu@3.109.208.181

# Run the deployment script
chmod +x deploy_aws.sh
./deploy_aws.sh
```

### Step 2: Environment Configuration
Create `.env` file with your credentials:
```bash
# Database
DB_NAME=kingdupattahouse
DB_USER=postgres
DB_PASSWORD=your-secure-password
DB_HOST=your-rds-endpoint.amazonaws.com
DB_PORT=5432

# AWS S3
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_STORAGE_BUCKET_NAME=kingdupattahouse-static
AWS_S3_REGION_NAME=ap-south-1

# Email (SES)
EMAIL_HOST=email-smtp.ap-south-1.amazonaws.com
EMAIL_HOST_USER=your-ses-user
EMAIL_HOST_PASSWORD=your-ses-password
DEFAULT_FROM_EMAIL=noreply@kingduppatahouse.in

# Security
SECRET_KEY=your-django-secret-key
DEBUG=False
```

### Step 3: Database Setup
```bash
# Create database
docker-compose exec web python manage.py migrate --settings=womens_wear_ecommerce.settings_production

# Create superuser
docker-compose exec web python manage.py createsuperuser --settings=womens_wear_ecommerce.settings_production

# Load sample data
docker-compose exec web python manage.py create_sample_categories --settings=womens_wear_ecommerce.settings_production
docker-compose exec web python manage.py create_sample_products --settings=womens_wear_ecommerce.settings_production
docker-compose exec web python manage.py populate_diverse_images --settings=womens_wear_ecommerce.settings_production
```

### Step 4: SSL Certificate Setup
```bash
# Install Certbot
sudo apt-get install certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot --nginx -d kingduppatahouse.in -d www.kingduppatahouse.in
```

### Step 5: DNS Configuration
Configure your domain DNS settings:
```
Type: A
Name: @
Value: 3.109.208.181

Type: A
Name: www
Value: 3.109.208.181

Type: CNAME
Name: api
Value: kingduppatahouse.in
```

## 🔧 AWS Services Configuration

### S3 Bucket Setup
1. Create bucket: `kingdupattahouse-static`
2. Enable public read access
3. Configure CORS:
```json
[
    {
        "AllowedHeaders": ["*"],
        "AllowedMethods": ["GET", "HEAD"],
        "AllowedOrigins": ["*"],
        "ExposeHeaders": []
    }
]
```

### RDS Database Setup
1. Create PostgreSQL instance
2. Configure security group
3. Create database: `kingdupattahouse`
4. Note the endpoint for connection

### Route 53 DNS
1. Create hosted zone for `kingduppatahouse.in`
2. Add A records pointing to your EC2 IP
3. Configure CNAME for www subdomain

## 📊 Monitoring & Maintenance

### Health Checks
```bash
# Check application status
curl -f http://localhost:8000/health/

# Check database connection
docker-compose exec web python manage.py dbshell

# Check logs
docker-compose logs -f web
```

### Backup Strategy
```bash
# Database backup
docker-compose exec db pg_dump -U postgres kingdupattahouse > backup.sql

# Media files backup
tar -czf media_backup.tar.gz media/

# Automated backups (already configured in deploy script)
crontab -l  # Check backup cron job
```

### Performance Optimization
```bash
# Enable Redis caching
# Configure CDN for static files
# Setup database connection pooling
# Enable Gzip compression (already configured)
```

## 🔒 Security Checklist

- [ ] SSL certificate installed and working
- [ ] HTTPS redirect configured
- [ ] Security headers implemented
- [ ] Database credentials secured
- [ ] AWS credentials properly configured
- [ ] Firewall rules configured
- [ ] Regular security updates enabled
- [ ] Backup strategy implemented

## 🚨 Troubleshooting

### Common Issues
1. **Database Connection Error**
   ```bash
   # Check RDS security group
   # Verify database credentials
   # Test connection: telnet your-rds-endpoint 5432
   ```

2. **Static Files Not Loading**
   ```bash
   # Check S3 bucket permissions
   # Verify AWS credentials
   # Check CORS configuration
   ```

3. **SSL Certificate Issues**
   ```bash
   # Renew certificate: sudo certbot renew
   # Check certificate status: sudo certbot certificates
   ```

### Log Locations
- Application logs: `/var/log/django/`
- Nginx logs: `/var/log/nginx/`
- Docker logs: `docker-compose logs`

## 📈 Performance Monitoring

### Key Metrics to Monitor
- CPU usage
- Memory usage
- Database connections
- Response times
- Error rates

### Monitoring Tools
```bash
# Install monitoring tools
sudo apt-get install htop iotop nethogs

# View real-time stats
htop
iotop
```

## 🔄 Updates & Maintenance

### Code Updates
```bash
# Pull latest changes
git pull origin main

# Rebuild and restart
docker-compose down
docker-compose up -d --build

# Run migrations
docker-compose exec web python manage.py migrate --settings=womens_wear_ecommerce.settings_production
```

### Regular Maintenance
```bash
# Update system packages
sudo apt-get update && sudo apt-get upgrade

# Clean Docker images
docker system prune -a

# Check disk space
df -h
```

## 📞 Support & Contact

For deployment issues:
- Check logs: `docker-compose logs -f`
- Monitor resources: `htop`
- Test connectivity: `curl -I https://kingduppatahouse.in`

## 🎯 Post-Deployment Checklist

- [ ] Website loads correctly at https://kingduppatahouse.in
- [ ] SSL certificate is valid
- [ ] All pages are accessible
- [ ] Database is connected
- [ ] Static files are loading
- [ ] Email functionality works
- [ ] Admin panel is accessible
- [ ] Mobile responsiveness works
- [ ] Performance is acceptable
- [ ] Backup system is working

## 🚀 Go Live!

Your King Dupatta House e-commerce website is now ready for production! 

**Live URLs:**
- Main site: https://kingduppatahouse.in
- Admin panel: https://kingduppatahouse.in/admin/
- API: https://kingduppatahouse.in/api/

**Client Showcase:**
The website is now ready to showcase to your client with:
- ✅ Professional design
- ✅ Dynamic content
- ✅ Secure HTTPS
- ✅ Mobile responsive
- ✅ Fast loading
- ✅ SEO optimized
