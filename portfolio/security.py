"""
Security middleware and utilities for Portfolio
"""

from django.http import HttpResponseForbidden
from django.core.cache import cache
from django.utils.deprecation import MiddlewareMixin
import time
import hashlib

class SecurityHeadersMiddleware(MiddlewareMixin):
    """
    Add security headers to all responses
    """
    def process_response(self, request, response):
        # Content Security Policy
        response['Content-Security-Policy'] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
            "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
            "img-src 'self' data: https:; "
            "font-src 'self' https://cdn.jsdelivr.net; "
            "connect-src 'self'; "
            "frame-ancestors 'none';"
        )
        
        # Additional security headers
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
        
        return response

class RateLimitMiddleware(MiddlewareMixin):
    """
    Rate limiting middleware for API endpoints
    """
    def process_request(self, request):
        # Only apply to contact form submissions
        if request.path == '/contact/' and request.method == 'POST':
            client_ip = self.get_client_ip(request)
            cache_key = f"rate_limit_{client_ip}"
            
            # Check current request count
            request_count = cache.get(cache_key, 0)
            
            if request_count >= 10:  # 10 requests per hour
                return HttpResponseForbidden("Rate limit exceeded. Please try again later.")
            
            # Increment counter
            cache.set(cache_key, request_count + 1, 3600)  # 1 hour
        
        return None
    
    def get_client_ip(self, request):
        """Get client IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

class SuspiciousActivityMiddleware(MiddlewareMixin):
    """
    Detect and block suspicious activity
    """
    def process_request(self, request):
        # Check for suspicious patterns
        user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
        path = request.path.lower()
        
        # Block common bot patterns
        bot_patterns = [
            'bot', 'crawler', 'spider', 'scraper', 'scanner',
            'sqlmap', 'nikto', 'nmap', 'masscan'
        ]
        
        for pattern in bot_patterns:
            if pattern in user_agent:
                # Log suspicious activity
                self.log_suspicious_activity(request, f"Suspicious User-Agent: {user_agent}")
                return HttpResponseForbidden("Access denied")
        
        # Block suspicious paths
        suspicious_paths = [
            'admin', 'wp-admin', 'phpmyadmin', 'config',
            '.env', '.git', 'backup', 'test'
        ]
        
        for pattern in suspicious_paths:
            if pattern in path and not path.startswith('/admin/'):
                self.log_suspicious_activity(request, f"Suspicious path access: {path}")
                return HttpResponseForbidden("Access denied")
        
        return None
    
    def log_suspicious_activity(self, request, reason):
        """Log suspicious activity for monitoring"""
        client_ip = self.get_client_ip(request)
        timestamp = time.time()
        
        # Store in cache for monitoring
        cache_key = f"suspicious_{client_ip}_{timestamp}"
        cache.set(cache_key, {
            'ip': client_ip,
            'reason': reason,
            'timestamp': timestamp,
            'user_agent': request.META.get('HTTP_USER_AGENT', ''),
            'path': request.path
        }, 86400)  # Keep for 24 hours
    
    def get_client_ip(self, request):
        """Get client IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

def generate_secure_token():
    """Generate a secure token for CSRF protection"""
    return hashlib.sha256(f"{time.time()}{hashlib.random_bytes(16)}".encode()).hexdigest()

def validate_request_origin(request):
    """Validate request origin for additional security"""
    origin = request.META.get('HTTP_ORIGIN')
    referer = request.META.get('HTTP_REFERER')
    
    # Check if request comes from same domain
    if origin and not origin.startswith(request.build_absolute_uri('/')[:-1]):
        return False
    
    if referer and not referer.startswith(request.build_absolute_uri('/')[:-1]):
        return False
    
    return True
