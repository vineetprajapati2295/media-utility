# Media Utility Platform

A complete web-based media utility platform for personal and educational use.

## Features

- ✅ Modern dark-themed UI
- ✅ Video and audio download
- ✅ Quality/format selection
- ✅ URL validation
- ✅ Progress tracking
- ✅ Rate limiting
- ✅ Security features
- ✅ Responsive design

## Quick Start

### Installation

**Option 1: Using setup script (recommended)**
```bash
./setup.sh
```

**Option 2: Manual setup**
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Development

```bash
# Activate virtual environment (if not already active)
source venv/bin/activate

# Start development server
./run_dev.sh
# OR
python3 -m backend.app
```

Then open `http://127.0.0.1:5000` in your browser.

### Production

```bash
# Using Gunicorn
./run.sh

# Using Docker
docker-compose up -d
```

## Project Structure

```
yout/
├── backend/          # Python Flask backend
│   ├── app.py       # Main application
│   ├── config.py    # Configuration
│   ├── download_service.py  # Download logic
│   ├── rate_limiter.py     # Rate limiting
│   └── security.py         # Security utilities
├── frontend/        # Static web files
│   ├── index.html   # Main page
│   ├── styles.css   # Styling
│   └── app.js       # JavaScript
├── downloads/       # Downloaded files (auto-created)
└── requirements.txt # Python dependencies
```

## API Endpoints

- `GET /api/health` - Health check
- `POST /api/validate` - Validate URL
- `POST /api/download` - Download media
- `GET /api/file/<filename>` - Serve file

## Configuration

Edit `backend/config.py` or use environment variables:

- `FLASK_PORT` - Server port (default: 5000)
- `MAX_REQUESTS_PER_HOUR` - Rate limit (default: 10)
- `MAX_DOWNLOAD_SIZE_MB` - Size limit (default: 500)

## Documentation

- `ARCHITECTURE.md` - Project architecture
- `PHASE2_GUIDE.md` - Backend API details
- `DEPLOYMENT.md` - Deployment guide
- `MONETIZATION.md` - Monetization options
- `QUICKSTART.md` - Quick start guide

## Legal Notice

This tool is for personal and educational use only. Users are responsible for ensuring they have the right to download content. Do not download copyrighted material without permission.

## License

Educational use only.
