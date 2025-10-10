#!/bin/bash

# Quick fix for Docker permissions
echo "🔧 Fixing Docker permissions..."

# Add user to docker group
sudo usermod -aG docker $USER

# Fix Docker socket permissions
sudo chmod 666 /var/run/docker.sock

# Restart Docker service
sudo systemctl restart docker

# Wait for Docker to start
sleep 5

# Test Docker
if docker ps > /dev/null 2>&1; then
    echo "✅ Docker is working now!"
    echo "You can now run the deployment script again."
else
    echo "❌ Docker still has permission issues."
    echo "Try logging out and back in, then run:"
    echo "newgrp docker"
fi
