#!/bin/bash
echo "========================================"
echo "   IKORA - Starting Python Backend"
echo "========================================"
echo

BACKEND_DIR="$(cd "$(dirname "$0")/bot/backend_python" && pwd)"
VENV_PYTHON="$BACKEND_DIR/venv/bin/python3"
VENV_PIP="$BACKEND_DIR/venv/bin/pip"

# Check Python
if ! command -v python3 &>/dev/null; then
    echo "ERROR: Python 3 is not installed!"
    echo "Install it with: sudo apt install python3 python3-venv"
    exit 1
fi

echo "Python found: $(python3 --version)"
echo

cd "$BACKEND_DIR" || exit 1

# Create venv if it doesn't exist
if [ ! -f "$VENV_PYTHON" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv || {
        echo "ERROR: python3-venv not installed."
        echo "Run: sudo apt install python3-venv python3-full"
        exit 1
    }
fi

# Install dependencies if flask is missing
if ! "$VENV_PYTHON" -c "import flask" &>/dev/null; then
    echo "Installing dependencies..."
    "$VENV_PIP" install -r requirements.txt
    echo
fi

# Create .env from example if missing
if [ ! -f ".env" ]; then
    echo "Creating .env file from example..."
    cp .env.example .env
    echo "⚠️  Please edit .env and add your API keys!"
    echo
fi

echo "Starting Python Backend Server..."
echo "Server will run on: http://localhost:3000"
echo
echo "Press Ctrl+C to stop the server"
echo "========================================"
echo

"$VENV_PYTHON" app.py
