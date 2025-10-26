from flask import Blueprint, request, jsonify
from core.utils.decorators import require_auth
from core.utils.error_handler import handle_errors
from services.advisor_service import AdvisorService

advisor_bp = Blueprint('advisor', __name__)
advisor_service = AdvisorService()

@advisor_bp.route('/account', methods=['POST'])
@require_auth
@handle_errors
def create_advisor_account():
    """Create a new advisor account"""
    user_id = request.user_id
    data = request.get_json()
    
    advisor_info = data.get('advisor_info', {})
    
    result = advisor_service.create_advisor_account(user_id, advisor_info)
    return jsonify({'result': result}), 200

@advisor_bp.route('/clients', methods=['GET'])
@require_auth
@handle_errors
def get_advisor_clients():
    """Get all clients for an advisor"""
    user_id = request.user_id
    status = request.args.get('status', 'all')
    
    result = advisor_service.get_advisor_clients(user_id, status)
    return jsonify({'clients': result}), 200

@advisor_bp.route('/clients', methods=['POST'])
@require_auth
@handle_errors
def add_client():
    """Add a new client to advisor's portfolio"""
    user_id = request.user_id
    data = request.get_json()
    
    client_data = data.get('client_data', {})
    
    result = advisor_service.add_client(user_id, client_data)
    return jsonify({'result': result}), 200

@advisor_bp.route('/clients/<client_id>', methods=['GET'])
@require_auth
@handle_errors
def get_client_details(client_id):
    """Get detailed information about a specific client"""
    user_id = request.user_id
    result = advisor_service.get_client_details(user_id, client_id)
    return jsonify({'client': result}), 200

@advisor_bp.route('/clients/<client_id>', methods=['PUT'])
@require_auth
@handle_errors
def update_client_info(client_id):
    """Update client information"""
    user_id = request.user_id
    data = request.get_json()
    
    updated_data = data.get('updated_data', {})
    
    result = advisor_service.update_client_info(user_id, client_id, updated_data)
    return jsonify({'result': result}), 200

@advisor_bp.route('/clients/bulk-import', methods=['POST'])
@require_auth
@handle_errors
def bulk_import_clients():
    """Bulk import clients from CSV data"""
    user_id = request.user_id
    data = request.get_json()
    
    csv_data = data.get('csv_data')
    
    if not csv_data:
        return jsonify({'error': 'CSV data is required'}), 400
    
    result = advisor_service.bulk_import_clients(user_id, csv_data)
    return jsonify({'result': result}), 200

@advisor_bp.route('/clients/<client_id>/report', methods=['GET'])
@require_auth
@handle_errors
def generate_client_report(client_id):
    """Generate a report for a specific client"""
    user_id = request.user_id
    report_type = request.args.get('type', 'comprehensive')
    
    result = advisor_service.generate_client_report(user_id, client_id, report_type)
    return jsonify({'report': result}), 200

@advisor_bp.route('/dashboard', methods=['GET'])
@require_auth
@handle_errors
def get_advisor_dashboard():
    """Get advisor dashboard data"""
    user_id = request.user_id
    result = advisor_service.get_advisor_dashboard(user_id)
    return jsonify({'dashboard': result}), 200

@advisor_bp.route('/meetings', methods=['POST'])
@require_auth
@handle_errors
def schedule_client_meeting():
    """Schedule a meeting with a client"""
    user_id = request.user_id
    data = request.get_json()
    
    client_id = data.get('client_id')
    meeting_data = data.get('meeting_data', {})
    
    if not client_id:
        return jsonify({'error': 'Client ID is required'}), 400
    
    result = advisor_service.schedule_client_meeting(user_id, client_id, meeting_data)
    return jsonify({'result': result}), 200

@advisor_bp.route('/schedule', methods=['GET'])
@require_auth
@handle_errors
def get_advisor_schedule():
    """Get advisor's schedule for a date range"""
    user_id = request.user_id
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    if not start_date or not end_date:
        return jsonify({'error': 'Start date and end date are required'}), 400
    
    result = advisor_service.get_advisor_schedule(user_id, start_date, end_date)
    return jsonify({'schedule': result}), 200

@advisor_bp.route('/upgrade', methods=['POST'])
@require_auth
@handle_errors
def upgrade_advisor_plan():
    """Upgrade advisor to a higher plan"""
    user_id = request.user_id
    data = request.get_json()
    
    new_plan = data.get('new_plan')
    billing_info = data.get('billing_info', {})
    
    if not new_plan:
        return jsonify({'error': 'New plan is required'}), 400
    
    result = advisor_service.upgrade_advisor_plan(user_id, new_plan, billing_info)
    return jsonify({'result': result}), 200

@advisor_bp.route('/analytics', methods=['GET'])
@require_auth
@handle_errors
def get_advisor_analytics():
    """Get advisor analytics and insights"""
    user_id = request.user_id
    period = request.args.get('period', 'monthly')
    
    result = advisor_service.get_advisor_analytics(user_id, period)
    return jsonify({'analytics': result}), 200
