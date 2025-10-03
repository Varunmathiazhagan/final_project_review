#!/bin/bash
# Startup script for Render deployment

echo "Starting SQL Scanner Dashboard..."
echo "Python version: $(python --version)"
echo "Installing dependencies..."

pip install -r requirements.txt

echo "Starting application..."
exec gunicorn dashboard:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120 --log-level info --access-logfile - --error-logfile -
