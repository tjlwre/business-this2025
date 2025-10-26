from flask import Blueprint, request, jsonify
from core.utils.decorators import require_auth, require_subscription
from core.utils.error_handler import handle_errors
from services.email_service import EmailService
from services.auth_service import AuthService
from services.financial_service import FinancialService

email_bp = Blueprint('email', __name__)
email_service = EmailService()
auth_service = AuthService()
financial_service = FinancialService()

@email_bp.route('/welcome', methods=['POST'])
@handle_errors
def send_welcome_email():
    """Send welcome email to new user"""
    data = request.get_json()
    user_email = data.get('email')
    user_name = data.get('name', 'User')
    
    if not user_email:
        return jsonify({'error': 'Email is required'}), 400
    
    result = email_service.send_welcome_email(user_email, user_name)
    return jsonify({'result': result}), 200

@email_bp.route('/onboarding', methods=['POST'])
@require_auth
@handle_errors
def send_onboarding_sequence():
    """Send onboarding email sequence"""
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

@email_bp.route('/newsletter', methods=['POST'])
@require_auth
@handle_errors
def send_weekly_newsletter():
    """Send weekly newsletter"""
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

@email_bp.route('/goal-achievement', methods=['POST'])
@require_auth
@handle_errors
def send_goal_achievement_email():
    """Send goal achievement email"""
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

@email_bp.route('/upgrade', methods=['POST'])
@require_auth
@handle_errors
def send_upgrade_email():
    """Send subscription upgrade email"""
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

@email_bp.route('/daily-tip', methods=['POST'])
@require_auth
@require_subscription('premium')
@handle_errors
def send_daily_tip_email():
    """Send daily financial tip email"""
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

@email_bp.route('/engagement', methods=['POST'])
@require_auth
@handle_errors
def send_engagement_email():
    """Send re-engagement email"""
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
