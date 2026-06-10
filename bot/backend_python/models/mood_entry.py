"""
Mood Entry Model
"""
from datetime import datetime
from bson import ObjectId
from config.mongodb import get_db

class MoodEntry:
    collection_name = 'moodentries'
    
    @staticmethod
    def create(user_id, mood, note=None, date=None):
        """Create a new mood entry"""
        db = get_db()
        if db is None:
            raise Exception('Database not connected')
        
        mood_data = {
            'userId': ObjectId(user_id),
            'mood': mood,
            'date': date or datetime.utcnow(),
            'createdAt': datetime.utcnow()
        }
        
        if note:
            mood_data['note'] = note
        
        result = db[MoodEntry.collection_name].insert_one(mood_data)
        mood_data['_id'] = result.inserted_id
        return mood_data
    
    @staticmethod
    def find_by_user(user_id, limit=100):
        """Find mood entries by user ID"""
        db = get_db()
        if db is None:
            return []
        
        try:
            entries = list(db[MoodEntry.collection_name].find(
                {'userId': ObjectId(user_id)}
            ).sort('date', -1).limit(limit))
            return entries
        except:
            return []
    
    @staticmethod
    def find_by_date_range(user_id, start_date, end_date):
        """Find mood entries within a date range"""
        db = get_db()
        if db is None:
            return []
        
        try:
            entries = list(db[MoodEntry.collection_name].find({
                'userId': ObjectId(user_id),
                'date': {'$gte': start_date, '$lte': end_date}
            }).sort('date', -1))
            return entries
        except:
            return []
    
    @staticmethod
    def delete_entry(user_id, entry_id):
        """Delete a mood entry"""
        db = get_db()
        if db is None:
            raise Exception('Database not connected')
        
        try:
            result = db[MoodEntry.collection_name].delete_one({
                '_id': ObjectId(entry_id),
                'userId': ObjectId(user_id)
            })
            return result.deleted_count > 0
        except:
            return False
