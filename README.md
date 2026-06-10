# 🔥 IKORA — AI Wellness Chatbot

> A mental wellness companion powered by Bhagavad Gita wisdom and Google Gemini AI.

**Live Demo:** [ikora.netlify.app](https://ikora.netlify.app) &nbsp;|&nbsp; **API:** [ikora-backend.onrender.com](https://ikora-backend.onrender.com/health)

---

## Features

- 💬 **AI Chat** — Empathetic responses using Google Gemini + curated Gita knowledge base
- 🧠 **Emotion Detection** — Automatically detects user's emotional state (sad, anxious, depressed, etc.)
- 📚 **Gita Library** — Browse Bhagavad Gita teachings by chapter
- 📊 **Mood Tracker** — Log and visualize your daily mood over time
- 🧘 **Guided Exercises** — Breathing and mindfulness exercises
- 🔐 **Auth** — JWT-based user accounts with bcrypt password hashing

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | HTML5, CSS3, Vanilla JS |
| Backend | Python 3, Flask, Flask-CORS |
| Database | MongoDB (Atlas in production) |
| AI | Google Gemini 2.5 Flash API |
| Auth | JWT + bcrypt |
| Deploy | Netlify (frontend) + Render (backend) |

## Architecture

```
Browser (Netlify)
    │
    ▼  REST API (HTTPS)
Flask Backend (Render)
    │
    ├── Emotion Detection (keyword + phrase analysis)
    ├── Knowledge Base Search (MongoDB text search)
    └── Gemini AI (fallback + general messages)
    │
    ▼
MongoDB Atlas
```

## Local Development

```bash
# 1. Clone the repo
git clone https://github.com/your-username/ikora.git
cd ikora

# 2. Set up backend
cd bot/backend_python
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env — add your GEMINI_API_KEY and MONGODB_URI

# 3. Import knowledge base
python3 import_knowledge_base.py

# 4. Run backend (terminal 1)
python3 app.py

# 5. Run frontend (terminal 2)
cd ../..
python3 -m http.server 8080
# Open http://localhost:8080
```

## Environment Variables

| Variable | Description |
|---|---|
| `MONGODB_URI` | MongoDB connection string |
| `JWT_SECRET` | Secret key for JWT signing |
| `GEMINI_API_KEY` | Google Gemini API key |
| `PORT` | Server port (default 3000) |
| `FLASK_ENV` | `development` or `production` |

## License

MIT
