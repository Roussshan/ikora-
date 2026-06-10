# IKORA Backend - Python Version

Complete Python/Flask implementation of the IKORA Mental Wellness Chatbot backend.

## Features

- ✅ User authentication (register, login, JWT tokens)
- ✅ Chat functionality with emotion detection
- ✅ MongoDB integration for data storage
- ✅ Mood tracking system
- ✅ Knowledge base search (692 Q&A entries)
- ✅ RESTful API endpoints
- ✅ Error handling and logging

## Requirements

- Python 3.8 or higher
- MongoDB (local or Atlas)
- pip (Python package manager)

## Installation

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

Or use virtual environment (recommended):

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Copy `.env.example` to `.env` and update the values:

```bash
cp .env.example .env
```

Edit `.env`:
```
PORT=3000
FLASK_ENV=development
JWT_SECRET=your-super-secret-jwt-key-change-this
JWT_EXPIRES_IN=1800
MONGODB_URI=mongodb://localhost:27017/ikora
```

### 3. Start MongoDB

Make sure MongoDB is running:

```bash
# Windows
net start MongoDB

# Or use the batch script
..\scripts\START_MONGODB.bat
```

### 4. Start the Backend

```bash
python app.py
```

Or use the batch script:

```bash
START_PYTHON_BACKEND.bat
```

## API Endpoints

### Authentication

- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/validate` - Validate token
- `POST /api/auth/logout` - Logout user

### Chat

- `POST /api/chat/send` - Send message
- `GET /api/chat/history` - Get conversation history
- `DELETE /api/chat/clear` - Clear conversation

### Mood Tracking

- `POST /api/mood/save` - Save mood entry
- `GET /api/mood/history` - Get mood history
- `GET /api/mood/statistics` - Get mood statistics

### Health Check

- `GET /health` - Server health check

## Project Structure

```
backend_python/
├── app.py                  # Main application
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── config/
│   └── mongodb.py         # MongoDB configuration
├── models/
│   ├── user.py           # User model
│   ├── conversation.py   # Conversation model
│   ├── mood_entry.py     # Mood entry model
│   └── knowledge_base.py # Knowledge base model
├── services/
│   ├── auth_service.py           # Authentication logic
│   ├── chat_service.py           # Chat logic
│   ├── emotion_service.py        # Emotion detection
│   ├── guidance_service.py       # Response generation
│   ├── knowledge_base_service.py # KB search
│   └── mood_tracking_service.py  # Mood tracking
├── routes/
│   ├── auth.py           # Auth endpoints
│   ├── chat.py           # Chat endpoints
│   └── mood.py           # Mood endpoints
├── middleware/
│   ├── auth.py           # JWT authentication
│   └── error_handler.py  # Error handling
└── utils/
    └── logger.py         # Logging utility
```

## Differences from TypeScript Version

### Similarities (100% Feature Parity)
- ✅ All API endpoints work identically
- ✅ Same database schema and collections
- ✅ Same authentication flow (JWT)
- ✅ Same emotion detection algorithm
- ✅ Same response generation logic
- ✅ Same error handling structure

### Technical Differences
- **Framework**: Flask instead of Express.js
- **Language**: Python instead of TypeScript
- **Database Driver**: PyMongo instead of Mongoose
- **Password Hashing**: bcrypt (Python) instead of bcrypt (Node.js)
- **JWT**: PyJWT instead of jsonwebtoken

### API Compatibility
The Python backend is 100% compatible with the existing frontend. No changes needed to HTML/JavaScript files.

## Testing

Test the backend:

```bash
# Health check
curl http://localhost:3000/health

# Register user
curl -X POST http://localhost:3000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"password123"}'

# Login
curl -X POST http://localhost:3000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"password123"}'
```

## Migration from TypeScript

To switch from TypeScript to Python backend:

1. Stop the TypeScript backend
2. Start the Python backend on the same port (3000)
3. No frontend changes needed
4. Uses the same MongoDB database

## Troubleshooting

### Port Already in Use
```bash
# Change PORT in .env file
PORT=3001
```

### MongoDB Connection Error
```bash
# Check if MongoDB is running
net start MongoDB

# Verify MONGODB_URI in .env
MONGODB_URI=mongodb://localhost:27017/ikora
```

### Module Not Found
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

## Production Deployment

For production:

1. Set `FLASK_ENV=production` in `.env`
2. Use a production WSGI server (gunicorn, waitress)
3. Set strong `JWT_SECRET`
4. Use MongoDB Atlas for cloud database
5. Enable HTTPS

Example with gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:3000 app:app
```

## License

MIT

## Support

For issues or questions, check the main project README or documentation.
