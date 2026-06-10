#!/bin/bash
# ============================================================
#   IKORA - First-time Linux Setup Script
#   Run this once to prepare your environment
# ============================================================

set -e  # exit on first error

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
BACKEND_DIR="$PROJECT_DIR/bot/backend_python"

echo "========================================"
echo "   IKORA - Linux Setup"
echo "========================================"
echo

# ----------------------------------------------------------
# 1. Check Python 3
# ----------------------------------------------------------
echo "[1/5] Checking Python 3..."
if ! command -v python3 &>/dev/null; then
    echo "  Python 3 not found. Installing..."
    sudo apt update && sudo apt install -y python3 python3-pip python3-venv
else
    echo "  ✅ $(python3 --version)"
fi

# ----------------------------------------------------------
# 2. Check / install MongoDB
# ----------------------------------------------------------
echo
echo "[2/5] Checking MongoDB..."
if ! command -v mongod &>/dev/null; then
    echo "  MongoDB not found. Installing..."
    sudo apt update
    sudo apt install -y gnupg curl
    # Add MongoDB 7.0 repo (Ubuntu 22.04+)
    curl -fsSL https://www.mongodb.org/static/pgp/server-7.0.asc | \
        sudo gpg -o /usr/share/keyrings/mongodb-server-7.0.gpg --dearmor
    echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] \
https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | \
        sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list
    sudo apt update && sudo apt install -y mongodb-org
    sudo systemctl enable mongod
    sudo systemctl start mongod
    echo "  ✅ MongoDB installed and started"
else
    echo "  ✅ MongoDB found: $(mongod --version | head -1)"
    # Make sure it's running
    sudo systemctl start mongod 2>/dev/null || sudo service mongod start 2>/dev/null || true
fi

# ----------------------------------------------------------
# 3. Install Python dependencies (in a venv)
# ----------------------------------------------------------
echo
echo "[3/5] Installing Python dependencies..."
cd "$BACKEND_DIR"

# Ensure python3-venv is available
if ! python3 -m venv --help &>/dev/null; then
    echo "  Installing python3-venv..."
    sudo apt install -y python3-venv python3-full
fi

# Remove old Windows venv if it exists (has Scripts/ instead of bin/)
if [ -d "$PROJECT_DIR/.venv/Scripts" ]; then
    echo "  Removing old Windows .venv..."
    rm -rf "$PROJECT_DIR/.venv"
fi

# Create fresh Linux venv inside backend dir
if [ ! -f "$BACKEND_DIR/venv/bin/activate" ]; then
    echo "  Creating virtual environment..."
    python3 -m venv "$BACKEND_DIR/venv"
fi

echo "  Installing packages into venv..."
"$BACKEND_DIR/venv/bin/pip" install -r requirements.txt
echo "  ✅ Dependencies installed in venv"

# ----------------------------------------------------------
# 4. Create .env if missing
# ----------------------------------------------------------
echo
echo "[4/5] Setting up .env..."
if [ ! -f "$BACKEND_DIR/.env" ]; then
    cp "$BACKEND_DIR/.env.example" "$BACKEND_DIR/.env"
    echo "  ✅ .env created from .env.example"
    echo
    echo "  ⚠️  IMPORTANT: Open bot/backend_python/.env and fill in your API keys:"
    echo "     - OPENAI_API_KEY  or  GEMINI_API_KEY"
    echo "     - JWT_SECRET (change to a random string)"
else
    echo "  ✅ .env already exists"
fi

# ----------------------------------------------------------
# 5. Make all shell scripts executable
# ----------------------------------------------------------
echo
echo "[5/5] Making shell scripts executable..."
chmod +x "$PROJECT_DIR"/*.sh
echo "  ✅ All .sh scripts are now executable"

# ----------------------------------------------------------
# Done
# ----------------------------------------------------------
echo
echo "========================================"
echo "   Setup Complete!"
echo "========================================"
echo
echo "Next steps:"
echo "  1. Edit bot/backend_python/.env — add your API key"
echo "  2. Run:  ./start_complete_system.sh"
echo "      OR run separately:"
echo "         ./start_backend.sh    (terminal 1)"
echo "         ./start_web_server.sh (terminal 2)"
echo
