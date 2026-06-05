#!/bin/bash

# AI Application Compiler - Unix Startup Script
# This script sets up and runs the complete application stack locally

set -e

echo ""
echo "========================================"
echo "AI Application Compiler"
echo "Local Development Environment"
echo "========================================"
echo ""

# Check if Docker is installed
if command -v docker &> /dev/null; then
    echo "[✓] Docker detected"
    echo ""
    read -p "Would you like to run with Docker? (Y/n) " use_docker
    use_docker=${use_docker:-y}
    
    if [[ $use_docker == "y" || $use_docker == "Y" ]]; then
        echo ""
        echo "Starting with Docker Compose..."
        echo ""
        docker compose up --build
        exit 0
    fi
fi

echo ""
echo "Running in LOCAL MODE"
echo ""

# Backend Setup
echo "========================================"
echo "Setting up BACKEND"
echo "========================================"
cd backend

if [ ! -d ".venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv .venv
fi

echo "Activating virtual environment..."
source .venv/bin/activate

echo "Installing Python dependencies..."
pip install -q -r requirements.txt

echo ""
echo "========================================"
echo "Backend is ready!"
echo "========================================"
echo "To start backend, run this command:"
echo ""
echo "  uvicorn app.main:app --reload --port 8000"
echo ""
echo "After starting, the API will be available at:"
echo "  http://localhost:8000/docs  (Interactive API docs)"
echo ""

cd ..

# Frontend Setup
echo "========================================"
echo "Setting up FRONTEND"
echo "========================================"
cd frontend

if [ ! -d "node_modules" ]; then
    echo "Installing Node dependencies..."
    npm install --silent
else
    echo "Node dependencies already installed"
fi

echo ""
echo "========================================"
echo "Frontend is ready!"
echo "========================================"
echo "To start frontend, run this command:"
echo ""
echo "  npm run dev"
echo ""
echo "After starting, the UI will be available at:"
echo "  http://localhost:3000"
echo ""

cd ..

echo ""
echo "========================================"
echo "NEXT STEPS"
echo "========================================"
echo ""
echo "1. Open TWO NEW TERMINALS"
echo ""
echo "2. Terminal 1 - START BACKEND:"
echo "   cd backend"
echo "   source .venv/bin/activate"
echo "   uvicorn app.main:app --reload --port 8000"
echo ""
echo "3. Terminal 2 - START FRONTEND:"
echo "   cd frontend"
echo "   npm run dev"
echo ""
echo "4. Open browser to http://localhost:3000"
echo ""
echo "5. Try a sample prompt and click 'Generate Configuration'"
echo ""
echo "========================================"
echo "OPTIONAL: Run Backend Tests"
echo "========================================"
echo ""
echo "   cd backend"
echo "   source .venv/bin/activate"
echo "   python test_pipeline.py"
echo ""
echo "========================================"
echo ""
