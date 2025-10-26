"""
Security utilities for BusinessThis
"""
import time
from typing import Dict, Optional
from functools import wraps
try:
    from flask import request, jsonify, g
except ImportError:
    # Fallback for when Flask is not available
    def jsonify(data):
        import json
        return json.dumps(data)
    
    class MockRequest:
        remote_addr = "127.0.0.1"
        environ = {}
        endpoint = "test"
    
    request = MockRequest()
import hashlib

# Rate limiting storage (in production, use Redis)
rate_limit_storage = {}

def rate_limit(max_requests: int = 100, window: int = 3600):
    """
    Rate limiting decorator
    Args:
        max_requests: Maximum requests per window
        window: Time window in seconds
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Get client IP
            client_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
            if client_ip:
                client_ip = client_ip.split(',')[0].strip()
            
            # Create rate limit key
            key = f"{client_ip}:{request.endpoint}"
            current_time = time.time()
            
            # Clean old entries
            rate_limit_storage[key] = [
                req_time for req_time in rate_limit_storage.get(key, [])
                if current_time - req_time < window
            ]
            
            # Check rate limit
            if len(rate_limit_storage.get(key, [])) >= max_requests:
                return jsonify({
                    'error': 'Rate limit exceeded',
                    'retry_after': window
                }), 429
            
            # Add current request
            if key not in rate_limit_storage:
                rate_limit_storage[key] = []
            rate_limit_storage[key].append(current_time)
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def add_security_headers(response):
    """Add security headers to response"""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'"
    return response

def validate_csrf_token(token: str, session_token: str) -> bool:
    """Validate CSRF token"""
    if not token or not session_token:
        return False
    return token == session_token

def generate_csrf_token() -> str:
    """Generate CSRF token"""
    import secrets
    return secrets.token_urlsafe(32)

def hash_password(password: str) -> str:
    """Hash password with salt"""
    import secrets
    salt = secrets.token_hex(16)
    return hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000).hex() + ':' + salt

def verify_password(password: str, hashed: str) -> bool:
    """Verify password against hash"""
    try:
        hash_part, salt = hashed.split(':')
        return hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000).hex() == hash_part
    except:
        return False

def sanitize_filename(filename: str) -> str:
    """Sanitize filename for security"""
    import re
    # Remove path components and dangerous characters
    filename = re.sub(r'[^\w\-_\.]', '', filename)
    # Limit length
    if len(filename) > 255:
        name, ext = filename.rsplit('.', 1) if '.' in filename else (filename, '')
        filename = name[:255-len(ext)-1] + ('.' + ext if ext else '')
    return filename

def validate_file_upload(file) -> Dict[str, any]:
    """Validate file upload"""
    allowed_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.pdf', '.txt', '.csv'}
    max_size = 16 * 1024 * 1024  # 16MB
    
    if not file:
        return {'valid': False, 'error': 'No file provided'}
    
    # Check file size
    if hasattr(file, 'content_length') and file.content_length > max_size:
        return {'valid': False, 'error': 'File too large'}
    
    # Check file extension
    if file.filename:
        import os
        ext = os.path.splitext(file.filename)[1].lower()
        if ext not in allowed_extensions:
            return {'valid': False, 'error': f'File type {ext} not allowed'}
    
    return {'valid': True}

def check_admin_permissions(user_id: str) -> bool:
    """Check if user has admin permissions"""
    # This would typically check against a database
    # For now, return False for security
    return False

def log_security_event(event_type: str, user_id: Optional[str], details: Dict[str, any]):
    """Log security events"""
    import logging
    logger = logging.getLogger('security')
    logger.warning(f"Security event: {event_type}, User: {user_id}, Details: {details}")

def detect_suspicious_activity(user_id: str, activity: str) -> bool:
    """Detect suspicious user activity"""
    # Simple heuristic - in production, use ML models
    suspicious_patterns = [
        'admin', 'drop', 'delete', 'union', 'select',
        'script', 'javascript', 'eval', 'exec'
    ]
    
    activity_lower = activity.lower()
    for pattern in suspicious_patterns:
        if pattern in activity_lower:
            log_security_event('suspicious_activity', user_id, {'pattern': pattern, 'activity': activity})
            return True
    
    return False
