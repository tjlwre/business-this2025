"""
BusinessThis Flask Backend
Main application file with API endpoints
"""
import os
import json
from datetime import datetime, timedelta
from flask import Flask, request, jsonify, session
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from functools import wraps

# Import our modules
from config.supabase_config import get_supabase_client, get_supabase_service_client
from config.validation import validate_environment
from models.user import User
from models.financial_profile import FinancialProfile
from models.savings_goal import SavingsGoal
from models.transaction import Transaction
from services.auth_service import AuthService
from services.financial_service import FinancialService
from services.subscription_service import SubscriptionService
from services.investment_service import InvestmentService
from services.ai_service import AIService
from services.admin_service import AdminService
from services.reports_service import ReportsService
from services.email_service import EmailService
from services.affiliate_service import AffiliateService
from services.course_service import CourseService
from services.multi_user_service import MultiUserService
from services.advisor_service import AdvisorService
from core.utils.validators import validate_email, validate_financial_data, validate_user_input
from core.utils.decorators import require_auth, require_subscription
from core.utils.security import rate_limit, add_security_headers, log_security_event
from core.utils.error_handler import handle_errors, ValidationError, AuthenticationError

# Validate environment before starting
try:
    validate_environment()
    print("✅ Environment validation passed")
except ValueError as e:
    print(f"❌ Environment validation failed: {e}")
    raise

# Initialize Flask app
app = Flask(__name__)
# Get secret key from environment - no default for security
secret_key = os.getenv('SECRET_KEY')
if not secret_key:
    raise ValueError("SECRET_KEY environment variable must be set for security")
app.config['SECRET_KEY'] = secret_key
# Dynamic CORS configuration
cors_origins = os.getenv('CORS_ORIGINS', 'http://localhost:8501').split(',')
CORS(app, origins=cors_origins)

# Add security headers to all responses
@app.after_request
def after_request(response):
    return add_security_headers(response)

# Initialize services
auth_service = AuthService()
financial_service = FinancialService()
subscription_service = SubscriptionService()
investment_service = InvestmentService()
ai_service = AIService()
admin_service = AdminService()
reports_service = ReportsService()
email_service = EmailService()
affiliate_service = AffiliateService()
course_service = CourseService()
multi_user_service = MultiUserService()
advisor_service = AdvisorService()

# JWT token configuration
JWT_SECRET = app.config['SECRET_KEY']
JWT_ALGORITHM = 'HS256'
JWT_EXPIRATION = 24 * 60 * 60  # 24 hours

def create_jwt_token(user_id: str) -> str:
    """Create JWT token for user"""
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(seconds=JWT_EXPIRATION),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def verify_jwt_token(token: str) -> dict:
    """Verify JWT token and return payload"""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("Token has expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")

"""Blueprint registrations for core domains"""
from backend.routes.auth import auth_bp
from backend.routes.profile import profile_bp
from backend.routes.goals import goals_bp
from backend.routes.calculator import calculator_bp
from backend.routes.subscription import subscription_bp
from backend.routes.investment import investment_bp
from backend.routes.ai import ai_bp
from backend.routes.reports import reports_bp
from backend.routes.admin import admin_bp
from backend.routes.email import email_bp
from backend.routes.affiliate import affiliate_bp
from backend.routes.courses import courses_bp
from backend.routes.accounts import accounts_bp
from backend.routes.advisor import advisor_bp

app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(profile_bp, url_prefix='/api/financial-profile')
app.register_blueprint(goals_bp, url_prefix='/api/savings-goals')
app.register_blueprint(calculator_bp, url_prefix='/api/calculator')
app.register_blueprint(subscription_bp, url_prefix='/api/subscription')
app.register_blueprint(investment_bp, url_prefix='/api/investment')
app.register_blueprint(ai_bp, url_prefix='/api/ai')
app.register_blueprint(reports_bp, url_prefix='/api/reports')
app.register_blueprint(admin_bp, url_prefix='/api/admin')
app.register_blueprint(email_bp, url_prefix='/api/email')
app.register_blueprint(affiliate_bp, url_prefix='/api/affiliate')
app.register_blueprint(courses_bp, url_prefix='/api/courses')
app.register_blueprint(accounts_bp, url_prefix='/api/accounts')
app.register_blueprint(advisor_bp, url_prefix='/api/advisor')

# Deprecated endpoints - moved to blueprints
@app.route('/api/investment/recommendations', methods=['GET'])
@require_auth
@require_subscription('premium')
def deprecated_investment_recommendations():
    return jsonify({'error': 'Moved to blueprint'}), 410

@app.route('/api/ai/daily-tip', methods=['GET'])
@require_auth
@require_subscription('premium')
def deprecated_ai_daily_tip():
    return jsonify({'error': 'Moved to blueprint'}), 410

@app.route('/api/reports/pdf', methods=['GET'])
@require_auth
@require_subscription('premium')
def deprecated_reports_pdf():
    return jsonify({'error': 'Moved to blueprint'}), 410

# All endpoints moved to blueprints - see routes/ directory

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0'
    }), 200

@app.route('/api/health/ollama', methods=['GET'])
def ollama_health_check():
    """Check Ollama service health"""
    try:
        is_healthy = ai_service.ollama.health_check()
        available_models = ai_service.ollama.get_available_models()
        
        return jsonify({
            'ollama_status': 'healthy' if is_healthy else 'unhealthy',
            'available_models': available_models,
            'current_model': ai_service.ollama.model,
            'timestamp': datetime.utcnow().isoformat()
        }), 200 if is_healthy else 503
        
    except Exception as e:
        return jsonify({
            'ollama_status': 'error',
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 503

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    # Run the app
    # Production-safe configuration
    debug_mode = os.getenv('DEBUG', 'False').lower() == 'true'
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    app.run(debug=debug_mode, host=host, port=port)
