"""
Authentication Middleware
"""
from functools import wraps
from flask import request, jsonify
from services.auth_service import validate_token
from utils.logger import logger

def authenticate_request(f):
    """Decorator to authenticate requests"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            auth_header = request.headers.get('Authorization')
            
            if not auth_header or not auth_header.startswith('Bearer '):
                return jsonify({
                    'error': {
                        'code': 'AUTH_MISSING_TOKEN',
                        'message': 'Authentication token required',
                        'timestamp': logger.get_timestamp()
                    }
                }), 401
            
            token = auth_header[7:]  # Remove 'Bearer ' prefix
            decoded = validate_token(token)
            
            # Add user info to request
            request.user = {
                'userId': decoded['userId'],
                'username': decoded['username']
            }
            
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({
                'error': {
                    'code': 'AUTH_INVALID_TOKEN',
                    'message': 'Invalid or expired token',
                    'timestamp': logger.get_timestamp()
                }
            }), 401
    
    return decorated_function
