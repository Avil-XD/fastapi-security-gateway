#!/bin/bash

echo "Setting up FastAPI Security Gateway..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Run the server
echo "Starting server..."
echo "Dashboard will be available at: http://localhost:8000/dashboard"
python main.py