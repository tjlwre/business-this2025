from flask import Blueprint, request, jsonify
from core.utils.decorators import require_auth
from core.utils.error_handler import handle_errors
from services.admin_service import AdminService

admin_bp = Blueprint('admin', __name__)
admin_service = AdminService()

@admin_bp.route('/dashboard', methods=['GET'])
@require_auth
@handle_errors
def get_admin_dashboard():
    """Get admin dashboard metrics"""
    user_id = request.user_id
    if not admin_service.is_admin(user_id):
        return jsonify({'error': 'Admin access required'}), 403
    
    result = admin_service.get_dashboard_metrics()
    return jsonify({'dashboard': result}), 200

@admin_bp.route('/users', methods=['GET'])
@require_auth
@handle_errors
def get_admin_users():
    """Get paginated user list"""
    user_id = request.user_id
    if not admin_service.is_admin(user_id):
        return jsonify({'error': 'Admin access required'}), 403
    
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 50))
    search = request.args.get('search', '')
    
    result = admin_service.get_user_list(page, limit, search)
    return jsonify({'users': result}), 200

@admin_bp.route('/users/<user_id>', methods=['GET'])
@require_auth
@handle_errors
def get_admin_user_details(user_id):
    """Get detailed user information"""
    admin_user_id = request.user_id
    if not admin_service.is_admin(admin_user_id):
        return jsonify({'error': 'Admin access required'}), 403
    
    result = admin_service.get_user_details(user_id)
    return jsonify({'user_details': result}), 200

@admin_bp.route('/users/<user_id>/subscription', methods=['PUT'])
@require_auth
@handle_errors
def update_admin_user_subscription(user_id):
    """Update user subscription"""
    admin_user_id = request.user_id
    if not admin_service.is_admin(admin_user_id):
        return jsonify({'error': 'Admin access required'}), 403
    
    data = request.get_json()
    tier = data.get('tier')
    status = data.get('status')
    
    if not tier or not status:
        return jsonify({'error': 'Tier and status are required'}), 400
    
    result = admin_service.update_user_subscription(user_id, tier, status)
    return jsonify({'result': result}), 200

@admin_bp.route('/support-tickets', methods=['GET'])
@require_auth
@handle_errors
def get_admin_support_tickets():
    """Get support tickets"""
    user_id = request.user_id
    if not admin_service.is_admin(user_id):
        return jsonify({'error': 'Admin access required'}), 403
    
    status = request.args.get('status', 'all')
    result = admin_service.get_support_tickets(status)
    return jsonify({'tickets': result}), 200

@admin_bp.route('/support-tickets/<ticket_id>', methods=['PUT'])
@require_auth
@handle_errors
def update_admin_support_ticket(ticket_id):
    """Update support ticket"""
    user_id = request.user_id
    if not admin_service.is_admin(user_id):
        return jsonify({'error': 'Admin access required'}), 403
    
    data = request.get_json()
    status = data.get('status')
    response = data.get('response', '')
    
    if not status:
        return jsonify({'error': 'Status is required'}), 400
    
    result = admin_service.update_support_ticket(ticket_id, status, response)
    return jsonify({'result': result}), 200
