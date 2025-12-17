#!/bin/bash
# Production run script

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Check if gunicorn is installed
if command -v gunicorn &> /dev/null; then
    echo "Starting with Gunicorn (Production)..."
    gunicorn -c gunicorn_config.py backend.app:app
else
    echo "Gunicorn not found. Starting with Flask dev server..."
    echo "Install Gunicorn for production: pip install gunicorn"
    python3 -m backend.app
fi

