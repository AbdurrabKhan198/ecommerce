# 🚀 One-Command Deployment for King Dupatta House

## Quick Deploy (Copy & Paste)

```bash
curl -sSL https://raw.githubusercontent.com/AbdurrabKhan198/ecommerce/main/auto_deploy.sh | bash
```

## What This Does Automatically:

✅ **System Setup**
- Updates Ubuntu packages
- Installs Docker & Docker Compose
- Installs Nginx & Certbot
- Installs PostgreSQL client

✅ **Application Deployment**
- Clones your GitHub repository
- Creates environment configuration
- Builds Docker containers
- Starts all services

✅ **Database Setup**
- Creates PostgreSQL database
- Runs Django migrations
- Creates admin user (admin/admin123)
- Loads sample data

✅ **Web Server Configuration**
- Configures Nginx reverse proxy
- Sets up SSL certificates
- Configures auto-start service
- Sets up backup system

✅ **Final Result**
- Website live at: `http://3.109.208.181`
- Admin panel: `http://3.109.208.181/admin/`
- Domain ready: `kingduppatahouse.in`

## Prerequisites:

1. **Ubuntu 20.04+ server** (your AWS EC2)
2. **GitHub repository** with your code
3. **Domain DNS** pointing to `3.109.208.181`

## After Deployment:

### 1. Update GitHub Repository URL
Edit `auto_deploy.sh` line 67:
```bash
GITHUB_REPO="https://github.com/YOURUSERNAME/kingdupattahouse.git"
```

### 2. Configure Domain DNS
Point your domain to the server:
```
A Record: @ → 3.109.208.181
A Record: www → 3.109.208.181
```

### 3. Get SSL Certificate
```bash
sudo certbot --nginx -d kingduppatahouse.in -d www.kingduppatahouse.in
```

### 4. Update Environment Variables
Edit `.env` file with your production settings:
```bash
nano /var/www/kingdupattahouse/.env
```

## Management Commands:

```bash
# View logs
cd /var/www/kingdupattahouse && docker-compose logs -f

# Restart services
cd /var/www/kingdupattahouse && docker-compose restart

# Update code
cd /var/www/kingdupattahouse && git pull && docker-compose up -d --build

# Stop services
cd /var/www/kingdupattahouse && docker-compose down

# Access database
cd /var/www/kingdupattahouse && docker-compose exec db psql -U postgres -d kingdupattahouse
```

## Default Credentials:

- **Admin Username**: admin
- **Admin Password**: admin123
- **Admin Email**: admin@kingduppatahouse.in

## Features Included:

🌐 **Dynamic Website**
- Dynamic product images
- Dynamic categories and content
- Dynamic cart and checkout
- Mobile responsive design

🔒 **Security**
- SSL/HTTPS ready
- Security headers
- CSRF protection
- Secure sessions

📊 **Admin Panel**
- Product management
- Order management
- User management
- Content management

🚀 **Performance**
- Docker containerization
- Nginx reverse proxy
- Static file optimization
- Database optimization

## Support:

If you encounter any issues:
1. Check logs: `docker-compose logs -f`
2. Restart services: `docker-compose restart`
3. Check disk space: `df -h`
4. Check memory: `free -h`

## 🎉 Ready for Client Showcase!

Your King Dupatta House e-commerce website is now ready to showcase to your client with all dynamic features working perfectly!
