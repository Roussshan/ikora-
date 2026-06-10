"""
User Model
"""
from datetime import datetime
from bson import ObjectId
from config.mongodb import get_db

class User:
    collection_name = 'users'
    
    @staticmethod
    def create(username, password_hash, email=None, full_name=None):
        """Create a new user"""
        db = get_db()
        if db is None:
            raise Exception('Database not connected')
        
        user_data = {
            'username': username.lower(),
            'password': password_hash,
            'createdAt': datetime.utcnow(),
            'updatedAt': datetime.utcnow(),
            'lastLogin': datetime.utcnow()
        }
        
        if email:
            user_data['email'] = email.lower()
        if full_name:
            user_data['fullName'] = full_name
        
        result = db[User.collection_name].insert_one(user_data)
        user_data['_id'] = result.inserted_id
        return user_data
    
    @staticmethod
    def find_by_username(username):
        """Find user by username"""
        db = get_db()
        if db is None:
            return None
        
        return db[User.collection_name].find_one({'username': username.lower()})
    
    @staticmethod
    def find_by_email(email):
        """Find user by email"""
        db = get_db()
        if db is None:
            return None
        
        return db[User.collection_name].find_one({'email': email.lower()})
    
    @staticmethod
    def find_by_id(user_id):
        """Find user by ID"""
        db = get_db()
        if db is None:
            return None
        
        try:
            return db[User.collection_name].find_one({'_id': ObjectId(user_id)})
        except:
            return None
    
    @staticmethod
    def update_last_login(user_id):
        """Update user's last login timestamp"""
        db = get_db()
        if db is None:
            return False
        
        try:
            db[User.collection_name].update_one(
                {'_id': ObjectId(user_id)},
                {'$set': {'lastLogin': datetime.utcnow(), 'updatedAt': datetime.utcnow()}}
            )
            return True
        except:
            return False
