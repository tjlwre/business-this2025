from flask import Blueprint, request, jsonify
from core.utils.decorators import require_auth
from core.utils.error_handler import handle_errors
from core.utils.validators import validate_financial_data
from services.financial_service import FinancialService


profile_bp = Blueprint('profile', __name__)
financial_service = FinancialService()


@profile_bp.route('', methods=['GET'])
@require_auth
@handle_errors
def get_financial_profile():
    user_id = request.user_id
    profile = financial_service.get_financial_profile(user_id)
    if profile:
        return jsonify({'profile': profile}), 200
    return jsonify({'error': 'Financial profile not found'}), 404


@profile_bp.route('', methods=['POST', 'PUT'])
@require_auth
@handle_errors
def update_financial_profile():
    user_id = request.user_id
    data = request.get_json()
    validation_result = validate_financial_data(data)
    if not validation_result['valid']:
        return jsonify({'error': validation_result['error']}), 400

    result = financial_service.update_financial_profile(user_id, data)
    if result['success']:
        return jsonify({'message': 'Financial profile updated successfully', 'profile': result['profile']}), 200
    return jsonify({'error': result['error']}), 400


