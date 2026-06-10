"""
Conversation Model
"""
from datetime import datetime
from bson import ObjectId
from config.mongodb import get_db

class Conversation:
    collection_name = 'conversations'
    
    @staticmethod
    def create(user_id, message, sender, emotion=None):
        """Create a new conversation entry"""
        db = get_db()
        if db is None:
            raise Exception('Database not connected')
        
        conversation_data = {
            'userId': ObjectId(user_id),
            'message': message,
            'sender': sender,
            'createdAt': datetime.utcnow()
        }
        
        if emotion:
            conversation_data['emotion'] = {
                'dominant': emotion['dominant'],
                'scores': emotion['scores'],
                'confidence': emotion['confidence']
            }
        
        result = db[Conversation.collection_name].insert_one(conversation_data)
        conversation_data['_id'] = result.inserted_id
        return conversation_data
    
    @staticmethod
    def find_by_user(user_id, limit=50):
        """Find conversations by user ID"""
        db = get_db()
        if db is None:
            return []
        
        try:
            conversations = list(db[Conversation.collection_name].find(
                {'userId': ObjectId(user_id)}
            ).sort('createdAt', -1).limit(limit))
            
            # Reverse to get chronological order
            conversations.reverse()
            return conversations
        except:
            return []
    
    @staticmethod
    def delete_by_user(user_id):
        """Delete all conversations for a user"""
        db = get_db()
        if db is None:
            raise Exception('Database not connected')
        
        try:
            result = db[Conversation.collection_name].delete_many({'userId': ObjectId(user_id)})
            return result.deleted_count
        except:
            return 0
