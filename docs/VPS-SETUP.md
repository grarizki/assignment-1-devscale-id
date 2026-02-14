# VPS Setup Guide for FastAPI Application

## Quick Diagnostics

If your service is failing, run these commands on your VPS:

```bash
# Check which services failed
systemctl --failed

# Check your FastAPI service status
systemctl status stocksOption.service

# View recent logs
journalctl -xeu stocksOption.service -n 50

# Check if port 8000 is available
sudo lsof -i :8000

# Check nginx status
systemctl status nginx
```

## Step-by-Step VPS Setup

### 1. Install Dependencies

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3.12
sudo apt install -y python3.12 python3.12-venv python3-pip

# Install uv (fast Python package installer)
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.cargo/env

# Install nginx
sudo apt install -y nginx

# Install git
sudo apt install -y git
```

### 2. Clone Your Repository

```bash
# Navigate to home directory
cd ~

# Clone your repository (replace with your repo URL)
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git assignment-1
cd assignment-1

# Create virtual environment
python3.12 -m venv .venv
source .venv/bin/activate

# Install dependencies
uv sync
```

### 3. Setup Environment Variables

```bash
# Create .env file
nano .env
```

Add your configuration:
```env
DATABASE_URL=sqlite:///./database.db
APP_NAME=Stock Options API
VERSION=1.0.0
```

### 4. Run Database Migrations

```bash
# Make sure you're in the project directory
cd ~/assignment-1
source .venv/bin/activate

# Run migrations
alembic upgrade head

# Optional: Seed initial data
curl -X POST http://localhost:8000/stocks/seed
```

### 5. Create Systemd Service

Create the service file:

```bash
sudo nano /etc/systemd/system/stocksOption.service
```

Add this configuration:

```ini
[Unit]
Description=Stock Options FastAPI Application
After=network.target

[Service]
Type=simple
User=grarizki
Group=grarizki
WorkingDirectory=/home/grarizki/assignment-1
Environment="PATH=/home/grarizki/assignment-1/.venv/bin"
EnvironmentFile=/home/grarizki/assignment-1/.env
ExecStart=/home/grarizki/assignment-1/.venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

**Important**: Replace `grarizki` with your actual username if different.

### 6. Enable and Start Service

```bash
# Reload systemd to recognize new service
sudo systemctl daemon-reload

# Enable service to start on boot
sudo systemctl enable stocksOption.service

# Start the service
sudo systemctl start stocksOption.service

# Check status
sudo systemctl status stocksOption.service
```

### 7. Configure Nginx

Create nginx configuration:

```bash
sudo nano /etc/nginx/sites-available/stocksOption
```

Add this configuration:

```nginx
server {
    listen 80;
    server_name your-domain.com;  # Replace with your domain or server IP

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # WebSocket support (if needed)
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

Enable the site:

```bash
# Create symbolic link
sudo ln -s /etc/nginx/sites-available/stocksOption /etc/nginx/sites-enabled/

# Remove default site (optional)
sudo rm /etc/nginx/sites-enabled/default

# Test nginx configuration
sudo nginx -t

# Reload nginx
sudo systemctl reload nginx
```

### 8. Configure Firewall (if enabled)

```bash
# Allow HTTP traffic
sudo ufw allow 'Nginx Full'

# Allow SSH (if not already allowed)
sudo ufw allow OpenSSH

# Enable firewall
sudo ufw enable
```

### 9. Setup Sudo Permissions for Deployment

Allow your user to restart services without password:

```bash
sudo visudo
```

Add at the end:
```
grarizki ALL=(ALL) NOPASSWD: /bin/systemctl restart stocksOption.service
grarizki ALL=(ALL) NOPASSWD: /bin/systemctl reload nginx
grarizki ALL=(ALL) NOPASSWD: /bin/systemctl status stocksOption.service
```

## Common Issues and Solutions

### Service Fails to Start

**Check logs:**
```bash
journalctl -xeu stocksOption.service -n 50
```

**Common causes:**

1. **Python not found**
   - Verify path in service file: `/home/grarizki/assignment-1/.venv/bin/python3`
   - Check with: `ls -la /home/grarizki/assignment-1/.venv/bin/`

2. **Module not found**
   - Reinstall dependencies: `cd ~/assignment-1 && source .venv/bin/activate && uv sync`

3. **Port already in use**
   - Check: `sudo lsof -i :8000`
   - Kill process: `sudo kill -9 PID`

4. **Database file permissions**
   - Fix: `chmod 644 ~/assignment-1/database.db`

5. **Environment file not found**
   - Create: `touch ~/assignment-1/.env`
   - Add required variables

### Service Starts but Crashes

**View live logs:**
```bash
journalctl -fu stocksOption.service
```

**Restart service:**
```bash
sudo systemctl restart stocksOption.service
```

### Nginx Configuration Issues

**Test config:**
```bash
sudo nginx -t
```

**Common fixes:**
```bash
# Check nginx error logs
sudo tail -f /var/log/nginx/error.log

# Restart nginx
sudo systemctl restart nginx
```

### Permission Denied Errors

```bash
# Fix ownership
sudo chown -R grarizki:grarizki ~/assignment-1

# Fix permissions
chmod +x ~/assignment-1/.venv/bin/uvicorn
```

## Verification Checklist

After setup, verify everything works:

```bash
# 1. Service is running
sudo systemctl status stocksOption.service
# Should show: Active: active (running)

# 2. App responds locally
curl http://127.0.0.1:8000/openapi.json
# Should return JSON

# 3. Nginx is running
sudo systemctl status nginx
# Should show: Active: active (running)

# 4. App accessible through nginx
curl http://localhost/openapi.json
# Should return JSON

# 5. Check from external network
curl http://YOUR_SERVER_IP/openapi.json
# Should return JSON
```

## Manual Testing

```bash
# Test FastAPI directly (without systemd)
cd ~/assignment-1
source .venv/bin/activate
uvicorn app.main:app --host 127.0.0.1 --port 8000

# In another terminal, test it
curl http://localhost:8000/openapi.json
```

## Monitoring

```bash
# View real-time logs
journalctl -fu stocksOption.service

# View nginx access logs
sudo tail -f /var/log/nginx/access.log

# View nginx error logs
sudo tail -f /var/log/nginx/error.log

# Check service resource usage
systemctl status stocksOption.service
```

## Updating the Application

```bash
cd ~/assignment-1
git pull origin master
source .venv/bin/activate
uv sync
alembic upgrade head
sudo systemctl restart stocksOption.service
```

Or use the deployment script:
```bash
cd ~/assignment-1
./scripts/deploy.sh
```
