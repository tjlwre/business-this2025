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
from models.user import User
from models.financial_profile import FinancialProfile
from models.savings_goal import SavingsGoal
from models.transaction import Transaction
from services.auth_service import AuthService
from services.financial_service import FinancialService
from services.subscription_service import SubscriptionService
from utils.validators import validate_email, validate_financial_data
from utils.decorators import require_auth, require_subscription

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
CORS(app, origins=['http://localhost:3000', 'http://localhost:8501'])

# Initialize services
auth_service = AuthService()
financial_service = FinancialService()
subscription_service = SubscriptionService()

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

# Authentication endpoints
@app.route('/api/auth/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.get_json()
        
        # Validate input
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Email and password are required'}), 400
        
        if not validate_email(data['email']):
            return jsonify({'error': 'Invalid email format'}), 400
        
        if len(data['password']) < 8:
            return jsonify({'error': 'Password must be at least 8 characters'}), 400
        
        # Register user with Supabase Auth
        result = auth_service.register_user(
            email=data['email'],
            password=data['password'],
            full_name=data.get('full_name', '')
        )
        
        if result['success']:
            return jsonify({
                'message': 'User registered successfully',
                'user_id': result['user_id']
            }), 201
        else:
            return jsonify({'error': result['error']}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    """Login user"""
    try:
        data = request.get_json()
        
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Email and password are required'}), 400
        
        # Authenticate with Supabase
        result = auth_service.login_user(data['email'], data['password'])
        
        if result['success']:
            # Create JWT token
            token = create_jwt_token(result['user_id'])
            
            return jsonify({
                'message': 'Login successful',
                'token': token,
                'user': result['user']
            }), 200
        else:
            return jsonify({'error': result['error']}), 401
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/logout', methods=['POST'])
@require_auth
def logout():
    """Logout user"""
    return jsonify({'message': 'Logout successful'}), 200

@app.route('/api/auth/me', methods=['GET'])
@require_auth
def get_current_user():
    """Get current user information"""
    try:
        user_id = request.user_id
        user = auth_service.get_user_by_id(user_id)
        
        if user:
            return jsonify({'user': user}), 200
        else:
            return jsonify({'error': 'User not found'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Financial profile endpoints
@app.route('/api/financial-profile', methods=['GET'])
@require_auth
def get_financial_profile():
    """Get user's financial profile"""
    try:
        user_id = request.user_id
        profile = financial_service.get_financial_profile(user_id)
        
        if profile:
            return jsonify({'profile': profile}), 200
        else:
            return jsonify({'error': 'Financial profile not found'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/financial-profile', methods=['POST', 'PUT'])
@require_auth
def update_financial_profile():
    """Create or update user's financial profile"""
    try:
        user_id = request.user_id
        data = request.get_json()
        
        # Validate financial data
        validation_result = validate_financial_data(data)
        if not validation_result['valid']:
            return jsonify({'error': validation_result['error']}), 400
        
        # Update financial profile
        result = financial_service.update_financial_profile(user_id, data)
        
        if result['success']:
            return jsonify({
                'message': 'Financial profile updated successfully',
                'profile': result['profile']
            }), 200
        else:
            return jsonify({'error': result['error']}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Savings goals endpoints
@app.route('/api/savings-goals', methods=['GET'])
@require_auth
def get_savings_goals():
    """Get user's savings goals"""
    try:
        user_id = request.user_id
        goals = financial_service.get_savings_goals(user_id)
        
        return jsonify({'goals': goals}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/savings-goals', methods=['POST'])
@require_auth
def create_savings_goal():
    """Create a new savings goal"""
    try:
        user_id = request.user_id
        data = request.get_json()
        
        # Validate goal data
        if not data.get('name') or not data.get('target_amount'):
            return jsonify({'error': 'Goal name and target amount are required'}), 400
        
        result = financial_service.create_savings_goal(user_id, data)
        
        if result['success']:
            return jsonify({
                'message': 'Savings goal created successfully',
                'goal': result['goal']
            }), 201
        else:
            return jsonify({'error': result['error']}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/savings-goals/<goal_id>', methods=['PUT'])
@require_auth
def update_savings_goal(goal_id):
    """Update a savings goal"""
    try:
        user_id = request.user_id
        data = request.get_json()
        
        result = financial_service.update_savings_goal(user_id, goal_id, data)
        
        if result['success']:
            return jsonify({
                'message': 'Savings goal updated successfully',
                'goal': result['goal']
            }), 200
        else:
            return jsonify({'error': result['error']}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/savings-goals/<goal_id>', methods=['DELETE'])
@require_auth
def delete_savings_goal(goal_id):
    """Delete a savings goal"""
    try:
        user_id = request.user_id
        
        result = financial_service.delete_savings_goal(user_id, goal_id)
        
        if result['success']:
            return jsonify({'message': 'Savings goal deleted successfully'}), 200
        else:
            return jsonify({'error': result['error']}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Calculator endpoints
@app.route('/api/calculator/safe-spend', methods=['POST'])
@require_auth
def calculate_safe_spend():
    """Calculate safe daily/weekly/monthly spending"""
    try:
        user_id = request.user_id
        data = request.get_json()
        
        # Get user's financial profile
        profile = financial_service.get_financial_profile(user_id)
        if not profile:
            return jsonify({'error': 'Financial profile not found'}), 404
        
        # Calculate safe spending
        result = financial_service.calculate_safe_spending(
            user_id,
            data.get('savings_goal'),
            data.get('months_for_goal')
        )
        
        return jsonify({'safe_spending': result}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/calculator/financial-health', methods=['GET'])
@require_auth
def calculate_financial_health():
    """Calculate user's financial health score"""
    try:
        user_id = request.user_id
        
        result = financial_service.calculate_financial_health_score(user_id)
        
        return jsonify({'financial_health': result}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Subscription endpoints
@app.route('/api/subscription/status', methods=['GET'])
@require_auth
def get_subscription_status():
    """Get user's subscription status"""
    try:
        user_id = request.user_id
        
        result = subscription_service.get_subscription_status(user_id)
        
        return jsonify({'subscription': result}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/subscription/upgrade', methods=['POST'])
@require_auth
def upgrade_subscription():
    """Upgrade user's subscription"""
    try:
        user_id = request.user_id
        data = request.get_json()
        
        plan = data.get('plan')
        if not plan or plan not in ['premium', 'pro']:
            return jsonify({'error': 'Invalid plan. Must be premium or pro'}), 400
        
        result = subscription_service.create_subscription(user_id, plan)
        
        if result['success']:
            return jsonify({
                'message': 'Subscription created successfully',
                'checkout_url': result['checkout_url']
            }), 200
        else:
            return jsonify({'error': result['error']}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0'
    }), 200

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
    app.run(debug=True, host='0.0.0.0', port=5000)
