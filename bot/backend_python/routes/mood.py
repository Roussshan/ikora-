"""
Mood Tracking Routes
"""
from flask import Blueprint, request, jsonify
from services.mood_tracking_service import save_mood, get_mood_entries, get_mood_stats
from middleware.auth import authenticate_request
from utils.logger import logger

mood_bp = Blueprint('mood', __name__)

@mood_bp.route('/save', methods=['POST'])
@authenticate_request
def save():
    """Save mood entry"""
    try:
        user_id = request.user['userId']
        data = request.get_json()
        mood = data.get('mood')
        note = data.get('note')
        date = data.get('date')
        
        if not mood:
            return jsonify({
                'error': {
                    'code': 'VALIDATION_ERROR',
                    'message': 'Mood is required',
                    'timestamp': logger.get_timestamp()
                }
            }), 400
        
        valid_moods = ['amazing', 'good', 'okay', 'sad', 'anxious']
        if mood not in valid_moods:
            return jsonify({
                'error': {
                    'code': 'VALIDATION_ERROR',
                    'message': 'Invalid mood value',
                    'timestamp': logger.get_timestamp()
                }
            }), 400
        
        mood_entry = save_mood(user_id, {
            'mood': mood,
            'note': note,
            'date': date
        })
        
        return jsonify({
            'success': True,
            'entry': mood_entry
        }), 201
    except Exception as e:
        logger.error('Error in save mood endpoint', e)
        raise e

@mood_bp.route('/history', methods=['GET'])
@authenticate_request
def history():
    """Get mood history"""
    try:
        user_id = request.user['userId']
        limit = request.args.get('limit', 100, type=int)
        
        entries = get_mood_entries(user_id, limit)
        return jsonify({
            'success': True,
            'data': entries
        }), 200
    except Exception as e:
        logger.error('Error in mood history endpoint', e)
        raise e

@mood_bp.route('/statistics', methods=['GET'])
@authenticate_request
def statistics():
    """Get mood statistics"""
    try:
        user_id = request.user['userId']
        stats = get_mood_stats(user_id)
        
        return jsonify({
            'success': True,
            'stats': stats
        }), 200
    except Exception as e:
        logger.error('Error in mood statistics endpoint', e)
        raise e
