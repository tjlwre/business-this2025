"""
BusinessThis Flask Backend - Vercel Compatible Version
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

# Initialize Flask app
app = Flask(__name__)

# Get secret key from environment with fallback
secret_key = os.getenv('SECRET_KEY', 'fallback-secret-key-for-development')
app.config['SECRET_KEY'] = secret_key

# Dynamic CORS configuration
cors_origins = os.getenv('CORS_ORIGINS', 'http://localhost:3000,http://localhost:8501,https://businessthis.com').split(',')
CORS(app, origins=cors_origins)

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'environment': os.getenv('ENVIRONMENT', 'development')
    })

# Basic API endpoints (without database dependencies for now)
@app.route('/api/auth/register', methods=['POST'])
def register():
    """Register new user"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        email = data.get('email')
        password = data.get('password')
        full_name = data.get('full_name')
        
        if not email or not password or not full_name:
            return jsonify({'error': 'Missing required fields'}), 400
        
        # For now, just return success (database integration will be added later)
        return jsonify({
            'message': 'User registered successfully',
            'user_id': 'temp-user-id',
            'email': email
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    """Login user"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'error': 'Missing email or password'}), 400
        
        # For now, just return success (database integration will be added later)
        return jsonify({
            'message': 'Login successful',
            'user_id': 'temp-user-id',
            'email': email,
            'token': 'temp-token'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/calculator/safe-spend', methods=['POST'])
def calculate_safe_spend():
    """Calculate safe spending amount"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        monthly_income = float(data.get('monthly_income', 0))
        fixed_expenses = float(data.get('fixed_expenses', 0))
        variable_expenses = float(data.get('variable_expenses', 0))
        emergency_fund = float(data.get('emergency_fund', 0))
        savings_goals = float(data.get('savings_goals', 0))
        
        # Calculate safe spending
        total_expenses = fixed_expenses + variable_expenses
        available_income = monthly_income - total_expenses
        safe_spending = available_income - (emergency_fund + savings_goals)
        
        # Calculate daily, weekly, monthly amounts
        daily_safe = max(0, safe_spending / 30)
        weekly_safe = max(0, safe_spending / 4.33)
        monthly_safe = max(0, safe_spending)
        
        return jsonify({
            'daily_safe_spend': round(daily_safe, 2),
            'weekly_safe_spend': round(weekly_safe, 2),
            'monthly_safe_spend': round(monthly_safe, 2),
            'total_available': round(available_income, 2),
            'recommendations': [
                'Build emergency fund to 3-6 months expenses',
                'Save 20% of income for long-term goals',
                'Track spending to identify savings opportunities'
            ]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
