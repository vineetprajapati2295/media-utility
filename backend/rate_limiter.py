"""
Rate Limiting Module

Implements rate limiting to prevent abuse.
Uses in-memory storage (simple) or can be extended to use Redis.
"""

from datetime import datetime, timedelta
from typing import Dict, Tuple
from collections import defaultdict
from backend.config import MAX_REQUESTS_PER_HOUR


class RateLimiter:
    """
    Simple rate limiter using sliding window.
    Tracks requests per IP address.
    """
    
    def __init__(self, max_requests: int = MAX_REQUESTS_PER_HOUR, window_seconds: int = 3600):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: Dict[str, list] = defaultdict(list)
        self._cleanup_interval = 300  # Clean up old entries every 5 minutes
        self._last_cleanup = datetime.now()
    
    def is_allowed(self, client_ip: str) -> Tuple[bool, str]:
        """
        Check if request is allowed for given IP.
        
        Args:
            client_ip: Client's IP address
            
        Returns:
            Tuple of (allowed, message)
        """
        now = datetime.now()
        
        # Cleanup old entries periodically
        if (now - self._last_cleanup).total_seconds() > self._cleanup_interval:
            self._cleanup_old_entries()
            self._last_cleanup = now
        
        # Get requests for this IP
        ip_requests = self.requests[client_ip]
        
        # Remove requests outside the time window
        cutoff_time = now - timedelta(seconds=self.window_seconds)
        ip_requests[:] = [req_time for req_time in ip_requests if req_time > cutoff_time]
        
        # Check if limit exceeded
        if len(ip_requests) >= self.max_requests:
            remaining = self._get_remaining_time(ip_requests[0])
            return False, f"Rate limit exceeded. Try again in {remaining} seconds."
        
        # Add current request
        ip_requests.append(now)
        
        return True, "OK"
    
    def _get_remaining_time(self, oldest_request: datetime) -> int:
        """Calculate remaining time until oldest request expires."""
        expiry_time = oldest_request + timedelta(seconds=self.window_seconds)
        remaining = (expiry_time - datetime.now()).total_seconds()
        return max(0, int(remaining))
    
    def _cleanup_old_entries(self):
        """Remove entries for IPs with no recent requests."""
        now = datetime.now()
        cutoff_time = now - timedelta(seconds=self.window_seconds * 2)
        
        ips_to_remove = []
        for ip, requests in self.requests.items():
            if not requests or (requests and max(requests) < cutoff_time):
                ips_to_remove.append(ip)
        
        for ip in ips_to_remove:
            del self.requests[ip]
    
    def get_remaining_requests(self, client_ip: str) -> int:
        """Get number of remaining requests for an IP."""
        now = datetime.now()
        cutoff_time = now - timedelta(seconds=self.window_seconds)
        ip_requests = self.requests.get(client_ip, [])
        valid_requests = [r for r in ip_requests if r > cutoff_time]
        return max(0, self.max_requests - len(valid_requests))


# Global rate limiter instance
rate_limiter = RateLimiter()

