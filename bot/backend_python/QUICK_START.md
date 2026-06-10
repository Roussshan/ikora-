# 🚀 Quick Start - Python Backend

## 3-Step Setup

### Step 1: Install Python
If you don't have Python installed:
1. Download from https://www.python.org/downloads/
2. Install Python 3.8 or higher
3. ✅ Check "Add Python to PATH" during installation

### Step 2: Start the Backend
```bash
cd bot/backend_python
START_PYTHON_BACKEND.bat
```

That's it! The script handles everything:
- Creates virtual environment
- Installs dependencies
- Configures environment
- Starts the server

### Step 3: Test It
Open your browser and go to:
```
http://localhost:3000/health
```

You should see:
```json
{
  "status": "ok",
  "timestamp": "2024-01-01T00:00:00.000Z"
}
```

## ✅ Done!

Your Python backend is running on port 3000.

Now open `index.html` in your browser and test the chatbot!

---

## Common Commands

### Start Backend
```bash
START_PYTHON_BACKEND.bat
```

### Stop Backend
Press `Ctrl+C` in the terminal

### Restart Backend
1. Stop with `Ctrl+C`
2. Run `START_PYTHON_BACKEND.bat` again

### View Logs
Logs appear in the terminal where you started the backend

---

## Configuration

Edit `bot/backend_python/.env` to change settings:

```env
PORT=3000                    # Server port
FLASK_ENV=development        # Environment
JWT_SECRET=your-secret-key   # JWT secret
JWT_EXPIRES_IN=1800          # Token expiry (seconds)
MONGODB_URI=mongodb://localhost:27017/ikora  # Database
```

---

## Troubleshooting

### "Python not found"
- Install Python from python.org
- Restart terminal
- Make sure PATH was set during installation

### "Port 3000 already in use"
- Stop the TypeScript backend first
- Or change PORT in `.env` file

### "MongoDB connection error"
- Start MongoDB: `net start MongoDB`
- Or run: `..\scripts\START_MONGODB.bat`

---

## Next Steps

1. ✅ Backend is running
2. Open `index.html` in browser
3. Register a new account
4. Start chatting with Ikora!

---

**Need help? Check `README.md` for detailed documentation.**
