"""
MongoDB Configuration
"""
import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from utils.logger import logger

# MongoDB client instance
mongo_client = None
db = None

MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/ikora')

def connect_mongodb():
    """Connect to MongoDB"""
    global mongo_client, db
    
    try:
        # Use longer timeout for Atlas on cloud hosting (Render cold starts)
        mongo_client = MongoClient(
            MONGODB_URI,
            serverSelectionTimeoutMS=10000,
            connectTimeoutMS=10000,
            socketTimeoutMS=10000,
            tls=True if 'mongodb+srv' in MONGODB_URI else False,
        )
        # Test connection
        mongo_client.admin.command('ping')
        
        # Get database name from URI or use default
        db_name = 'ikora'
        if '/' in MONGODB_URI.split('?')[0]:
            db_name = MONGODB_URI.split('/')[-1].split('?')[0] or 'ikora'
        
        db = mongo_client[db_name]
        
        logger.info('✅ Connected to MongoDB successfully')
        logger.info(f'📊 Database: {db_name}')
        
        # Create indexes
        create_indexes()
        
        return db
    except ConnectionFailure as e:
        logger.error(f'❌ MongoDB connection error: {e}')
        logger.warning('⚠️  Chatbot will use fallback responses without MongoDB')
        return None
    except Exception as e:
        logger.error(f'❌ Unexpected error connecting to MongoDB: {e}')
        return None

def create_indexes():
    """Create database indexes for better performance"""
    try:
        if db is None:
            return
        
        # Users collection indexes
        db.users.create_index('username', unique=True)
        db.users.create_index('email', unique=True, sparse=True)
        
        # Conversations collection indexes
        db.conversations.create_index([('userId', 1), ('createdAt', -1)])
        
        # MoodEntries collection indexes
        db.moodentries.create_index([('userId', 1), ('date', -1)])
        db.moodentries.create_index([('userId', 1), ('mood', 1)])
        
        # KnowledgeBase collection indexes
        db.knowledgebases.create_index([('question', 'text'), ('answer', 'text'), ('keywords', 'text'), ('tags', 'text')])
        db.knowledgebases.create_index([('emotion', 1), ('priority', -1)])
        db.knowledgebases.create_index([('category', 1), ('priority', -1)])
        
        logger.info('✅ Database indexes created')
    except Exception as e:
        logger.warning(f'Could not create indexes: {e}')

def get_db():
    """Get database instance"""
    return db

def disconnect_mongodb():
    """Disconnect from MongoDB"""
    global mongo_client
    if mongo_client:
        mongo_client.close()
        logger.info('Disconnected from MongoDB')
