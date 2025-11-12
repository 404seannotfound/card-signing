#!/bin/bash

# Quick start script for local development

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -q -r requirements.txt

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env and set a secure SECRET_KEY"
fi

# Run the application
echo "Starting Flask application..."
echo "Access the app at: http://localhost:5000"
python app.py
