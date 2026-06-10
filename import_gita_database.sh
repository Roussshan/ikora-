#!/bin/bash
echo "========================================"
echo "   IKORA - Import Bhagavad Gita Database"
echo "========================================"
echo

BACKEND_DIR="$(cd "$(dirname "$0")/bot/backend_python" && pwd)"
VENV_PYTHON="$BACKEND_DIR/venv/bin/python3"

# Check Python
if ! command -v python3 &>/dev/null; then
    echo "ERROR: Python 3 is not installed!"
    exit 1
fi

# Check venv
if [ ! -f "$VENV_PYTHON" ]; then
    echo "⚠️  Virtual environment not found. Run ./setup_linux.sh first."
    exit 1
fi

echo "This will import 692 Bhagavad Gita verses into MongoDB"
echo
echo "Make sure MongoDB is running!"
echo
read -rp "Press Enter to continue (Ctrl+C to cancel)..."

echo
echo "Starting import..."
echo

cd "$BACKEND_DIR" || exit 1
"$VENV_PYTHON" import_knowledge_base.py

echo
echo "========================================"
echo "   Import Complete!"
echo "========================================"
echo
echo "Your chatbot can now answer questions"
echo "using the Bhagavad Gita wisdom!"
echo
