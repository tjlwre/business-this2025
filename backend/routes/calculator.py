from flask import Blueprint, request, jsonify
from core.utils.decorators import require_auth
from core.utils.error_handler import handle_errors
from services.financial_service import FinancialService


calculator_bp = Blueprint('calculator', __name__)
financial_service = FinancialService()


@calculator_bp.route('/safe-spend', methods=['POST'])
@require_auth
@handle_errors
def calculate_safe_spend():
    user_id = request.user_id
    data = request.get_json()
    profile = financial_service.get_financial_profile(user_id)
    if not profile:
        return jsonify({'error': 'Financial profile not found'}), 404

    result = financial_service.calculate_safe_spending(
        user_id,
        data.get('savings_goal'),
        data.get('months_for_goal')
    )
    return jsonify({'safe_spending': result}), 200


@calculator_bp.route('/financial-health', methods=['GET'])
@require_auth
@handle_errors
def calculate_financial_health():
    user_id = request.user_id
    result = financial_service.calculate_financial_health_score(user_id)
    return jsonify({'financial_health': result}), 200


