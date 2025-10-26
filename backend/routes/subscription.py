from flask import Blueprint, request, jsonify
from core.utils.decorators import require_auth
from core.utils.error_handler import handle_errors
from services.subscription_service import SubscriptionService


subscription_bp = Blueprint('subscription', __name__)
subscription_service = SubscriptionService()


@subscription_bp.route('/status', methods=['GET'])
@require_auth
@handle_errors
def get_subscription_status():
    user_id = request.user_id
    result = subscription_service.get_subscription_status(user_id)
    return jsonify({'subscription': result}), 200


@subscription_bp.route('/upgrade', methods=['POST'])
@require_auth
@handle_errors
def upgrade_subscription():
    user_id = request.user_id
    data = request.get_json()
    plan = data.get('plan')
    if not plan or plan not in ['premium', 'pro']:
        return jsonify({'error': 'Invalid plan. Must be premium or pro'}), 400

    result = subscription_service.create_subscription(user_id, plan)
    if result['success']:
        return jsonify({'message': 'Subscription created successfully', 'checkout_url': result['checkout_url']}), 200
    return jsonify({'error': result['error']}), 400


