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
    # Use best video+audio or best (will merge if needed for Instagram, Twitter, etc.)
    'format': 'bestvideo+bestaudio/best',  # Merge video and audio for platforms like Instagram
    'outtmpl': str(DOWNLOADS_DIR / '%(title)s.%(ext)s'),  # Output filename template
    'quiet': False,  # Show progress
    'no_warnings': False,
    # Post-processors to merge video and audio when separate
    'postprocessors': [{
        'key': 'FFmpegVideoConvertor',
        'preferedformat': 'mp4',
    }],
    # Merge video and audio if separate streams
    'merge_output_format': 'mp4',
    # YouTube bot detection bypass - try mweb (mobile web) first, most reliable
    'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1',
    'extractor_args': {
        'youtube': {
            # Try mweb (mobile web) first - most reliable for avoiding bot detection
            'player_client': ['mweb', 'ios', 'android', 'web'],
            'player_skip': [],
        }
    },
    # Additional headers to look more legitimate
    'http_headers': {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-us,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
    },
    # Retry options
    'retries': 10,
    'fragment_retries': 10,
    'file_access_retries': 5,
    # Additional options
    'no_check_certificate': False,
    'prefer_insecure': False,
    'extract_flat': False,
}

# Create downloads directory if it doesn't exist
DOWNLOADS_DIR.mkdir(exist_ok=True)
