#!/bin/bash

# Clean up everything
echo "🧹 Cleaning up everything..."

# Stop all services
sudo systemctl stop kingdupattahouse || true
sudo systemctl stop nginx || true

# Remove service files
sudo rm -f /etc/systemd/system/kingdupattahouse.service
sudo rm -f /etc/nginx/sites-available/kingdupattahouse
sudo rm -f /etc/nginx/sites-enabled/kingdupattahouse
sudo rm -f /etc/nginx/sites-enabled/default

# Remove project directory
sudo rm -rf /home/ubuntu/kingdupattahouse

# Remove log directory
sudo rm -rf /var/log/django

# Restart services
sudo systemctl daemon-reload
sudo systemctl restart nginx

echo "✅ Cleanup completed!"
