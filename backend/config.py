"""
Configuration Settings for Media Utility Platform

This file centralizes all configuration values.
Why separate? Easy to change settings without touching main code.
"""

import os
from pathlib import Path

# Base directory (project root)
BASE_DIR = Path(__file__).parent.parent

# Flask Configuration
FLASK_ENV = os.getenv('FLASK_ENV', 'development')
FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
FLASK_PORT = int(os.getenv('FLASK_PORT', 5000))
FLASK_HOST = os.getenv('FLASK_HOST', '127.0.0.1')

# Secret Key (for session security - change in production!)
SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

# Download Settings
DOWNLOADS_DIR = BASE_DIR / 'downloads'
MAX_DOWNLOAD_SIZE_MB = int(os.getenv('MAX_DOWNLOAD_SIZE_MB', 500))
MAX_DOWNLOAD_SIZE_BYTES = MAX_DOWNLOAD_SIZE_MB * 1024 * 1024  # Convert to bytes

# Rate Limiting
MAX_REQUESTS_PER_HOUR = int(os.getenv('MAX_REQUESTS_PER_HOUR', 10))

# Allowed Domains (empty = allow all, for now)
ALLOWED_DOMAINS = os.getenv('ALLOWED_DOMAINS', '').split(',') if os.getenv('ALLOWED_DOMAINS') else []

# yt-dlp Options
YTDLP_OPTIONS = {
    'format': 'best',  # Best quality by default
    'outtmpl': str(DOWNLOADS_DIR / '%(title)s.%(ext)s'),  # Output filename template
    'quiet': False,  # Show progress
    'no_warnings': False,
}

# Create downloads directory if it doesn't exist
DOWNLOADS_DIR.mkdir(exist_ok=True)
