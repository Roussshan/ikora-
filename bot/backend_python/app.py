"""
IKORA Backend - Main Application
Python/Flask implementation
"""
import os
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from config.mongodb import connect_mongodb
from routes.auth import auth_bp
from routes.chat import chat_bp
from routes.mood import mood_bp
from middleware.error_handler import register_error_handlers
from utils.logger import logger

# Load environment variables
load_dotenv()

# Create Flask app
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.getenv('JWT_SECRET', 'your-secret-key')
app.config['JSON_SORT_KEYS'] = False

# CORS Configuration
# In production set FRONTEND_URL env var to your Netlify URL
FRONTEND_URL = os.getenv('FRONTEND_URL', '*')
CORS(app, resources={
    r"/*": {
        "origins": "*",          # keep wildcard so Netlify preview URLs also work
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": False,
        "expose_headers": ["Content-Type", "Authorization"]
    }
})

# Connect to MongoDB
try:
    connect_mongodb()
except Exception as e:
    logger.error(f'Failed to connect to MongoDB: {e}')
    logger.warning('Server will continue with fallback responses')

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(chat_bp, url_prefix='/api/chat')
app.register_blueprint(mood_bp, url_prefix='/api/mood')

# Register error handlers
register_error_handlers(app)

# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    from config.mongodb import get_db
    db = get_db()
    return jsonify({
        'status': 'ok',
        'database': 'connected' if db is not None else 'disconnected',
        'timestamp': logger.get_timestamp()
    })

# Debug endpoint — shows env config (no secrets)
@app.route('/debug', methods=['GET'])
def debug():
    import os
    uri = os.getenv('MONGODB_URI', 'NOT SET')
    # Mask password in URI for safe display
    import re
    masked = re.sub(r'://([^:]+):([^@]+)@', r'://\1:***@', uri)
    return jsonify({
        'mongodb_uri_set': bool(uri and uri != 'NOT SET'),
        'mongodb_uri_masked': masked,
        'gemini_key_set': bool(os.getenv('GEMINI_API_KEY')),
        'jwt_secret_set': bool(os.getenv('JWT_SECRET')),
        'flask_env': os.getenv('FLASK_ENV', 'not set'),
        'port': os.getenv('PORT', 'not set'),
    })

# Root endpoint
@app.route('/', methods=['GET'])
def root():
    return jsonify({
        'message': 'IKORA Backend API',
        'version': '1.0.0',
        'status': 'running'
    })

if __name__ == '__main__':
    PORT = int(os.getenv('PORT', 3000))
    logger.info(f'🚀 Ikora backend server running on port {PORT}')
    logger.info(f'📊 MongoDB URI: {os.getenv("MONGODB_URI", "mongodb://localhost:27017/ikora")}')
    
    app.run(
        host='0.0.0.0',
        port=PORT,
        debug=os.getenv('FLASK_ENV') == 'development'
    )
