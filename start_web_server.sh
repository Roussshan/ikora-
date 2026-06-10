#!/bin/bash
echo "========================================"
echo "   IKORA - Starting Web Server"
echo "========================================"
echo

# Check Python
if ! command -v python3 &>/dev/null; then
    echo "ERROR: Python 3 is not installed!"
    echo "Install it with: sudo apt install python3"
    exit 1
fi

echo "Starting web server on port 8080..."
echo
echo "Your website will be available at:"
echo "  http://localhost:8080"
echo
echo "Press Ctrl+C to stop the server"
echo "========================================"
echo

# Serve from the project root (where index.html / about.html etc. live)
cd "$(dirname "$0")" || exit 1
python3 -m http.server 8080
