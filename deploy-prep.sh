#!/bin/bash
# Quick deployment preparation script for Linux/Mac
# This script prepares your project for Render deployment

set -e

echo "========================================"
echo "SQL Scanner - Render Deployment Prep"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python3 is not installed"
    echo "Please install Python 3.11+ first"
    exit 1
fi

echo "[1/6] Checking Python version..."
python3 --version

echo ""
echo "[2/6] Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

echo "[3/6] Activating virtual environment..."
source venv/bin/activate

echo "[4/6] Installing/updating dependencies..."
pip install -r requirements.txt

echo ""
echo "[5/6] Running tests..."
echo "Testing imports..."
python3 -c "import flask; import aiohttp; import bs4; print('✓ All imports successful')"

echo ""
echo "[6/6] Testing local server..."
echo "Starting Flask app on http://localhost:5050"
echo "Press Ctrl+C to stop the server when you're done testing"
echo ""

export FLASK_ENV=development
export START_URL=http://testphp.vulnweb.com

python3 dashboard.py &
SERVER_PID=$!

echo ""
echo "Server started with PID: $SERVER_PID"
echo "Waiting 3 seconds for server to start..."
sleep 3

echo "Testing health endpoint..."
curl -s http://localhost:5050/health | python3 -m json.tool || echo "Health check failed"

echo ""
echo "Press Enter to stop the server and continue..."
read

kill $SERVER_PID 2>/dev/null || true

echo ""
echo "========================================"
echo "Next Steps:"
echo "========================================"
echo "1. Push your code to GitHub:"
echo "   git init"
echo "   git add ."
echo "   git commit -m 'Initial commit'"
echo "   git remote add origin YOUR_GITHUB_URL"
echo "   git push -u origin main"
echo ""
echo "2. Deploy on Render:"
echo "   - Go to https://dashboard.render.com"
echo "   - Click 'New +' > 'Blueprint'"
echo "   - Connect your GitHub repository"
echo "   - Click 'Apply'"
echo ""
echo "3. Set environment variables in Render:"
echo "   PYTHON_VERSION=3.11.0"
echo "   FLASK_ENV=production"
echo "   START_URL=http://testphp.vulnweb.com"
echo ""
echo "See CHECKLIST.md for detailed instructions"
echo "========================================"
