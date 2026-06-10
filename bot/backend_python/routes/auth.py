"""
Authentication Routes
"""
from flask import Blueprint, request, jsonify
from services.auth_service import register, login
from middleware.auth import authenticate_request
from utils.logger import logger

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register_user():
    """Register a new user"""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        
        if not username or not password:
            return jsonify({
                'error': {
                    'code': 'VALIDATION_ERROR',
                    'message': 'Username and password are required',
                    'timestamp': logger.get_timestamp()
                }
            }), 400
        
        if len(username) < 3:
            return jsonify({
                'error': {
                    'code': 'VALIDATION_ERROR',
                    'message': 'Username must be at least 3 characters',
                    'timestamp': logger.get_timestamp()
                }
            }), 400
        
        result = register(username, password, email)
        return jsonify(result), 201
    except Exception as e:
        if str(e) == 'Username already exists' or str(e) == 'Email already exists':
            return jsonify({
                'error': {
                    'code': 'USER_EXISTS',
                    'message': str(e),
                    'timestamp': logger.get_timestamp()
                }
            }), 409
        raise e

@auth_bp.route('/login', methods=['POST'])
def login_user():
    """Login user"""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({
                'error': {
                    'code': 'VALIDATION_ERROR',
                    'message': 'Username and password are required',
                    'timestamp': logger.get_timestamp()
                }
            }), 400
        
        result = login(username, password)
        return jsonify(result), 200
    except Exception as e:
        if str(e) == 'Invalid credentials':
            return jsonify({
                'error': {
                    'code': 'AUTH_INVALID_CREDENTIALS',
                    'message': 'Invalid username or password',
                    'timestamp': logger.get_timestamp()
                }
            }), 401
        raise e

@auth_bp.route('/validate', methods=['GET'])
@authenticate_request
def validate():
    """Validate token"""
    return jsonify({
        'valid': True,
        'user': request.user
    }), 200

@auth_bp.route('/logout', methods=['POST'])
@authenticate_request
def logout():
    """Logout user"""
    return jsonify({'success': True}), 200
