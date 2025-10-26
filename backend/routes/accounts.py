from flask import Blueprint, request, jsonify
from core.utils.decorators import require_auth
from core.utils.error_handler import handle_errors
from services.multi_user_service import MultiUserService

accounts_bp = Blueprint('accounts', __name__)
multi_user_service = MultiUserService()

@accounts_bp.route('/family', methods=['POST'])
@require_auth
@handle_errors
def create_family_account():
    """Create a new family account"""
    user_id = request.user_id
    data = request.get_json()
    
    family_name = data.get('family_name')
    billing_info = data.get('billing_info', {})
    
    if not family_name:
        return jsonify({'error': 'Family name is required'}), 400
    
    result = multi_user_service.create_family_account(user_id, family_name, billing_info)
    return jsonify({'result': result}), 200

@accounts_bp.route('/enterprise', methods=['POST'])
@require_auth
@handle_errors
def create_enterprise_account():
    """Create a new enterprise account"""
    user_id = request.user_id
    data = request.get_json()
    
    company_name = data.get('company_name')
    enterprise_info = data.get('enterprise_info', {})
    
    if not company_name:
        return jsonify({'error': 'Company name is required'}), 400
    
    result = multi_user_service.create_enterprise_account(user_id, company_name, enterprise_info)
    return jsonify({'result': result}), 200

@accounts_bp.route('/<account_id>/invite', methods=['POST'])
@require_auth
@handle_errors
def invite_user_to_account(account_id):
    """Invite a user to join an account"""
    user_id = request.user_id
    data = request.get_json()
    
    email = data.get('email')
    role = data.get('role', 'member')
    
    if not email:
        return jsonify({'error': 'Email is required'}), 400
    
    result = multi_user_service.invite_user_to_account(account_id, user_id, email, role)
    return jsonify({'result': result}), 200

@accounts_bp.route('/invitations/<invitation_token>/accept', methods=['POST'])
@require_auth
@handle_errors
def accept_invitation(invitation_token):
    """Accept an invitation to join an account"""
    user_id = request.user_id
    result = multi_user_service.accept_invitation(invitation_token, user_id)
    return jsonify({'result': result}), 200

@accounts_bp.route('/<account_id>/members', methods=['GET'])
@require_auth
@handle_errors
def get_account_members(account_id):
    """Get all members of an account"""
    user_id = request.user_id
    result = multi_user_service.get_account_members(account_id, user_id)
    return jsonify({'members': result}), 200

@accounts_bp.route('/<account_id>/members/<member_id>/role', methods=['PUT'])
@require_auth
@handle_errors
def update_member_role(account_id, member_id):
    """Update a member's role in the account"""
    user_id = request.user_id
    data = request.get_json()
    
    new_role = data.get('role')
    
    if not new_role:
        return jsonify({'error': 'Role is required'}), 400
    
    result = multi_user_service.update_member_role(account_id, user_id, member_id, new_role)
    return jsonify({'result': result}), 200

@accounts_bp.route('/<account_id>/members/<member_id>', methods=['DELETE'])
@require_auth
@handle_errors
def remove_member_from_account(account_id, member_id):
    """Remove a member from the account"""
    user_id = request.user_id
    result = multi_user_service.remove_member_from_account(account_id, user_id, member_id)
    return jsonify({'result': result}), 200

@accounts_bp.route('/<account_id>/shared-goals', methods=['GET'])
@require_auth
@handle_errors
def get_shared_goals(account_id):
    """Get shared goals for the account"""
    user_id = request.user_id
    result = multi_user_service.get_shared_goals(account_id, user_id)
    return jsonify({'goals': result}), 200

@accounts_bp.route('/<account_id>/shared-goals', methods=['POST'])
@require_auth
@handle_errors
def create_shared_goal(account_id):
    """Create a shared goal for the account"""
    user_id = request.user_id
    data = request.get_json()
    
    goal_data = data.get('goal_data', {})
    
    result = multi_user_service.create_shared_goal(account_id, user_id, goal_data)
    return jsonify({'result': result}), 200

@accounts_bp.route('/<account_id>/dashboard', methods=['GET'])
@require_auth
@handle_errors
def get_family_dashboard(account_id):
    """Get family dashboard data"""
    user_id = request.user_id
    result = multi_user_service.get_family_dashboard(account_id, user_id)
    return jsonify({'dashboard': result}), 200

@accounts_bp.route('/<account_id>/enterprise-settings', methods=['GET'])
@require_auth
@handle_errors
def get_enterprise_settings(account_id):
    """Get enterprise account settings"""
    user_id = request.user_id
    result = multi_user_service.get_enterprise_settings(account_id, user_id)
    return jsonify({'settings': result}), 200

@accounts_bp.route('/<account_id>/enterprise-settings', methods=['PUT'])
@require_auth
@handle_errors
def update_enterprise_settings(account_id):
    """Update enterprise account settings"""
    user_id = request.user_id
    data = request.get_json()
    
    settings = data.get('settings', {})
    
    result = multi_user_service.update_enterprise_settings(account_id, user_id, settings)
    return jsonify({'result': result}), 200

@accounts_bp.route('/<account_id>/usage-stats', methods=['GET'])
@require_auth
@handle_errors
def get_account_usage_stats(account_id):
    """Get account usage statistics"""
    user_id = request.user_id
    result = multi_user_service.get_account_usage_stats(account_id, user_id)
    return jsonify({'stats': result}), 200

@accounts_bp.route('/<account_id>/upgrade', methods=['POST'])
@require_auth
@handle_errors
def upgrade_account(account_id):
    """Upgrade account to a higher plan"""
    user_id = request.user_id
    data = request.get_json()
    
    new_plan = data.get('new_plan')
    billing_info = data.get('billing_info', {})
    
    if not new_plan:
        return jsonify({'error': 'New plan is required'}), 400
    
    result = multi_user_service.upgrade_account(account_id, user_id, new_plan, billing_info)
    return jsonify({'result': result}), 200

@accounts_bp.route('/<account_id>/billing-history', methods=['GET'])
@require_auth
@handle_errors
def get_account_billing_history(account_id):
    """Get account billing history"""
    user_id = request.user_id
    result = multi_user_service.get_account_billing_history(account_id, user_id)
    return jsonify({'billing': result}), 200

@accounts_bp.route('/<account_id>/cancel', methods=['POST'])
@require_auth
@handle_errors
def cancel_account(account_id):
    """Cancel an account"""
    user_id = request.user_id
    data = request.get_json()
    
    cancellation_reason = data.get('cancellation_reason')
    
    result = multi_user_service.cancel_account(account_id, user_id, cancellation_reason)
    return jsonify({'result': result}), 200
