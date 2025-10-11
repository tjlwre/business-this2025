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
from core.models.user import User
from core.models.financial_profile import FinancialProfile
from core.models.savings_goal import SavingsGoal
from core.models.transaction import Transaction
from core.services.auth_service import AuthService
from core.services.financial_service import FinancialService
from core.services.subscription_service import SubscriptionService
from core.services.investment_service import InvestmentService
from core.services.ai_service import AIService
from core.services.admin_service import AdminService
from core.services.reports_service import ReportsService
from core.services.email_service import EmailService
from core.services.affiliate_service import AffiliateService
from core.services.course_service import CourseService
from core.services.multi_user_service import MultiUserService
from core.services.advisor_service import AdvisorService
from core.utils.validators import validate_email, validate_financial_data
from core.utils.decorators import require_auth, require_subscription

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
CORS(app, origins=['http://localhost:3000', 'http://localhost:8501'])

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

# Investment endpoints
@app.route('/api/investment/asset-allocation', methods=['POST'])
@require_auth
@require_subscription('premium')
def calculate_asset_allocation():
    """Calculate recommended asset allocation"""
    try:
        user_id = request.user_id
        data = request.get_json()
        
        age = data.get('age', 30)
        risk_tolerance = data.get('risk_tolerance', 'moderate')
        investment_amount = data.get('investment_amount', 10000)
        
        result = investment_service.calculate_asset_allocation(age, risk_tolerance, investment_amount)
        
        return jsonify({'asset_allocation': result}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/investment/retirement-planning', methods=['POST'])
@require_auth
@require_subscription('premium')
def calculate_retirement_planning():
    """Calculate retirement planning needs"""
    try:
        user_id = request.user_id
        data = request.get_json()
        
        current_age = data.get('current_age', 30)
        retirement_age = data.get('retirement_age', 65)
        current_savings = data.get('current_savings', 0)
        monthly_income = data.get('monthly_income', 5000)
        desired_retirement_income = data.get('desired_retirement_income', 0)
        
        result = investment_service.calculate_retirement_needs(
            current_age, retirement_age, current_savings, 
            monthly_income, desired_retirement_income
        )
        
        return jsonify({'retirement_planning': result}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/investment/compound-interest', methods=['POST'])
@require_auth
def calculate_compound_interest():
    """Calculate compound interest growth"""
    try:
        user_id = request.user_id
        data = request.get_json()
        
        principal = data.get('principal', 0)
        monthly_contribution = data.get('monthly_contribution', 0)
        annual_rate = data.get('annual_rate', 0.07)
        years = data.get('years', 10)
        
        result = investment_service.calculate_compound_interest(
            principal, monthly_contribution, annual_rate, years
        )
        
        return jsonify({'compound_interest': result}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/investment/tax-optimization', methods=['POST'])
@require_auth
@require_subscription('premium')
def calculate_tax_optimization():
    """Calculate tax optimization strategies"""
    try:
        user_id = request.user_id
        data = request.get_json()
        
        income = data.get('income', 50000)
        filing_status = data.get('filing_status', 'single')
        deductions = data.get('deductions', 0)
        credits = data.get('credits', 0)
        
        result = investment_service.calculate_tax_optimization(
            income, filing_status, deductions, credits
        )
        
        return jsonify({'tax_optimization': result}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/investment/what-if-scenarios', methods=['POST'])
@require_auth
@require_subscription('premium')
def calculate_what_if_scenarios():
    """Calculate what-if scenarios"""
    try:
        user_id = request.user_id
        data = request.get_json()
        
        base_income = data.get('base_income', 5000)
        base_expenses = data.get('base_expenses', 3000)
        scenarios = data.get('scenarios', [])
        
        result = investment_service.calculate_what_if_scenarios(
            base_income, base_expenses, scenarios
        )
        
        return jsonify({'what_if_scenarios': result}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/investment/recommendations', methods=['GET'])
@require_auth
@require_subscription('premium')
def get_investment_recommendations():
    """Get personalized investment recommendations"""
    try:
        user_id = request.user_id
        
        # Get user's financial profile
        profile_response, status = financial_service.get_financial_profile(user_id)
        if status != 200:
            return jsonify({'error': 'Financial profile not found'}), 404
        
        profile = profile_response['profile']
        
        age = profile.get('age', 30)
        income = profile.get('monthly_income', 0) * 12  # Convert to annual
        risk_tolerance = profile.get('risk_tolerance', 'moderate')
        current_investments = profile.get('emergency_fund_current', 0)
        
        result = investment_service.get_investment_recommendations(
            age, income, risk_tolerance, current_investments
        )
        
        return jsonify({'investment_recommendations': result}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# AI endpoints
@app.route('/api/ai/coaching', methods=['POST'])
@require_auth
@require_subscription('premium')
def get_ai_coaching():
    """Get AI financial coaching"""
    try:
        user_id = request.user_id
        data = request.get_json()
        
        question = data.get('question', '')
        if not question:
            return jsonify({'error': 'Question is required'}), 400
        
        # Get user's financial profile
        profile_response, status = financial_service.get_financial_profile(user_id)
        if status != 200:
            return jsonify({'error': 'Financial profile not found'}), 404
        
        profile = profile_response['profile']
        
        result = ai_service.get_financial_coaching(profile, question)
        
        return jsonify({'coaching': result}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ai/spending-recommendations', methods=['GET'])
@require_auth
@require_subscription('premium')
def get_spending_recommendations():
    """Get AI-powered spending recommendations"""
    try:
        user_id = request.user_id
        
        # Get user's financial profile
        profile_response, status = financial_service.get_financial_profile(user_id)
        if status != 200:
            return jsonify({'error': 'Financial profile not found'}), 404
        
        profile = profile_response['profile']
        
        # Get recent transactions (mock data for now)
        recent_transactions = []  # TODO: Implement transaction retrieval
        
        result = ai_service.get_spending_recommendations(profile, recent_transactions)
        
        return jsonify({'recommendations': result}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ai/daily-tip', methods=['GET'])
@require_auth
@require_subscription('premium')
def get_daily_tip():
    """Get daily financial tip"""
    try:
        user_id = request.user_id
        
        # Get user's financial profile
        profile_response, status = financial_service.get_financial_profile(user_id)
        if status != 200:
            return jsonify({'error': 'Financial profile not found'}), 404
        
        profile = profile_response['profile']
        
        result = ai_service.get_daily_financial_tip(profile)
        
        return jsonify({'daily_tip': result}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ai/goal-analysis', methods=['GET'])
@require_auth
@require_subscription('premium')
def get_goal_analysis():
    """Get AI analysis of financial goals"""
    try:
        user_id = request.user_id
        
        # Get user's financial profile
        profile_response, status = financial_service.get_financial_profile(user_id)
        if status != 200:
            return jsonify({'error': 'Financial profile not found'}), 404
        
        profile = profile_response['profile']
        
        # Get savings goals
        goals_response, goals_status = financial_service.get_savings_goals(user_id)
        goals = goals_response if goals_status == 200 else []
        
        result = ai_service.analyze_financial_goals(profile, goals)
        
        return jsonify({'goal_analysis': result}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ai/investment-advice', methods=['POST'])
@require_auth
@require_subscription('pro')
def get_investment_advice():
    """Get AI investment advice"""
    try:
        user_id = request.user_id
        data = request.get_json()
        
        # Get user's financial profile
        profile_response, status = financial_service.get_financial_profile(user_id)
        if status != 200:
            return jsonify({'error': 'Financial profile not found'}), 404
        
        profile = profile_response['profile']
        
        # Get current portfolio (mock data for now)
        current_portfolio = data.get('portfolio', {
            'total_value': 0,
            'stock_percentage': 0,
            'bond_percentage': 0,
            'cash_percentage': 100
        })
        
        result = ai_service.get_investment_advice(profile, current_portfolio)
        
        return jsonify({'investment_advice': result}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Admin endpoints
@app.route('/api/admin/dashboard', methods=['GET'])
@require_auth
def get_admin_dashboard():
    """Get admin dashboard metrics"""
    try:
        # TODO: Add admin role check
        user_id = request.user_id
        
        result = admin_service.get_dashboard_metrics()
        
        return jsonify({'dashboard': result}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/users', methods=['GET'])
@require_auth
def get_admin_users():
    """Get paginated user list"""
    try:
        # TODO: Add admin role check
        user_id = request.user_id
        
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 50))
        search = request.args.get('search', '')
        
        result = admin_service.get_user_list(page, limit, search)
        
        return jsonify({'users': result}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/users/<user_id>', methods=['GET'])
@require_auth
def get_admin_user_details(user_id):
    """Get detailed user information"""
    try:
        # TODO: Add admin role check
        admin_user_id = request.user_id
        
        result = admin_service.get_user_details(user_id)
        
        return jsonify({'user_details': result}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/users/<user_id>/subscription', methods=['PUT'])
@require_auth
def update_admin_user_subscription(user_id):
    """Update user subscription"""
    try:
        # TODO: Add admin role check
        admin_user_id = request.user_id
        data = request.get_json()
        
        tier = data.get('tier')
        status = data.get('status')
        
        if not tier or not status:
            return jsonify({'error': 'Tier and status are required'}), 400
        
        result = admin_service.update_user_subscription(user_id, tier, status)
        
        return jsonify({'result': result}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/support-tickets', methods=['GET'])
@require_auth
def get_admin_support_tickets():
    """Get support tickets"""
    try:
        # TODO: Add admin role check
        user_id = request.user_id
        
        status = request.args.get('status', 'all')
        
        result = admin_service.get_support_tickets(status)
        
        return jsonify({'tickets': result}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/support-tickets/<ticket_id>', methods=['PUT'])
@require_auth
def update_admin_support_ticket(ticket_id):
    """Update support ticket"""
    try:
        # TODO: Add admin role check
        user_id = request.user_id
        data = request.get_json()
        
        status = data.get('status')
        response = data.get('response', '')
        
        if not status:
            return jsonify({'error': 'Status is required'}), 400
        
        result = admin_service.update_support_ticket(ticket_id, status, response)
        
        return jsonify({'result': result}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Reports endpoints
@app.route('/api/reports/pdf', methods=['GET'])
@require_auth
@require_subscription('premium')
def generate_pdf_report():
    """Generate PDF financial report"""
    try:
        user_id = request.user_id
        
        # Get user's financial profile
        profile_response, status = financial_service.get_financial_profile(user_id)
        if status != 200:
            return jsonify({'error': 'Financial profile not found'}), 404
        
        profile = profile_response['profile']
        
        # Get savings goals
        goals_response, goals_status = financial_service.get_savings_goals(user_id)
        goals = goals_response if goals_status == 200 else []
        
        # Get financial health score
        health_response, health_status = financial_service.calculate_financial_health_score(user_id)
        health = health_response.get('financial_health', {}) if health_status == 200 else {}
        
        # Generate PDF
        pdf_data = reports_service.generate_financial_report_pdf(profile, goals, health)
        
        # Return PDF as base64
        import base64
        pdf_base64 = base64.b64encode(pdf_data).decode()
        
        return jsonify({
            'pdf_data': pdf_base64,
            'filename': f'financial_report_{datetime.now().strftime("%Y%m%d")}.pdf'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/reports/excel', methods=['GET'])
@require_auth
@require_subscription('premium')
def generate_excel_export():
    """Generate Excel export of financial data"""
    try:
        user_id = request.user_id
        
        # Get user's financial profile
        profile_response, status = financial_service.get_financial_profile(user_id)
        if status != 200:
            return jsonify({'error': 'Financial profile not found'}), 404
        
        profile = profile_response['profile']
        
        # Get savings goals
        goals_response, goals_status = financial_service.get_savings_goals(user_id)
        goals = goals_response if goals_status == 200 else []
        
        # Get transactions (mock data for now)
        transactions = []  # TODO: Implement transaction retrieval
        
        # Generate Excel
        excel_data = reports_service.generate_excel_export(profile, goals, transactions)
        
        # Return Excel as base64
        import base64
        excel_base64 = base64.b64encode(excel_data).decode()
        
        return jsonify({
            'excel_data': excel_base64,
            'filename': f'financial_data_{datetime.now().strftime("%Y%m%d")}.xlsx'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/reports/email-summary', methods=['GET'])
@require_auth
def generate_email_summary():
    """Generate email summary"""
    try:
        user_id = request.user_id
        
        # Get user's financial profile
        profile_response, status = financial_service.get_financial_profile(user_id)
        if status != 200:
            return jsonify({'error': 'Financial profile not found'}), 404
        
        profile = profile_response['profile']
        
        # Get savings goals
        goals_response, goals_status = financial_service.get_savings_goals(user_id)
        goals = goals_response if goals_status == 200 else []
        
        # Get recent transactions (mock data for now)
        transactions = []  # TODO: Implement transaction retrieval
        
        # Generate email summary
        summary = reports_service.generate_email_summary(profile, goals, transactions)
        
        return jsonify({'email_summary': summary}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/reports/chart', methods=['POST'])
@require_auth
@require_subscription('premium')
def generate_chart():
    """Generate financial chart"""
    try:
        user_id = request.user_id
        data = request.get_json()
        
        chart_type = data.get('chart_type')
        chart_data = data.get('data', {})
        
        if not chart_type:
            return jsonify({'error': 'Chart type is required'}), 400
        
        # Generate chart
        chart_base64 = reports_service.create_financial_chart(chart_type, chart_data)
        
        return jsonify({
            'chart_data': chart_base64,
            'chart_type': chart_type
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Email endpoints
@app.route('/api/email/welcome', methods=['POST'])
def send_welcome_email():
    """Send welcome email to new user"""
    try:
        data = request.get_json()
        
        user_email = data.get('email')
        user_name = data.get('name', 'User')
        
        if not user_email:
            return jsonify({'error': 'Email is required'}), 400
        
        result = email_service.send_welcome_email(user_email, user_name)
        
        return jsonify({'result': result}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/email/onboarding', methods=['POST'])
@require_auth
def send_onboarding_sequence():
    """Send onboarding email sequence"""
    try:
        user_id = request.user_id
        
        # Get user data
        user_result = auth_service.get_user_by_id(user_id)
        if not user_result:
            return jsonify({'error': 'User not found'}), 404
        
        # Get financial profile
        profile_response, status = financial_service.get_financial_profile(user_id)
        profile = profile_response.get('profile', {}) if status == 200 else {}
        
        result = email_service.send_onboarding_sequence(
            user_result.email, 
            user_result.full_name or 'User', 
            profile
        )
        
        return jsonify({'result': result}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/email/newsletter', methods=['POST'])
@require_auth
def send_weekly_newsletter():
    """Send weekly newsletter"""
    try:
        user_id = request.user_id
        
        # Get user data
        user_result = auth_service.get_user_by_id(user_id)
        if not user_result:
            return jsonify({'error': 'User not found'}), 404
        
        # Get financial summary
        profile_response, status = financial_service.get_financial_profile(user_id)
        if status != 200:
            return jsonify({'error': 'Financial profile not found'}), 404
        
        profile = profile_response['profile']
        
        # Generate financial summary
        financial_summary = {
            'monthly_income': profile.get('monthly_income', 0),
            'monthly_expenses': profile.get('fixed_expenses', 0) + profile.get('variable_expenses', 0),
            'monthly_savings': profile.get('monthly_income', 0) - profile.get('fixed_expenses', 0) - profile.get('variable_expenses', 0),
            'savings_rate': 0,
            'insights': ['Keep up the great work with your financial goals!']
        }
        
        # Calculate savings rate
        if financial_summary['monthly_income'] > 0:
            financial_summary['savings_rate'] = (financial_summary['monthly_savings'] / financial_summary['monthly_income']) * 100
        
        result = email_service.send_weekly_newsletter(
            user_result.email, 
            user_result.full_name or 'User', 
            financial_summary
        )
        
        return jsonify({'result': result}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/email/goal-achievement', methods=['POST'])
@require_auth
def send_goal_achievement_email():
    """Send goal achievement email"""
    try:
        user_id = request.user_id
        data = request.get_json()
        
        goal_name = data.get('goal_name')
        goal_amount = data.get('goal_amount', 0)
        
        if not goal_name:
            return jsonify({'error': 'Goal name is required'}), 400
        
        # Get user data
        user_result = auth_service.get_user_by_id(user_id)
        if not user_result:
            return jsonify({'error': 'User not found'}), 404
        
        result = email_service.send_goal_achievement_email(
            user_result.email, 
            user_result.full_name or 'User', 
            goal_name, 
            goal_amount
        )
        
        return jsonify({'result': result}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/email/upgrade', methods=['POST'])
@require_auth
def send_upgrade_email():
    """Send subscription upgrade email"""
    try:
        user_id = request.user_id
        data = request.get_json()
        
        new_tier = data.get('tier')
        
        if not new_tier:
            return jsonify({'error': 'Tier is required'}), 400
        
        # Get user data
        user_result = auth_service.get_user_by_id(user_id)
        if not user_result:
            return jsonify({'error': 'User not found'}), 404
        
        result = email_service.send_subscription_upgrade_email(
            user_result.email, 
            user_result.full_name or 'User', 
            new_tier
        )
        
        return jsonify({'result': result}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/email/daily-tip', methods=['POST'])
@require_auth
@require_subscription('premium')
def send_daily_tip_email():
    """Send daily financial tip email"""
    try:
        user_id = request.user_id
        data = request.get_json()
        
        tip = data.get('tip')
        tip_category = data.get('category', 'General')
        
        if not tip:
            return jsonify({'error': 'Tip is required'}), 400
        
        # Get user data
        user_result = auth_service.get_user_by_id(user_id)
        if not user_result:
            return jsonify({'error': 'User not found'}), 404
        
        result = email_service.send_daily_tip_email(
            user_result.email, 
            user_result.full_name or 'User', 
            tip, 
            tip_category
        )
        
        return jsonify({'result': result}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/email/engagement', methods=['POST'])
@require_auth
def send_engagement_email():
    """Send re-engagement email"""
    try:
        user_id = request.user_id
        data = request.get_json()
        
        days_since_last_login = data.get('days_since_last_login', 7)
        
        # Get user data
        user_result = auth_service.get_user_by_id(user_id)
        if not user_result:
            return jsonify({'error': 'User not found'}), 404
        
        result = email_service.send_engagement_email(
            user_result.email, 
            user_result.full_name or 'User', 
            days_since_last_login
        )
        
        return jsonify({'result': result}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Affiliate endpoints
@app.route('/api/affiliate/products', methods=['GET'])
@require_auth
def get_affiliate_products():
    """Get affiliate products based on user profile"""
    try:
        user_id = request.user_id
        category = request.args.get('category', 'all')
        
        # Get user's financial profile for personalization
        profile_response, status = financial_service.get_financial_profile(user_id)
        profile = profile_response.get('profile', {}) if status == 200 else {}
        
        result = affiliate_service.get_affiliate_products(category, profile)
        
        return jsonify({'products': result}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/affiliate/track-referral', methods=['POST'])
@require_auth
def track_referral():
    """Track referral click"""
    try:
        user_id = request.user_id
        data = request.get_json()
        
        product_id = data.get('product_id')
        referral_data = data.get('referral_data', {})
        
        if not product_id:
            return jsonify({'error': 'Product ID is required'}), 400
        
        result = affiliate_service.track_referral(user_id, product_id, referral_data)
        
        return jsonify({'result': result}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/affiliate/stats', methods=['GET'])
@require_auth
def get_affiliate_stats():
    """Get user's affiliate statistics"""
    try:
        user_id = request.user_id
        
        result = affiliate_service.get_user_affiliate_stats(user_id)
        
        return jsonify({'stats': result}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/affiliate/commission-breakdown', methods=['GET'])
@require_auth
def get_commission_breakdown():
    """Get detailed commission breakdown"""
    try:
        user_id = request.user_id
        
        result = affiliate_service.get_commission_breakdown(user_id)
        
        return jsonify({'breakdown': result}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/affiliate/generate-link', methods=['POST'])
@require_auth
def generate_affiliate_link():
    """Generate personalized affiliate link"""
    try:
        user_id = request.user_id
        data = request.get_json()
        
        product_id = data.get('product_id')
        
        if not product_id:
            return jsonify({'error': 'Product ID is required'}), 400
        
        link = affiliate_service.generate_affiliate_link(user_id, product_id)
        
        if not link:
            return jsonify({'error': 'Failed to generate affiliate link'}), 500
        
        return jsonify({'affiliate_link': link}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Course endpoints
@app.route('/api/courses/catalog', methods=['GET'])
def get_course_catalog():
    """Get course catalog with filtering options"""
    try:
        category = request.args.get('category', 'all')
        difficulty = request.args.get('difficulty', 'all')
        
        result = course_service.get_course_catalog(category, difficulty)
        
        return jsonify({'catalog': result}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/courses/<course_id>', methods=['GET'])
def get_course_details(course_id):
    """Get detailed information about a specific course"""
    try:
        result = course_service.get_course_details(course_id)
        
        if 'error' in result:
            return jsonify(result), 404
        
        return jsonify({'course': result}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/courses/<course_id>/enroll', methods=['POST'])
@require_auth
def enroll_in_course(course_id):
    """Enroll user in a course"""
    try:
        user_id = request.user_id
        data = request.get_json()
        
        payment_data = data.get('payment_data', {})
        
        result = course_service.enroll_user_in_course(user_id, course_id, payment_data)
        
        if 'error' in result:
            return jsonify(result), 400
        
        return jsonify({'enrollment': result}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/courses/user-courses', methods=['GET'])
@require_auth
def get_user_courses():
    """Get user's enrolled courses and progress"""
    try:
        user_id = request.user_id
        
        result = course_service.get_user_courses(user_id)
        
        return jsonify({'courses': result}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/courses/<course_id>/progress', methods=['POST'])
@require_auth
def update_course_progress(course_id):
    """Update user's progress in a course"""
    try:
        user_id = request.user_id
        data = request.get_json()
        
        module_id = data.get('module_id')
        
        if not module_id:
            return jsonify({'error': 'Module ID is required'}), 400
        
        result = course_service.update_course_progress(user_id, course_id, module_id)
        
        return jsonify({'progress': result}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/courses/<course_id>/certificate', methods=['GET'])
@require_auth
def get_course_certificate(course_id):
    """Get course certificate for completed course"""
    try:
        user_id = request.user_id
        
        result = course_service.get_course_certificate(user_id, course_id)
        
        return jsonify({'certificate': result}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/courses/recommendations', methods=['GET'])
@require_auth
def get_learning_recommendations():
    """Get personalized course recommendations"""
    try:
        user_id = request.user_id
        
        # Get user's financial profile for personalization
        profile_response, status = financial_service.get_financial_profile(user_id)
        profile = profile_response.get('profile', {}) if status == 200 else {}
        
        result = course_service.get_learning_recommendations(user_id, profile)
        
        return jsonify({'recommendations': result}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Multi-user account endpoints
@app.route('/api/accounts/family', methods=['POST'])
@require_auth
def create_family_account():
    """Create a new family account"""
    try:
        user_id = request.user_id
        data = request.get_json()
        
        family_name = data.get('family_name')
        billing_info = data.get('billing_info', {})
        
        if not family_name:
            return jsonify({'error': 'Family name is required'}), 400
        
        result = multi_user_service.create_family_account(user_id, family_name, billing_info)
        
        return jsonify({'result': result}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/accounts/enterprise', methods=['POST'])
@require_auth
def create_enterprise_account():
    """Create a new enterprise account"""
    try:
        user_id = request.user_id
        data = request.get_json()
        
        company_name = data.get('company_name')
        enterprise_info = data.get('enterprise_info', {})
        
        if not company_name:
            return jsonify({'error': 'Company name is required'}), 400
        
        result = multi_user_service.create_enterprise_account(user_id, company_name, enterprise_info)
        
        return jsonify({'result': result}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/accounts/<account_id>/invite', methods=['POST'])
@require_auth
def invite_user_to_account(account_id):
    """Invite a user to join an account"""
    try:
        user_id = request.user_id
        data = request.get_json()
        
        email = data.get('email')
        role = data.get('role', 'member')
        
        if not email:
            return jsonify({'error': 'Email is required'}), 400
        
        result = multi_user_service.invite_user_to_account(account_id, user_id, email, role)
        
        return jsonify({'result': result}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/accounts/invitations/<invitation_token>/accept', methods=['POST'])
@require_auth
def accept_invitation(invitation_token):
    """Accept an invitation to join an account"""
    try:
        user_id = request.user_id
        
        result = multi_user_service.accept_invitation(invitation_token, user_id)
        
        return jsonify({'result': result}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/accounts/<account_id>/members', methods=['GET'])
@require_auth
def get_account_members(account_id):
    """Get all members of an account"""
    try:
        user_id = request.user_id
        
        result = multi_user_service.get_account_members(account_id, user_id)
        
        return jsonify({'members': result}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/accounts/<account_id>/members/<member_id>/role', methods=['PUT'])
@require_auth
def update_member_role(account_id, member_id):
    """Update a member's role in the account"""
    try:
        user_id = request.user_id
        data = request.get_json()
        
        new_role = data.get('role')
        
        if not new_role:
            return jsonify({'error': 'Role is required'}), 400
        
        result = multi_user_service.update_member_role(account_id, user_id, member_id, new_role)
        
        return jsonify({'result': result}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/accounts/<account_id>/members/<member_id>', methods=['DELETE'])
@require_auth
def remove_member_from_account(account_id, member_id):
    """Remove a member from the account"""
    try:
        user_id = request.user_id
        
        result = multi_user_service.remove_member_from_account(account_id, user_id, member_id)
        
        return jsonify({'result': result}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/accounts/<account_id>/shared-goals', methods=['GET'])
@require_auth
def get_shared_goals(account_id):
    """Get shared goals for the account"""
    try:
        user_id = request.user_id
        
        result = multi_user_service.get_shared_goals(account_id, user_id)
        
        return jsonify({'goals': result}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/accounts/<account_id>/shared-goals', methods=['POST'])
@require_auth
def create_shared_goal(account_id):
    """Create a shared goal for the account"""
    try:
        user_id = request.user_id
        data = request.get_json()
        
        goal_data = data.get('goal_data', {})
        
        result = multi_user_service.create_shared_goal(account_id, user_id, goal_data)
        
        return jsonify({'result': result}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/accounts/<account_id>/dashboard', methods=['GET'])
@require_auth
def get_family_dashboard(account_id):
    """Get family dashboard data"""
    try:
        user_id = request.user_id
        
        result = multi_user_service.get_family_dashboard(account_id, user_id)
        
        return jsonify({'dashboard': result}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/accounts/<account_id>/enterprise-settings', methods=['GET'])
@require_auth
def get_enterprise_settings(account_id):
    """Get enterprise account settings"""
    try:
        user_id = request.user_id
        
        result = multi_user_service.get_enterprise_settings(account_id, user_id)
        
        return jsonify({'settings': result}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/accounts/<account_id>/enterprise-settings', methods=['PUT'])
@require_auth
def update_enterprise_settings(account_id):
    """Update enterprise account settings"""
    try:
        user_id = request.user_id
        data = request.get_json()
        
        settings = data.get('settings', {})
        
        result = multi_user_service.update_enterprise_settings(account_id, user_id, settings)
        
        return jsonify({'result': result}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/accounts/<account_id>/usage-stats', methods=['GET'])
@require_auth
def get_account_usage_stats(account_id):
    """Get account usage statistics"""
    try:
        user_id = request.user_id
        
        result = multi_user_service.get_account_usage_stats(account_id, user_id)
        
        return jsonify({'stats': result}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/accounts/<account_id>/upgrade', methods=['POST'])
@require_auth
def upgrade_account(account_id):
    """Upgrade account to a higher plan"""
    try:
        user_id = request.user_id
        data = request.get_json()
        
        new_plan = data.get('new_plan')
        billing_info = data.get('billing_info', {})
        
        if not new_plan:
            return jsonify({'error': 'New plan is required'}), 400
        
        result = multi_user_service.upgrade_account(account_id, user_id, new_plan, billing_info)
        
        return jsonify({'result': result}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/accounts/<account_id>/billing-history', methods=['GET'])
@require_auth
def get_account_billing_history(account_id):
    """Get account billing history"""
    try:
        user_id = request.user_id
        
        result = multi_user_service.get_account_billing_history(account_id, user_id)
        
        return jsonify({'billing': result}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/accounts/<account_id>/cancel', methods=['POST'])
@require_auth
def cancel_account(account_id):
    """Cancel an account"""
    try:
        user_id = request.user_id
        data = request.get_json()
        
        cancellation_reason = data.get('cancellation_reason')
        
        result = multi_user_service.cancel_account(account_id, user_id, cancellation_reason)
        
        return jsonify({'result': result}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Advisor endpoints
@app.route('/api/advisor/account', methods=['POST'])
@require_auth
def create_advisor_account():
    """Create a new advisor account"""
    try:
        user_id = request.user_id
        data = request.get_json()
        
        advisor_info = data.get('advisor_info', {})
        
        result = advisor_service.create_advisor_account(user_id, advisor_info)
        
        return jsonify({'result': result}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/advisor/clients', methods=['GET'])
@require_auth
def get_advisor_clients():
    """Get all clients for an advisor"""
    try:
        user_id = request.user_id
        status = request.args.get('status', 'all')
        
        result = advisor_service.get_advisor_clients(user_id, status)
        
        return jsonify({'clients': result}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/advisor/clients', methods=['POST'])
@require_auth
def add_client():
    """Add a new client to advisor's portfolio"""
    try:
        user_id = request.user_id
        data = request.get_json()
        
        client_data = data.get('client_data', {})
        
        result = advisor_service.add_client(user_id, client_data)
        
        return jsonify({'result': result}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/advisor/clients/<client_id>', methods=['GET'])
@require_auth
def get_client_details(client_id):
    """Get detailed information about a specific client"""
    try:
        user_id = request.user_id
        
        result = advisor_service.get_client_details(user_id, client_id)
        
        return jsonify({'client': result}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/advisor/clients/<client_id>', methods=['PUT'])
@require_auth
def update_client_info(client_id):
    """Update client information"""
    try:
        user_id = request.user_id
        data = request.get_json()
        
        updated_data = data.get('updated_data', {})
        
        result = advisor_service.update_client_info(user_id, client_id, updated_data)
        
        return jsonify({'result': result}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/advisor/clients/bulk-import', methods=['POST'])
@require_auth
def bulk_import_clients():
    """Bulk import clients from CSV data"""
    try:
        user_id = request.user_id
        data = request.get_json()
        
        csv_data = data.get('csv_data')
        
        if not csv_data:
            return jsonify({'error': 'CSV data is required'}), 400
        
        result = advisor_service.bulk_import_clients(user_id, csv_data)
        
        return jsonify({'result': result}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/advisor/clients/<client_id>/report', methods=['GET'])
@require_auth
def generate_client_report(client_id):
    """Generate a report for a specific client"""
    try:
        user_id = request.user_id
        report_type = request.args.get('type', 'comprehensive')
        
        result = advisor_service.generate_client_report(user_id, client_id, report_type)
        
        return jsonify({'report': result}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/advisor/dashboard', methods=['GET'])
@require_auth
def get_advisor_dashboard():
    """Get advisor dashboard data"""
    try:
        user_id = request.user_id
        
        result = advisor_service.get_advisor_dashboard(user_id)
        
        return jsonify({'dashboard': result}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/advisor/meetings', methods=['POST'])
@require_auth
def schedule_client_meeting():
    """Schedule a meeting with a client"""
    try:
        user_id = request.user_id
        data = request.get_json()
        
        client_id = data.get('client_id')
        meeting_data = data.get('meeting_data', {})
        
        if not client_id:
            return jsonify({'error': 'Client ID is required'}), 400
        
        result = advisor_service.schedule_client_meeting(user_id, client_id, meeting_data)
        
        return jsonify({'result': result}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/advisor/schedule', methods=['GET'])
@require_auth
def get_advisor_schedule():
    """Get advisor's schedule for a date range"""
    try:
        user_id = request.user_id
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        if not start_date or not end_date:
            return jsonify({'error': 'Start date and end date are required'}), 400
        
        result = advisor_service.get_advisor_schedule(user_id, start_date, end_date)
        
        return jsonify({'schedule': result}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/advisor/upgrade', methods=['POST'])
@require_auth
def upgrade_advisor_plan():
    """Upgrade advisor to a higher plan"""
    try:
        user_id = request.user_id
        data = request.get_json()
        
        new_plan = data.get('new_plan')
        billing_info = data.get('billing_info', {})
        
        if not new_plan:
            return jsonify({'error': 'New plan is required'}), 400
        
        result = advisor_service.upgrade_advisor_plan(user_id, new_plan, billing_info)
        
        return jsonify({'result': result}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/advisor/analytics', methods=['GET'])
@require_auth
def get_advisor_analytics():
    """Get advisor analytics and insights"""
    try:
        user_id = request.user_id
        period = request.args.get('period', 'monthly')
        
        result = advisor_service.get_advisor_analytics(user_id, period)
        
        return jsonify({'analytics': result}), 200
        
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
    app.run(debug=True, host='0.0.0.0', port=5000)
