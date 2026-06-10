#!/bin/bash
echo "========================================"
echo "   IKORA - Complete System Startup"
echo "========================================"
echo

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
BACKEND_DIR="$PROJECT_DIR/bot/backend_python"
VENV_PYTHON="$BACKEND_DIR/venv/bin/python3"

# Check Python
if ! command -v python3 &>/dev/null; then
    echo "ERROR: Python 3 is not installed!"
    echo "Install it with: sudo apt install python3 python3-venv"
    exit 1
fi

# Check venv exists
if [ ! -f "$VENV_PYTHON" ]; then
    echo "⚠️  Virtual environment not found."
    echo "    Run ./setup_linux.sh first to set everything up."
    exit 1
fi

# Step 1: Start MongoDB
echo "Step 1: Starting MongoDB..."
if command -v systemctl &>/dev/null; then
    sudo systemctl start mongod 2>/dev/null && echo "✅ MongoDB started via systemctl" \
        || echo "⚠️  Could not start MongoDB via systemctl (may already be running)"
else
    sudo service mongod start 2>/dev/null && echo "✅ MongoDB started via service" \
        || echo "⚠️  Could not start MongoDB (may already be running)"
fi
echo

# Step 2: Start Python Backend in a new terminal
echo "Step 2: Starting Python Backend (Port 3000)..."
BACKEND_CMD="cd '$BACKEND_DIR' && '$VENV_PYTHON' app.py; read -rp 'Press Enter to close...'"
if command -v gnome-terminal &>/dev/null; then
    gnome-terminal --title="IKORA Backend" -- bash -c "$BACKEND_CMD" &
elif command -v xterm &>/dev/null; then
    xterm -title "IKORA Backend" -e "bash -c \"$BACKEND_CMD\"" &
else
    # Fallback: background process with log file
    cd "$BACKEND_DIR" && "$VENV_PYTHON" app.py > "$PROJECT_DIR/backend.log" 2>&1 &
    echo "  (running in background — logs: $PROJECT_DIR/backend.log)"
fi
echo "✅ Backend starting..."
sleep 3
echo

# Step 3: Start Web Server in a new terminal
echo "Step 3: Starting Web Server (Port 8080)..."
WEB_CMD="cd '$PROJECT_DIR' && python3 -m http.server 8080; read -rp 'Press Enter to close...'"
if command -v gnome-terminal &>/dev/null; then
    gnome-terminal --title="IKORA Web Server" -- bash -c "$WEB_CMD" &
elif command -v xterm &>/dev/null; then
    xterm -title "IKORA Web Server" -e "bash -c \"$WEB_CMD\"" &
else
    cd "$PROJECT_DIR" && python3 -m http.server 8080 > "$PROJECT_DIR/webserver.log" 2>&1 &
    echo "  (running in background — logs: $PROJECT_DIR/webserver.log)"
fi
echo "✅ Web server starting..."
sleep 2
echo

# Step 4: Open browser
echo "Step 4: Opening website..."
if command -v xdg-open &>/dev/null; then
    xdg-open http://localhost:8080
elif command -v sensible-browser &>/dev/null; then
    sensible-browser http://localhost:8080
else
    echo "  Open manually: http://localhost:8080"
fi
echo "✅ Website launched"
echo

echo "========================================"
echo "   IKORA is Running!"
echo "========================================"
echo
echo "Backend API:  http://localhost:3000"
echo "Website:      http://localhost:8080"
echo
echo "IMPORTANT:"
echo "  - Use http://localhost:8080 (NOT file://)"
echo "  - Clear browser cache if needed: Ctrl+Shift+R"
echo "  - To stop: close the Backend and Web Server terminals"
echo
echo "Logs (if running in background):"
echo "  Backend:    $PROJECT_DIR/backend.log"
echo "  Web server: $PROJECT_DIR/webserver.log"
echo
