from flask import Blueprint, request, jsonify
from core.utils.decorators import require_auth
from core.utils.error_handler import handle_errors
from services.course_service import CourseService
from services.financial_service import FinancialService

courses_bp = Blueprint('courses', __name__)
course_service = CourseService()
financial_service = FinancialService()

@courses_bp.route('/catalog', methods=['GET'])
@handle_errors
def get_course_catalog():
    """Get course catalog with filtering options"""
    category = request.args.get('category', 'all')
    difficulty = request.args.get('difficulty', 'all')
    
    result = course_service.get_course_catalog(category, difficulty)
    return jsonify({'catalog': result}), 200

@courses_bp.route('/<course_id>', methods=['GET'])
@handle_errors
def get_course_details(course_id):
    """Get detailed information about a specific course"""
    result = course_service.get_course_details(course_id)
    
    if 'error' in result:
        return jsonify(result), 404
    
    return jsonify({'course': result}), 200

@courses_bp.route('/<course_id>/enroll', methods=['POST'])
@require_auth
@handle_errors
def enroll_in_course(course_id):
    """Enroll user in a course"""
    user_id = request.user_id
    data = request.get_json()
    
    payment_data = data.get('payment_data', {})
    
    result = course_service.enroll_user_in_course(user_id, course_id, payment_data)
    
    if 'error' in result:
        return jsonify(result), 400
    
    return jsonify({'enrollment': result}), 200

@courses_bp.route('/user-courses', methods=['GET'])
@require_auth
@handle_errors
def get_user_courses():
    """Get user's enrolled courses and progress"""
    user_id = request.user_id
    result = course_service.get_user_courses(user_id)
    return jsonify({'courses': result}), 200

@courses_bp.route('/<course_id>/progress', methods=['POST'])
@require_auth
@handle_errors
def update_course_progress(course_id):
    """Update user's progress in a course"""
    user_id = request.user_id
    data = request.get_json()
    
    module_id = data.get('module_id')
    
    if not module_id:
        return jsonify({'error': 'Module ID is required'}), 400
    
    result = course_service.update_course_progress(user_id, course_id, module_id)
    return jsonify({'progress': result}), 200

@courses_bp.route('/<course_id>/certificate', methods=['GET'])
@require_auth
@handle_errors
def get_course_certificate(course_id):
    """Get course certificate for completed course"""
    user_id = request.user_id
    result = course_service.get_course_certificate(user_id, course_id)
    return jsonify({'certificate': result}), 200

@courses_bp.route('/recommendations', methods=['GET'])
@require_auth
@handle_errors
def get_learning_recommendations():
    """Get personalized course recommendations"""
    user_id = request.user_id
    
    # Get user's financial profile for personalization
    profile_response, status = financial_service.get_financial_profile(user_id)
    profile = profile_response.get('profile', {}) if status == 200 else {}
    
    result = course_service.get_learning_recommendations(user_id, profile)
    return jsonify({'recommendations': result}), 200
