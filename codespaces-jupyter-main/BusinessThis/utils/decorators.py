"""
Decorators for BusinessThis
"""
from functools import wraps
from flask import request, jsonify
import jwt
from datetime import datetime

def require_auth(f):
    """Decorator to require authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        
        # Check for token in Authorization header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]  # Bearer <token>
            except IndexError:
                return jsonify({'error': 'Invalid authorization header format'}), 401
        
        if not token:
            return jsonify({'error': 'Authorization token is missing'}), 401
        
        try:
            # Verify token
            from backend.app import JWT_SECRET, JWT_ALGORITHM
            payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            user_id = payload['user_id']
            
            # Add user_id to request object for use in route handlers
            request.user_id = user_id
            
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
        except Exception as e:
            return jsonify({'error': f'Token verification failed: {str(e)}'}), 401
        
        return f(*args, **kwargs)
    
    return decorated_function

def require_subscription(tier: str = 'premium'):
    """Decorator to require specific subscription tier"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # First check if user is authenticated
            if not hasattr(request, 'user_id'):
                return jsonify({'error': 'Authentication required'}), 401
            
            user_id = request.user_id
            
            # Get user's subscription status
            from services.auth_service import AuthService
            auth_service = AuthService()
            user = auth_service.get_user_by_id(user_id)
            
            if not user:
                return jsonify({'error': 'User not found'}), 404
            
            # Check subscription tier
            if tier == 'premium' and not user.is_premium():
                return jsonify({'error': 'Premium subscription required'}), 403
            elif tier == 'pro' and not user.is_pro():
                return jsonify({'error': 'Pro subscription required'}), 403
            
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator

def require_ai_access(f):
    """Decorator to check AI usage limits"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not hasattr(request, 'user_id'):
            return jsonify({'error': 'Authentication required'}), 401
        
        user_id = request.user_id
        
        # Get user's AI usage status
        from services.auth_service import AuthService
        auth_service = AuthService()
        user = auth_service.get_user_by_id(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        if not user.can_use_ai():
            return jsonify({'error': 'AI access not available for your subscription tier'}), 403
        
        # Increment AI usage count
        auth_service.increment_ai_usage(user_id)
        
        return f(*args, **kwargs)
    
    return decorated_function

def rate_limit(max_requests: int = 100, window_minutes: int = 60):
    """Simple rate limiting decorator"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # This is a simple implementation
            # In production, you'd use Redis or similar for distributed rate limiting
            # For now, we'll just allow the request
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator

def validate_json_schema(schema):
    """Decorator to validate JSON request body against schema"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not request.is_json:
                return jsonify({'error': 'Request must be JSON'}), 400
            
            data = request.get_json()
            
            # Simple schema validation
            for field, field_type in schema.items():
                if field not in data:
                    return jsonify({'error': f'Missing required field: {field}'}), 400
                
                if not isinstance(data[field], field_type):
                    return jsonify({'error': f'Field {field} must be of type {field_type.__name__}'}), 400
            
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator

def log_api_call(f):
    """Decorator to log API calls"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Log the API call
        print(f"API Call: {request.method} {request.path} - User: {getattr(request, 'user_id', 'Anonymous')}")
        
        return f(*args, **kwargs)
    
    return decorated_function
