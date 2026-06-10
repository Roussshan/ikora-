"""
Authentication Service
"""
import os
import bcrypt
import jwt
from datetime import datetime, timedelta
from models.user import User
from utils.logger import logger

SALT_ROUNDS = 12
JWT_SECRET = os.getenv('JWT_SECRET', 'your-secret-key')
JWT_EXPIRES_IN = int(os.getenv('JWT_EXPIRES_IN', 1800))  # seconds

def hash_password(password):
    """Hash a password"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(SALT_ROUNDS)).decode('utf-8')

def compare_password(password, password_hash):
    """Compare password with hash"""
    return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))

def generate_token(user_id, username):
    """Generate JWT token"""
    payload = {
        'userId': str(user_id),
        'username': username,
        'exp': datetime.utcnow() + timedelta(seconds=JWT_EXPIRES_IN),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, JWT_SECRET, algorithm='HS256')

def validate_token(token):
    """Validate JWT token"""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        raise Exception('Token has expired')
    except jwt.InvalidTokenError:
        raise Exception('Invalid token')

def register(username, password, email=None, full_name=None):
    """Register a new user"""
    try:
        # Check if user exists
        if email:
            existing_user = User.find_by_username(username) or User.find_by_email(email)
            if existing_user:
                if existing_user.get('username') == username.lower():
                    raise Exception('Username already exists')
                if existing_user.get('email') == email.lower():
                    raise Exception('Email already exists')
        else:
            existing_user = User.find_by_username(username)
            if existing_user:
                raise Exception('Username already exists')
        
        # Hash password
        password_hash = hash_password(password)
        
        # Create user
        user = User.create(username, password_hash, email, full_name)
        
        # Generate token
        token = generate_token(user['_id'], user['username'])
        
        logger.info(f'User registered: {username} (MongoDB)')
        
        return {
            'user': {
                'id': str(user['_id']),
                'username': user['username'],
                'email': user.get('email'),
                'fullName': user.get('fullName'),
                'createdAt': user['createdAt'].isoformat() + 'Z'
            },
            'token': token,
            'expiresIn': f'{JWT_EXPIRES_IN}s'
        }
    except Exception as e:
        logger.error('Registration error', e)
        raise e

def login(username, password):
    """Login user"""
    try:
        # Find user
        user = User.find_by_username(username)
        
        if not user:
            raise Exception('Invalid credentials')
        
        # Verify password
        if not compare_password(password, user['password']):
            raise Exception('Invalid credentials')
        
        # Update last login
        User.update_last_login(user['_id'])
        
        # Generate token
        token = generate_token(user['_id'], user['username'])
        
        logger.info(f'User logged in: {username} (MongoDB)')
        
        return {
            'user': {
                'id': str(user['_id']),
                'username': user['username'],
                'email': user.get('email'),
                'fullName': user.get('fullName'),
                'createdAt': user['createdAt'].isoformat() + 'Z',
                'lastLogin': datetime.utcnow().isoformat() + 'Z'
            },
            'token': token,
            'expiresIn': f'{JWT_EXPIRES_IN}s'
        }
    except Exception as e:
        logger.error('Login error', e)
        raise e

def get_user_by_id(user_id):
    """Get user by ID"""
    try:
        user = User.find_by_id(user_id)
        
        if not user:
            return None
        
        return {
            'id': str(user['_id']),
            'username': user['username'],
            'email': user.get('email'),
            'fullName': user.get('fullName'),
            'createdAt': user['createdAt'].isoformat() + 'Z',
            'lastLogin': user.get('lastLogin').isoformat() + 'Z' if user.get('lastLogin') else None
        }
    except Exception as e:
        logger.error('Get user error', e)
        return None
