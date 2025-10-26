from flask import Blueprint, request, jsonify
from core.utils.decorators import require_auth, require_subscription
from core.utils.error_handler import handle_errors
from services.reports_service import ReportsService
from services.financial_service import FinancialService
import base64
from datetime import datetime


reports_bp = Blueprint('reports', __name__)
reports_service = ReportsService()
financial_service = FinancialService()


@reports_bp.route('/pdf', methods=['GET'])
@require_auth
@require_subscription('premium')
@handle_errors
def generate_pdf_report():
    user_id = request.user_id
    profile_response, status = financial_service.get_financial_profile(user_id)
    if status != 200:
        return jsonify({'error': 'Financial profile not found'}), 404
    profile = profile_response['profile']
    goals_response, goals_status = financial_service.get_savings_goals(user_id)
    goals = goals_response if goals_status == 200 else []
    health_response, health_status = financial_service.calculate_financial_health_score(user_id)
    health = health_response.get('financial_health', {}) if health_status == 200 else {}
    pdf_data = reports_service.generate_financial_report_pdf(profile, goals, health)
    pdf_base64 = base64.b64encode(pdf_data).decode()
    return jsonify({'pdf_data': pdf_base64, 'filename': f'financial_report_{datetime.now().strftime("%Y%m%d")}.pdf'}), 200


@reports_bp.route('/excel', methods=['GET'])
@require_auth
@require_subscription('premium')
@handle_errors
def generate_excel_export():
    user_id = request.user_id
    profile_response, status = financial_service.get_financial_profile(user_id)
    if status != 200:
        return jsonify({'error': 'Financial profile not found'}), 404
    profile = profile_response['profile']
    goals_response, goals_status = financial_service.get_savings_goals(user_id)
    goals = goals_response if goals_status == 200 else []
    try:
        transactions = financial_service.get_user_transactions(user_id)
    except Exception:
        transactions = []
    excel_data = reports_service.generate_excel_export(profile, goals, transactions)
    excel_base64 = base64.b64encode(excel_data).decode()
    return jsonify({'excel_data': excel_base64, 'filename': f'financial_data_{datetime.now().strftime("%Y%m%d")}.xlsx'}), 200


@reports_bp.route('/email-summary', methods=['GET'])
@require_auth
@handle_errors
def generate_email_summary():
    user_id = request.user_id
    profile_response, status = financial_service.get_financial_profile(user_id)
    if status != 200:
        return jsonify({'error': 'Financial profile not found'}), 404
    profile = profile_response['profile']
    goals_response, goals_status = financial_service.get_savings_goals(user_id)
    goals = goals_response if goals_status == 200 else []
    try:
        transactions = financial_service.get_user_transactions(user_id)
    except Exception:
        transactions = []
    summary = reports_service.generate_email_summary(profile, goals, transactions)
    return jsonify({'email_summary': summary}), 200


@reports_bp.route('/chart', methods=['POST'])
@require_auth
@require_subscription('premium')
@handle_errors
def generate_chart():
    data = request.get_json()
    chart_type = data.get('chart_type')
    chart_data = data.get('data', {})
    if not chart_type:
        return jsonify({'error': 'Chart type is required'}), 400
    chart_base64 = reports_service.create_financial_chart(chart_type, chart_data)
    return jsonify({'chart_data': chart_base64, 'chart_type': chart_type}), 200


