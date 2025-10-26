from flask import Blueprint, request, jsonify
from core.utils.security import rate_limit
from core.utils.error_handler import handle_errors
from core.utils.decorators import require_auth
from services.auth_service import AuthService


auth_bp = Blueprint('auth', __name__)
auth_service = AuthService()


@auth_bp.route('/register', methods=['POST'])
@rate_limit(max_requests=5, window=3600)
@handle_errors
def register():
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password are required'}), 400

    if len(data['password']) < 8:
        return jsonify({'error': 'Password must be at least 8 characters'}), 400

    result = auth_service.register_user(
        email=data['email'],
        password=data['password'],
        full_name=data.get('full_name', '')
    )

    if result['success']:
        return jsonify({'message': 'User registered successfully', 'user_id': result['user_id']}), 201
    return jsonify({'error': result['error']}), 400


@auth_bp.route('/login', methods=['POST'])
@rate_limit(max_requests=10, window=3600)
@handle_errors
def login():
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password are required'}), 400

    result = auth_service.login_user(data['email'], data['password'])
    if result['success']:
        # token is created in app-level login previously; blueprint will return user and expect caller to wrap with JWT
        return jsonify({'message': 'Login successful', 'user': result['user'], 'user_id': result['user_id']}), 200
    return jsonify({'error': result['error']}), 401


@auth_bp.route('/logout', methods=['POST'])
@require_auth
def logout():
    return jsonify({'message': 'Logout successful'}), 200


@auth_bp.route('/me', methods=['GET'])
@require_auth
def me():
    from services.auth_service import AuthService
    auth_service_local = AuthService()
    user = auth_service_local.get_user_by_id(request.user_id)
    if user:
        return jsonify({'user': user}), 200
    return jsonify({'error': 'User not found'}), 404


