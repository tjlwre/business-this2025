"""
Comprehensive error handling utilities for BusinessThis
"""
import logging
import traceback
from typing import Dict, Any, Optional
from functools import wraps

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Fallback for when Flask is not available
try:
    from flask import jsonify
except ImportError:
    def jsonify(data):
        import json
        return json.dumps(data)

class BusinessThisError(Exception):
    """Base exception for BusinessThis"""
    def __init__(self, message: str, error_code: str = None, status_code: int = 400):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        super().__init__(self.message)

class ValidationError(BusinessThisError):
    """Validation error"""
    def __init__(self, message: str, field: str = None):
        super().__init__(message, "VALIDATION_ERROR", 400)
        self.field = field

class AuthenticationError(BusinessThisError):
    """Authentication error"""
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, "AUTH_ERROR", 401)

class AuthorizationError(BusinessThisError):
    """Authorization error"""
    def __init__(self, message: str = "Access denied"):
        super().__init__(message, "AUTHZ_ERROR", 403)

class NotFoundError(BusinessThisError):
    """Resource not found error"""
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, "NOT_FOUND", 404)

class DatabaseError(BusinessThisError):
    """Database error"""
    def __init__(self, message: str = "Database operation failed"):
        super().__init__(message, "DB_ERROR", 500)

class ExternalServiceError(BusinessThisError):
    """External service error"""
    def __init__(self, message: str = "External service error"):
        super().__init__(message, "EXTERNAL_SERVICE_ERROR", 502)

def handle_errors(f):
    """Decorator for comprehensive error handling"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ValidationError as e:
            logger.warning(f"Validation error: {e.message}")
            return jsonify({
                'error': e.message,
                'error_code': e.error_code,
                'field': getattr(e, 'field', None)
            }), e.status_code
        except AuthenticationError as e:
            logger.warning(f"Authentication error: {e.message}")
            return jsonify({
                'error': e.message,
                'error_code': e.error_code
            }), e.status_code
        except AuthorizationError as e:
            logger.warning(f"Authorization error: {e.message}")
            return jsonify({
                'error': e.message,
                'error_code': e.error_code
            }), e.status_code
        except NotFoundError as e:
            logger.info(f"Not found: {e.message}")
            return jsonify({
                'error': e.message,
                'error_code': e.error_code
            }), e.status_code
        except DatabaseError as e:
            logger.error(f"Database error: {e.message}")
            return jsonify({
                'error': 'Database operation failed',
                'error_code': e.error_code
            }), e.status_code
        except ExternalServiceError as e:
            logger.error(f"External service error: {e.message}")
            return jsonify({
                'error': 'External service temporarily unavailable',
                'error_code': e.error_code
            }), e.status_code
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            return jsonify({
                'error': 'An unexpected error occurred',
                'error_code': 'INTERNAL_ERROR'
            }), 500
    return decorated_function

def safe_execute(func, *args, **kwargs):
    """Safely execute a function with error handling"""
    try:
        return func(*args, **kwargs), None
    except Exception as e:
        logger.error(f"Error in safe_execute: {str(e)}")
        return None, str(e)

def validate_and_execute(validation_func, execution_func, data: Dict[str, Any]):
    """Validate data and execute function with error handling"""
    try:
        # Validate input
        validation_result = validation_func(data)
        if not validation_result.get('valid', False):
            raise ValidationError(f"Validation failed: {', '.join(validation_result.get('errors', []))}")
        
        # Execute function
        return execution_func(data), None
    except Exception as e:
        logger.error(f"Error in validate_and_execute: {str(e)}")
        return None, str(e)

def log_error(error: Exception, context: str = ""):
    """Log error with context"""
    logger.error(f"Error in {context}: {str(error)}")
    logger.error(f"Traceback: {traceback.format_exc()}")

def create_error_response(message: str, error_code: str = "ERROR", status_code: int = 400) -> tuple:
    """Create standardized error response"""
    return jsonify({
        'error': message,
        'error_code': error_code
    }), status_code
