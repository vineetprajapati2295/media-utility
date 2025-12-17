"""
Flask Application - Main Entry Point

This is the heart of our backend. It handles:
- HTTP requests from the frontend
- API endpoints for downloading
- Error handling and responses

Why Flask?
- Simple and beginner-friendly
- Perfect for REST APIs
- Easy to deploy
- Great documentation
"""

from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
from pathlib import Path
from typing import Tuple
import os
from backend.config import (
    FLASK_DEBUG, 
    FLASK_PORT, 
    FLASK_HOST,
    FLASK_ENV,
    SECRET_KEY,
    DOWNLOADS_DIR,
    MAX_REQUESTS_PER_HOUR
)
from backend.download_service import DownloadService
from backend.rate_limiter import rate_limiter
from backend.security import sanitize_filename, is_safe_path, get_client_ip, validate_domain

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

# Enable CORS (Cross-Origin Resource Sharing)
# Allow all origins in production (since frontend is served from same origin)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Initialize download service
download_service = DownloadService()


# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.route('/')
def index():
    """
    Root endpoint - serves frontend HTML.
    """
    from flask import send_from_directory
    import os
    frontend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend')
    return send_from_directory(frontend_dir, 'index.html')


@app.route('/api/validate', methods=['POST'])
def validate_url():
    """
    Validate if a URL can be downloaded.
    
    Request body:
        {
            "url": "https://..."
        }
    
    Response:
        {
            "valid": true/false,
            "message": "error message if invalid"
        }
    """
    try:
        data = request.get_json()
        
        if not data or 'url' not in data:
            return jsonify({
                'valid': False,
                'message': 'URL is required'
            }), 400
        
        url = data['url']
        
        # Domain validation
        if not validate_domain(url):
            return jsonify({
                'valid': False,
                'message': 'Domain not allowed'
            }), 403
        
        is_valid, error_msg = download_service.validate_url(url)
        
        if is_valid:
            # Get video info if valid
            try:
                video_info = download_service.get_video_info(url)
                return jsonify({
                    'valid': True,
                    'message': 'URL is valid',
                    'video_info': video_info
                })
            except Exception as e:
                return jsonify({
                    'valid': True,
                    'message': 'URL is valid but info unavailable',
                    'error': str(e)
                })
        else:
            return jsonify({
                'valid': False,
                'message': error_msg or 'Invalid URL'
            }), 400
            
    except Exception as e:
        return jsonify({
            'valid': False,
            'message': f'Server error: {str(e)}'
        }), 500


@app.route('/api/download', methods=['POST'])
def download():
    """
    Download video or audio from URL.
    
    Request body:
        {
            "url": "https://...",
            "format_id": "optional format ID",
            "audio_only": true/false
        }
    
    Response:
        {
            "status": "success/error",
            "message": "...",
            "filename": "...",
            "download_url": "/api/file/..."
        }
    """
    try:
        data = request.get_json()
        
        if not data or 'url' not in data:
            return jsonify({
                'status': 'error',
                'message': 'URL is required'
            }), 400
        
        url = data['url']
        format_id = data.get('format_id')
        audio_only = data.get('audio_only', False)
        
        # Domain validation
        if not validate_domain(url):
            return jsonify({
                'status': 'error',
                'message': 'Domain not allowed'
            }), 403
        
        # Validate URL first
        is_valid, error_msg = download_service.validate_url(url)
        if not is_valid:
            return jsonify({
                'status': 'error',
                'message': error_msg or 'Invalid URL'
            }), 400
        
        # Check rate limit
        client_ip = get_client_ip(request)
        allowed, msg = rate_limiter.is_allowed(client_ip)
        if not allowed:
            return jsonify({
                'status': 'error',
                'message': msg,
                'rate_limit_exceeded': True
            }), 429
        
        # Download
        result = download_service.download_video(
            url=url,
            format_id=format_id,
            audio_only=audio_only
        )
        
        # Return success with download URL
        return jsonify({
            'status': 'success',
            'message': 'Download completed',
            'filename': result['filename'],
            'filesize': result['filesize'],
            'title': result['title'],
            'download_url': f"/api/file/{result['filename']}"
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/file/<filename>', methods=['GET'])
def serve_file(filename):
    """
    Serve downloaded files.
    
    Security: Only serves files from downloads directory.
    Prevents directory traversal attacks.
    """
    try:
        # Sanitize filename
        safe_filename = sanitize_filename(filename)
        
        # Security: Prevent directory traversal
        file_path = DOWNLOADS_DIR / safe_filename
        
        # Ensure the file is actually in downloads directory
        if not is_safe_path(file_path):
            return jsonify({
                'status': 'error',
                'message': 'Invalid file path'
            }), 403
        
        if not file_path.exists():
            return jsonify({
                'status': 'error',
                'message': 'File not found'
            }), 404
        
        # Send file to client
        return send_file(
            str(file_path),
            as_attachment=True,
            download_name=safe_filename
        )
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Health check endpoint.
    Useful for monitoring and deployment checks.
    """
    client_ip = get_client_ip(request)
    remaining = rate_limiter.get_remaining_requests(client_ip)
    
    return jsonify({
        'status': 'healthy',
        'downloads_dir': str(DOWNLOADS_DIR),
        'downloads_dir_exists': DOWNLOADS_DIR.exists(),
        'rate_limit': {
            'max_requests': MAX_REQUESTS_PER_HOUR,
            'remaining': remaining
        }
    })


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({
        'status': 'error',
        'message': 'Endpoint not found'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({
        'status': 'error',
        'message': 'Internal server error'
    }), 500


# Serve static frontend files
@app.route('/styles.css')
def serve_css():
    """Serve CSS file."""
    import os
    frontend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend')
    return send_from_directory(frontend_dir, 'styles.css')


@app.route('/app.js')
def serve_js():
    """Serve JavaScript file."""
    import os
    frontend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend')
    return send_from_directory(frontend_dir, 'app.js')


@app.route('/ads.js')
def serve_ads_js():
    """Serve ads JavaScript file."""
    import os
    frontend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend')
    return send_from_directory(frontend_dir, 'ads.js')


@app.route('/config.js')
def serve_config_js():
    """Serve config JavaScript file."""
    import os
    frontend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend')
    return send_from_directory(frontend_dir, 'config.js')


# ============================================================================
# RUN SERVER
# ============================================================================

if __name__ == '__main__':
    """
    Run the Flask development server.
    
    In production, use a WSGI server like Gunicorn:
    gunicorn -w 4 -b 0.0.0.0:5000 backend.app:app
    
    To run from project root:
    python3 -m backend.app
    OR
    python3 backend/app.py (if PYTHONPATH includes project root)
    """
    import sys
    import os
    
    # Ensure we can import backend modules
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    
    print(f"""
    ╔═══════════════════════════════════════════════════════╗
    ║   Media Utility Platform - Backend Server             ║
    ╠═══════════════════════════════════════════════════════╣
    ║   Server running at: http://{FLASK_HOST}:{FLASK_PORT:<5}        ║
    ║   Environment: {FLASK_ENV:<30} ║
    ║   Debug mode: {str(FLASK_DEBUG):<30} ║
    ╚═══════════════════════════════════════════════════════╝
    """)
    
    app.run(
        host=FLASK_HOST,
        port=FLASK_PORT,
        debug=FLASK_DEBUG
    )
