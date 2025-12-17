#!/bin/bash
# Development run script

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✅ Using project virtual environment"
elif [ -d "/home/vineet/media-fetcher/venv" ]; then
    # Use existing venv from another project if available
    source /home/vineet/media-fetcher/venv/bin/activate
    echo "✅ Using venv from /home/vineet/media-fetcher/venv"
    
    # Check if dependencies are installed
    if ! python3 -c "import flask" 2>/dev/null; then
        echo "📦 Installing dependencies..."
        pip install -r requirements.txt
    fi
else
    echo "⚠️  No virtual environment found!"
    echo "💡 Run './setup.sh' first to create one, or:"
    echo "   python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

echo "Starting development server..."
python3 -m backend.app

