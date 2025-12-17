# Deployment Guide

## Local Development

### Quick Start
```bash
# Install dependencies
pip3 install -r requirements.txt

# Run development server
./run_dev.sh
# OR
cd backend && python3 app.py
```

Server runs at: `http://127.0.0.1:5000`

---

## Production Deployment

### Option 1: VPS with Gunicorn + Nginx

#### Step 1: Server Setup
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3 python3-pip python3-venv nginx ffmpeg -y
```

#### Step 2: Deploy Application
```bash
# Clone or upload your code
cd /var/www
sudo mkdir media-utility
sudo chown $USER:$USER media-utility
cd media-utility

# Upload your files here
# Then create virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
```

#### Step 3: Configure Gunicorn
```bash
# Test Gunicorn
gunicorn -c gunicorn_config.py backend.app:app

# Create systemd service
sudo nano /etc/systemd/system/media-utility.service
```

Service file content:
```ini
[Unit]
Description=Media Utility Gunicorn
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/media-utility
Environment="PATH=/var/www/media-utility/venv/bin"
ExecStart=/var/www/media-utility/venv/bin/gunicorn -c gunicorn_config.py backend.app:app

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start
sudo systemctl enable media-utility
sudo systemctl start media-utility
```

#### Step 4: Configure Nginx
```bash
sudo nano /etc/nginx/sites-available/media-utility
```

Use the example from `nginx.conf.example`, then:
```bash
sudo ln -s /etc/nginx/sites-available/media-utility /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

#### Step 5: SSL (Let's Encrypt)
```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your-domain.com
```

---

### Option 2: Docker Deployment

#### Build and Run
```bash
# Build image
docker build -t media-utility .

# Run container
docker run -d \
  -p 5000:5000 \
  -v $(pwd)/downloads:/app/downloads \
  --name media-utility \
  media-utility
```

#### Docker Compose
```bash
docker-compose up -d
```

---

### Option 3: Cloud Platforms

#### Heroku
```bash
# Install Heroku CLI
# Create Procfile
echo "web: gunicorn -c gunicorn_config.py backend.app:app" > Procfile

# Deploy
heroku create
git push heroku main
```

#### DigitalOcean App Platform
1. Connect GitHub repository
2. Select Python buildpack
3. Set start command: `gunicorn -c gunicorn_config.py backend.app:app`
4. Deploy

#### AWS EC2
- Follow VPS instructions above
- Use Elastic IP for static address
- Configure security groups (port 80, 443, 5000)

---

## Environment Variables

Create `.env` file:
```bash
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=your-secret-key-here
PORT=5000
MAX_REQUESTS_PER_HOUR=10
MAX_DOWNLOAD_SIZE_MB=500
```

---

## Security Checklist

- [ ] Change `SECRET_KEY` in production
- [ ] Set `FLASK_DEBUG=False`
- [ ] Configure firewall (UFW)
- [ ] Enable SSL/HTTPS
- [ ] Set up rate limiting
- [ ] Regular backups
- [ ] Monitor logs
- [ ] Update dependencies regularly

---

## Monitoring

### Logs
```bash
# Gunicorn logs
sudo journalctl -u media-utility -f

# Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Health Check
```bash
curl http://your-domain.com/api/health
```

---

## Troubleshooting

### Port Already in Use
```bash
sudo lsof -i :5000
sudo kill <PID>
```

### Permission Denied
```bash
sudo chown -R www-data:www-data /var/www/media-utility
sudo chmod -R 755 /var/www/media-utility
```

### Gunicorn Not Found
```bash
source venv/bin/activate
pip install gunicorn
```

---

## Backup Strategy

```bash
# Backup downloads
tar -czf backups/downloads-$(date +%Y%m%d).tar.gz downloads/

# Backup database (if added later)
# Backup configuration files
```

---

## Scaling

### Horizontal Scaling
- Use load balancer (Nginx, HAProxy)
- Multiple Gunicorn workers
- Redis for session storage

### Vertical Scaling
- Increase server resources
- Optimize database queries
- Use CDN for static files

