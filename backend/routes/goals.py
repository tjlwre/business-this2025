from flask import Blueprint, request, jsonify
from core.utils.decorators import require_auth
from core.utils.error_handler import handle_errors
from services.financial_service import FinancialService


goals_bp = Blueprint('goals', __name__)
financial_service = FinancialService()


@goals_bp.route('', methods=['GET'])
@require_auth
@handle_errors
def get_savings_goals():
    user_id = request.user_id
    goals = financial_service.get_savings_goals(user_id)
    return jsonify({'goals': goals}), 200


@goals_bp.route('', methods=['POST'])
@require_auth
@handle_errors
def create_savings_goal():
    user_id = request.user_id
    data = request.get_json()
    if not data.get('name') or not data.get('target_amount'):
        return jsonify({'error': 'Goal name and target amount are required'}), 400

    result = financial_service.create_savings_goal(user_id, data)
    if result['success']:
        return jsonify({'message': 'Savings goal created successfully', 'goal': result['goal']}), 201
    return jsonify({'error': result['error']}), 400


@goals_bp.route('/<goal_id>', methods=['PUT'])
@require_auth
@handle_errors
def update_savings_goal(goal_id):
    user_id = request.user_id
    data = request.get_json()
    result = financial_service.update_savings_goal(user_id, goal_id, data)
    if result['success']:
        return jsonify({'message': 'Savings goal updated successfully', 'goal': result['goal']}), 200
    return jsonify({'error': result['error']}), 400


@goals_bp.route('/<goal_id>', methods=['DELETE'])
@require_auth
@handle_errors
def delete_savings_goal(goal_id):
    user_id = request.user_id
    result = financial_service.delete_savings_goal(user_id, goal_id)
    if result['success']:
        return jsonify({'message': 'Savings goal deleted successfully'}), 200
    return jsonify({'error': result['error']}), 400


