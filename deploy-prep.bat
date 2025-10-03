@echo off
REM Quick deployment preparation script for Windows
REM This script prepares your project for Render deployment

echo ========================================
echo SQL Scanner - Render Deployment Prep
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.11+ first
    pause
    exit /b 1
)

echo [1/6] Checking Python version...
python --version

echo.
echo [2/6] Installing/updating dependencies...
pip install -r requirements.txt

echo.
echo [3/6] Testing local server...
echo Starting Flask app on http://localhost:5050
echo Press Ctrl+C to stop the server when you're done testing
echo.

set FLASK_ENV=development
set START_URL=http://testphp.vulnweb.com

python dashboard.py

echo.
echo ========================================
echo Next Steps:
echo ========================================
echo 1. Push your code to GitHub:
echo    git init
echo    git add .
echo    git commit -m "Initial commit"
echo    git remote add origin YOUR_GITHUB_URL
echo    git push -u origin main
echo.
echo 2. Deploy on Render:
echo    - Go to https://dashboard.render.com
echo    - Click New + ^> Blueprint
echo    - Connect your GitHub repository
echo    - Click Apply
echo.
echo 3. Set environment variables in Render:
echo    PYTHON_VERSION=3.11.0
echo    FLASK_ENV=production
echo    START_URL=http://testphp.vulnweb.com
echo.
echo See CHECKLIST.md for detailed instructions
echo ========================================

pause
