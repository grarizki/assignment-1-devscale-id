# Deployment Guide

## GitHub Actions CI/CD Setup

This project uses GitHub Actions for automated testing and deployment to your VPS.

### Pipeline Overview

The CI/CD pipeline runs in two stages:

1. **Test & Lint** (runs on all pushes and PRs)
   - Checks code formatting with `ruff format --check`
   - Lints code with `ruff check`
   - Runs test suite with `pytest`

2. **Deploy to VPS** (runs only on master branch pushes after tests pass)
   - SSH into your VPS
   - Pull latest code
   - Install dependencies with `uv sync`
   - Run database migrations with `alembic upgrade head`
   - Restart application service
   - Reload nginx

### Required GitHub Secrets

To enable automatic deployment, add these secrets to your GitHub repository:

**Settings → Secrets and variables → Actions → New repository secret**

| Secret Name | Description | Example |
|------------|-------------|---------|
| `VPS_HOST` | Your VPS IP address or domain | `123.45.67.89` or `example.com` |
| `VPS_USERNAME` | SSH username for VPS | `ubuntu` or `root` |
| `VPS_SSH_KEY` | Private SSH key for authentication | Contents of `~/.ssh/id_rsa` |
| `VPS_PORT` | SSH port (optional, defaults to 22) | `22` |
| `VPS_PROJECT_PATH` | Absolute path to project on VPS | `/home/ubuntu/assignment-1` |
| `VPS_SERVICE_NAME` | Systemd service name for your app | `fastapi-app` |

### Setting up SSH Key

If you don't have an SSH key set up:

```bash
# On your local machine, generate SSH key pair
ssh-keygen -t ed25519 -C "github-actions"

# Copy the public key to your VPS
ssh-copy-id -i ~/.ssh/id_ed25519.pub user@your-vps-ip

# Copy the PRIVATE key content to GitHub secrets (VPS_SSH_KEY)
cat ~/.ssh/id_ed25519
```

### VPS Setup Requirements

On your VPS, ensure you have:

1. **Git repository cloned** at the path specified in `VPS_PROJECT_PATH`
2. **Python virtual environment** set up at `.venv`
3. **uv package manager** installed
4. **Systemd service** configured for your FastAPI app
5. **Nginx** configured as reverse proxy
6. **Sudo permissions** for the deployment user (for systemctl commands)

#### Example Systemd Service

Create `/etc/systemd/system/fastapi-app.service`:

```ini
[Unit]
Description=FastAPI Application
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/assignment-1
Environment="PATH=/home/ubuntu/assignment-1/.venv/bin"
ExecStart=/home/ubuntu/assignment-1/.venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable fastapi-app
sudo systemctl start fastapi-app
```

#### Example Nginx Configuration

Create `/etc/nginx/sites-available/fastapi-app`:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable the site:

```bash
sudo ln -s /etc/nginx/sites-available/fastapi-app /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### Manual Deployment

You can also deploy manually using the deployment script:

```bash
# On your VPS
./scripts/deploy.sh
```

### Testing the Pipeline

1. Push to a feature branch and create a PR - tests will run automatically
2. Merge to master - tests run, then deployment happens if tests pass
3. Check the "Actions" tab in your GitHub repository to see pipeline status

### Troubleshooting

**Deployment fails with "Permission denied"**
- Ensure the SSH key is correctly added to GitHub secrets
- Verify the key is in your VPS `~/.ssh/authorized_keys`

**Service restart fails**
- Check if the systemd service name matches `VPS_SERVICE_NAME`
- Ensure the deployment user has sudo privileges

**Tests fail**
- Run `uv run pytest -v` locally to debug
- Check the Actions tab for detailed error logs
