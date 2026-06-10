"""
Chat Routes
"""
from flask import Blueprint, request, jsonify
from services.chat_service import send_message, get_conversation_history, clear_conversation
from middleware.auth import authenticate_request
from utils.logger import logger

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/send', methods=['POST'])
@chat_bp.route('/message', methods=['POST'])  # Alternative endpoint for compatibility
@authenticate_request
def send():
    """Send a chat message"""
    try:
        user_id = request.user['userId']
        data = request.get_json()
        message = data.get('message')
        
        if not message:
            return jsonify({
                'error': {
                    'code': 'VALIDATION_ERROR',
                    'message': 'Message is required',
                    'timestamp': logger.get_timestamp()
                }
            }), 400
        
        if len(message) > 1000:
            return jsonify({
                'error': {
                    'code': 'VALIDATION_ERROR',
                    'message': 'Message too long (max 1000 characters)',
                    'timestamp': logger.get_timestamp()
                }
            }), 400
        
        result = send_message(user_id, message)
        return jsonify(result), 200
    except Exception as e:
        logger.error('Error in send endpoint', e)
        raise e

@chat_bp.route('/history', methods=['GET'])
@authenticate_request
def history():
    """Get conversation history"""
    try:
        user_id = request.user['userId']
        limit = request.args.get('limit', 50, type=int)
        
        messages = get_conversation_history(user_id, limit)
        return jsonify({'messages': messages}), 200
    except Exception as e:
        logger.error('Error in history endpoint', e)
        raise e

@chat_bp.route('/clear', methods=['DELETE'])
@authenticate_request
def clear():
    """Clear conversation history"""
    try:
        user_id = request.user['userId']
        count = clear_conversation(user_id)
        return jsonify({
            'success': True,
            'deletedCount': count
        }), 200
    except Exception as e:
        logger.error('Error in clear endpoint', e)
        raise e
