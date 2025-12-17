"""
Security Utilities

Additional security functions for the application.
"""

import re
from pathlib import Path
from urllib.parse import urlparse
from backend.config import DOWNLOADS_DIR, ALLOWED_DOMAINS


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename to prevent directory traversal and invalid characters.
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    # Remove path components
    filename = Path(filename).name
    
    # Remove invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    
    # Limit length
    if len(filename) > 255:
        name, ext = Path(filename).stem, Path(filename).suffix
        filename = name[:255-len(ext)] + ext
    
    return filename


def is_safe_path(file_path: Path) -> bool:
    """
    Check if file path is safe (within downloads directory).
    
    Args:
        file_path: Path to check
        
    Returns:
        True if safe, False otherwise
    """
    try:
        # Resolve to absolute path
        resolved = file_path.resolve()
        downloads_resolved = DOWNLOADS_DIR.resolve()
        
        # Check if path is within downloads directory
        return str(resolved).startswith(str(downloads_resolved))
    except Exception:
        return False


def validate_domain(url: str) -> bool:
    """
    Validate if URL domain is allowed.
    
    Args:
        url: URL to validate
        
    Returns:
        True if allowed, False otherwise
    """
    if not ALLOWED_DOMAINS:
        return True  # All domains allowed if list is empty
    
    try:
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        
        # Remove port if present
        if ':' in domain:
            domain = domain.split(':')[0]
        
        return domain in [d.lower() for d in ALLOWED_DOMAINS if d]
    except Exception:
        return False


def get_client_ip(request) -> str:
    """
    Get client IP address from request.
    Handles proxies and load balancers.
    
    Args:
        request: Flask request object
        
    Returns:
        Client IP address
    """
    # Check for forwarded IP (from proxy/load balancer)
    if request.headers.get('X-Forwarded-For'):
        return request.headers.get('X-Forwarded-For').split(',')[0].strip()
    
    if request.headers.get('X-Real-IP'):
        return request.headers.get('X-Real-IP')
    
    # Fallback to remote address
    return request.remote_addr or '127.0.0.1'

