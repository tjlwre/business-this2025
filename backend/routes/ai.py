from flask import Blueprint, request, jsonify
from core.utils.decorators import require_auth, require_subscription
from core.utils.error_handler import handle_errors
from services.ai_service import AIService
from services.financial_service import FinancialService


ai_bp = Blueprint('ai', __name__)
ai_service = AIService()
financial_service = FinancialService()


@ai_bp.route('/coaching', methods=['POST'])
@require_auth
@require_subscription('premium')
@handle_errors
def get_ai_coaching():
    user_id = request.user_id
    data = request.get_json()
    question = data.get('question', '')
    if not question:
        return jsonify({'error': 'Question is required'}), 400
    profile_response, status = financial_service.get_financial_profile(user_id)
    if status != 200:
        return jsonify({'error': 'Financial profile not found'}), 404
    profile = profile_response['profile']
    result = ai_service.get_financial_coaching(profile, question)
    return jsonify({'coaching': result}), 200


@ai_bp.route('/spending-recommendations', methods=['GET'])
@require_auth
@require_subscription('premium')
@handle_errors
def get_spending_recommendations():
    user_id = request.user_id
    profile_response, status = financial_service.get_financial_profile(user_id)
    if status != 200:
        return jsonify({'error': 'Financial profile not found'}), 404
    profile = profile_response['profile']
    try:
        recent_transactions = financial_service.get_recent_transactions(user_id, limit=5)
    except Exception:
        recent_transactions = []
    result = ai_service.get_spending_recommendations(profile, recent_transactions)
    return jsonify({'recommendations': result}), 200


@ai_bp.route('/daily-tip', methods=['GET'])
@require_auth
@require_subscription('premium')
@handle_errors
def get_daily_tip():
    user_id = request.user_id
    profile_response, status = financial_service.get_financial_profile(user_id)
    if status != 200:
        return jsonify({'error': 'Financial profile not found'}), 404
    profile = profile_response['profile']
    result = ai_service.get_daily_financial_tip(profile)
    return jsonify({'daily_tip': result}), 200


@ai_bp.route('/goal-analysis', methods=['GET'])
@require_auth
@require_subscription('premium')
@handle_errors
def get_goal_analysis():
    user_id = request.user_id
    profile_response, status = financial_service.get_financial_profile(user_id)
    if status != 200:
        return jsonify({'error': 'Financial profile not found'}), 404
    profile = profile_response['profile']
    goals_response, goals_status = financial_service.get_savings_goals(user_id)
    goals = goals_response if goals_status == 200 else []
    result = ai_service.analyze_financial_goals(profile, goals)
    return jsonify({'goal_analysis': result}), 200


@ai_bp.route('/investment-advice', methods=['POST'])
@require_auth
@require_subscription('pro')
@handle_errors
def get_investment_advice():
    user_id = request.user_id
    data = request.get_json()
    profile_response, status = financial_service.get_financial_profile(user_id)
    if status != 200:
        return jsonify({'error': 'Financial profile not found'}), 404
    profile = profile_response['profile']
    current_portfolio = data.get('portfolio', {
        'total_value': 0,
        'stock_percentage': 0,
        'bond_percentage': 0,
        'cash_percentage': 100
    })
    result = ai_service.get_investment_advice(profile, current_portfolio)
    return jsonify({'investment_advice': result}), 200


