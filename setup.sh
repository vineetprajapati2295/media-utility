#!/bin/bash
# Setup script - creates virtual environment and installs dependencies

echo "Setting up Media Utility Platform..."

# Check if virtual environment exists
if [ -d "venv" ]; then
    echo "Virtual environment already exists."
    read -p "Recreate it? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Removing existing virtual environment..."
        rm -rf venv
    else
        echo "Using existing virtual environment."
        source venv/bin/activate
        pip install -r requirements.txt
        echo "Setup complete!"
        exit 0
    fi
fi

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "To activate the virtual environment manually:"
echo "  source venv/bin/activate"
echo ""
echo "To run the development server:"
echo "  ./run_dev.sh"
echo ""

