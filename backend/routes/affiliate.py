from flask import Blueprint, request, jsonify
from core.utils.decorators import require_auth
from core.utils.error_handler import handle_errors
from services.affiliate_service import AffiliateService
from services.financial_service import FinancialService

affiliate_bp = Blueprint('affiliate', __name__)
affiliate_service = AffiliateService()
financial_service = FinancialService()

@affiliate_bp.route('/products', methods=['GET'])
@require_auth
@handle_errors
def get_affiliate_products():
    """Get affiliate products based on user profile"""
    user_id = request.user_id
    category = request.args.get('category', 'all')
    
    # Get user's financial profile for personalization
    profile_response, status = financial_service.get_financial_profile(user_id)
    profile = profile_response.get('profile', {}) if status == 200 else {}
    
    result = affiliate_service.get_affiliate_products(category, profile)
    return jsonify({'products': result}), 200

@affiliate_bp.route('/track-referral', methods=['POST'])
@require_auth
@handle_errors
def track_referral():
    """Track referral click"""
    user_id = request.user_id
    data = request.get_json()
    
    product_id = data.get('product_id')
    referral_data = data.get('referral_data', {})
    
    if not product_id:
        return jsonify({'error': 'Product ID is required'}), 400
    
    result = affiliate_service.track_referral(user_id, product_id, referral_data)
    return jsonify({'result': result}), 200

@affiliate_bp.route('/stats', methods=['GET'])
@require_auth
@handle_errors
def get_affiliate_stats():
    """Get user's affiliate statistics"""
    user_id = request.user_id
    result = affiliate_service.get_user_affiliate_stats(user_id)
    return jsonify({'stats': result}), 200

@affiliate_bp.route('/commission-breakdown', methods=['GET'])
@require_auth
@handle_errors
def get_commission_breakdown():
    """Get detailed commission breakdown"""
    user_id = request.user_id
    result = affiliate_service.get_commission_breakdown(user_id)
    return jsonify({'breakdown': result}), 200

@affiliate_bp.route('/generate-link', methods=['POST'])
@require_auth
@handle_errors
def generate_affiliate_link():
    """Generate personalized affiliate link"""
    user_id = request.user_id
    data = request.get_json()
    
    product_id = data.get('product_id')
    
    if not product_id:
        return jsonify({'error': 'Product ID is required'}), 400
    
    link = affiliate_service.generate_affiliate_link(user_id, product_id)
    
    if not link:
        return jsonify({'error': 'Failed to generate affiliate link'}), 500
    
    return jsonify({'affiliate_link': link}), 200
