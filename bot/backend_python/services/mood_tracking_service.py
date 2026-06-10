"""
Mood Tracking Service
"""
from datetime import datetime, timedelta
from models.mood_entry import MoodEntry
from utils.logger import logger

def save_mood(user_id, mood_data):
    """Save mood entry"""
    try:
        mood = mood_data.get('mood')
        note = mood_data.get('note')
        date = mood_data.get('date')
        
        if isinstance(date, str):
            date = datetime.fromisoformat(date.replace('Z', '+00:00'))
        elif date is None:
            date = datetime.utcnow()
        
        mood_entry = MoodEntry.create(user_id, mood, note, date)
        logger.info(f'Mood saved for user {user_id}: {mood}')
        
        return {
            '_id': str(mood_entry['_id']),
            'userId': str(mood_entry['userId']),
            'mood': mood_entry['mood'],
            'note': mood_entry.get('note'),
            'date': mood_entry['date'].isoformat() + 'Z',
            'createdAt': mood_entry['createdAt'].isoformat() + 'Z'
        }
    except Exception as e:
        logger.error('Error saving mood', e)
        raise e

def get_mood_entries(user_id, limit=100):
    """Get mood entries for a user"""
    try:
        entries = MoodEntry.find_by_user(user_id, limit)
        
        result = []
        for entry in entries:
            result.append({
                '_id': str(entry['_id']),
                'userId': str(entry['userId']),
                'mood': entry['mood'],
                'note': entry.get('note'),
                'date': entry['date'].isoformat() + 'Z',
                'createdAt': entry['createdAt'].isoformat() + 'Z'
            })
        
        return result
    except Exception as e:
        logger.error('Error getting mood entries', e)
        return []

def get_mood_entries_by_date_range(user_id, start_date, end_date):
    """Get mood entries within a date range"""
    try:
        entries = MoodEntry.find_by_date_range(user_id, start_date, end_date)
        
        result = []
        for entry in entries:
            result.append({
                '_id': str(entry['_id']),
                'userId': str(entry['userId']),
                'mood': entry['mood'],
                'note': entry.get('note'),
                'date': entry['date'].isoformat() + 'Z',
                'createdAt': entry['createdAt'].isoformat() + 'Z'
            })
        
        return result
    except Exception as e:
        logger.error('Error getting mood entries by date range', e)
        return []

def get_mood_stats(user_id):
    """Calculate mood statistics"""
    try:
        entries = get_mood_entries(user_id, 365)
        
        if not entries:
            return {
                'streak': 0,
                'total': 0,
                'commonMood': '-',
                'weekMood': '-'
            }
        
        # Total entries
        total = len(entries)
        
        # Calculate streak
        streak = calculate_streak(entries)
        
        # Most common mood
        common_mood = get_most_common_mood(entries)
        
        # This week's mood
        week_ago = datetime.utcnow() - timedelta(days=7)
        week_entries = [e for e in entries if datetime.fromisoformat(e['date'].replace('Z', '+00:00')) >= week_ago]
        week_mood = get_most_common_mood(week_entries)
        
        return {
            'streak': streak,
            'total': total,
            'commonMood': common_mood,
            'weekMood': week_mood
        }
    except Exception as e:
        logger.error('Error calculating mood stats', e)
        return {
            'streak': 0,
            'total': 0,
            'commonMood': '-',
            'weekMood': '-'
        }

def calculate_streak(entries):
    """Calculate current streak"""
    if not entries:
        return 0
    
    # Sort by date descending
    sorted_entries = sorted(entries, key=lambda x: datetime.fromisoformat(x['date'].replace('Z', '+00:00')), reverse=True)
    
    streak = 0
    today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    
    for i, entry in enumerate(sorted_entries):
        entry_date = datetime.fromisoformat(entry['date'].replace('Z', '+00:00')).replace(hour=0, minute=0, second=0, microsecond=0)
        expected_date = today - timedelta(days=i)
        
        if entry_date == expected_date:
            streak += 1
        else:
            break
    
    return streak

def get_most_common_mood(entries):
    """Get most common mood"""
    if not entries:
        return '-'
    
    mood_counts = {}
    for entry in entries:
        mood = entry['mood']
        mood_counts[mood] = mood_counts.get(mood, 0) + 1
    
    most_common = max(mood_counts, key=mood_counts.get)
    
    mood_emojis = {
        'amazing': '😄',
        'good': '😊',
        'okay': '😐',
        'sad': '😔',
        'anxious': '😰'
    }
    
    return mood_emojis.get(most_common, most_common)

def delete_mood_entry(user_id, entry_id):
    """Delete a mood entry"""
    try:
        success = MoodEntry.delete_entry(user_id, entry_id)
        return success
    except Exception as e:
        logger.error('Error deleting mood entry', e)
        return False
