#!/bin/bash

# Deployment script for production VPS
# This script should be run on the VPS server

set -e  # Exit on error

echo "🚀 Starting deployment..."

# Navigate to project directory
cd "$(dirname "$0")/.." || exit 1

# Pull latest changes
echo "📥 Pulling latest code from master..."
git pull origin master

# Activate virtual environment and sync dependencies
echo "📦 Installing dependencies..."
source .venv/bin/activate
uv sync

# Run database migrations
echo "🗄️  Running database migrations..."
alembic upgrade head

# Restart the application service
echo "♻️  Restarting application service..."
sudo systemctl restart fastapi-app

# Reload nginx
echo "🔄 Reloading nginx..."
sudo systemctl reload nginx

# Check service status
echo "✅ Checking service status..."
sudo systemctl status fastapi-app --no-pager

echo "🎉 Deployment completed successfully!"
