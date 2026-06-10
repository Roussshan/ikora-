"""
Error Handler Middleware
"""
from flask import jsonify
from utils.logger import logger
import os

def register_error_handlers(app):
    """Register error handlers for the Flask app"""
    
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'error': {
                'code': 'BAD_REQUEST',
                'message': str(error),
                'timestamp': logger.get_timestamp()
            }
        }), 400
    
    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            'error': {
                'code': 'UNAUTHORIZED',
                'message': 'Authentication required',
                'timestamp': logger.get_timestamp()
            }
        }), 401
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'error': {
                'code': 'NOT_FOUND',
                'message': 'Resource not found',
                'timestamp': logger.get_timestamp()
            }
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        logger.error('Internal server error', error)
        return jsonify({
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': 'Internal server error',
                'details': str(error) if os.getenv('FLASK_ENV') == 'development' else None,
                'timestamp': logger.get_timestamp()
            }
        }), 500
    
    @app.errorhandler(Exception)
    def handle_exception(error):
        logger.error('Unhandled exception', error)
        return jsonify({
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': str(error),
                'timestamp': logger.get_timestamp()
            }
        }), 500
