from flask import Blueprint, request, jsonify
from core.utils.decorators import require_auth, require_subscription
from core.utils.error_handler import handle_errors
from services.investment_service import InvestmentService
from services.financial_service import FinancialService


investment_bp = Blueprint('investment', __name__)
investment_service = InvestmentService()
financial_service = FinancialService()


@investment_bp.route('/asset-allocation', methods=['POST'])
@require_auth
@require_subscription('premium')
@handle_errors
def calculate_asset_allocation():
    data = request.get_json()
    age = data.get('age', 30)
    risk_tolerance = data.get('risk_tolerance', 'moderate')
    investment_amount = data.get('investment_amount', 10000)
    result = investment_service.calculate_asset_allocation(age, risk_tolerance, investment_amount)
    return jsonify({'asset_allocation': result}), 200


@investment_bp.route('/retirement-planning', methods=['POST'])
@require_auth
@require_subscription('premium')
@handle_errors
def calculate_retirement_planning():
    data = request.get_json()
    result = investment_service.calculate_retirement_needs(
        data.get('current_age', 30),
        data.get('retirement_age', 65),
        data.get('current_savings', 0),
        data.get('monthly_income', 5000),
        data.get('desired_retirement_income', 0)
    )
    return jsonify({'retirement_planning': result}), 200


@investment_bp.route('/compound-interest', methods=['POST'])
@require_auth
@handle_errors
def calculate_compound_interest():
    data = request.get_json()
    result = investment_service.calculate_compound_interest(
        data.get('principal', 0),
        data.get('monthly_contribution', 0),
        data.get('annual_rate', 0.07),
        data.get('years', 10)
    )
    return jsonify({'compound_interest': result}), 200


@investment_bp.route('/tax-optimization', methods=['POST'])
@require_auth
@require_subscription('premium')
@handle_errors
def calculate_tax_optimization():
    data = request.get_json()
    result = investment_service.calculate_tax_optimization(
        data.get('income', 50000),
        data.get('filing_status', 'single'),
        data.get('deductions', 0),
        data.get('credits', 0)
    )
    return jsonify({'tax_optimization': result}), 200


@investment_bp.route('/what-if-scenarios', methods=['POST'])
@require_auth
@require_subscription('premium')
@handle_errors
def calculate_what_if_scenarios():
    data = request.get_json()
    result = investment_service.calculate_what_if_scenarios(
        data.get('base_income', 5000),
        data.get('base_expenses', 3000),
        data.get('scenarios', [])
    )
    return jsonify({'what_if_scenarios': result}), 200


@investment_bp.route('/recommendations', methods=['GET'])
@require_auth
@require_subscription('premium')
@handle_errors
def get_investment_recommendations():
    user_id = request.user_id
    profile_response, status = financial_service.get_financial_profile(user_id)
    if status != 200:
        return jsonify({'error': 'Financial profile not found'}), 404
    profile = profile_response['profile']
    age = profile.get('age', 30)
    income = profile.get('monthly_income', 0) * 12
    risk_tolerance = profile.get('risk_tolerance', 'moderate')
    current_investments = profile.get('emergency_fund_current', 0)
    result = investment_service.get_investment_recommendations(age, income, risk_tolerance, current_investments)
    return jsonify({'investment_recommendations': result}), 200


