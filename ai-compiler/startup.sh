#!/bin/bash

# AI Application Compiler - Complete Startup Script (Unix/macOS/Linux)

echo ""
echo "========================================"
echo "AI Application Compiler - Local Setup"
echo "========================================"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 not found. Please install Python 3.12+"
    exit 1
fi

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "ERROR: Node.js not found. Please install Node.js 20+"
    exit 1
fi

echo "[1/5] Setting up Backend..."
cd backend

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate

echo "Installing backend dependencies..."
pip install -q -r requirements.txt

# Create .env if not exists
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
fi

echo "Seeding database..."
python scripts/seed_db.py

echo ""
echo "[2/5] Backend ready!"
echo ""
echo "To start backend:"
echo "  uvicorn app.main:app --reload"
echo ""
echo "Backend: http://localhost:8000"
echo "API Docs: http://localhost:8000/docs"
echo ""

cd ..

# Start frontend in background
echo "[3/5] Setting up Frontend..."
cd frontend

# Create .env if not exists
if [ ! -f ".env.local" ]; then
    echo "Creating .env.local file..."
    cp .env.example .env.local
fi

echo "Installing frontend dependencies..."
npm install -q

echo ""
echo "[4/5] Frontend ready!"
echo ""
echo "To start frontend in another terminal:"
echo "  cd frontend"
echo "  npm run dev"
echo ""
echo "Frontend: http://localhost:3000"
echo ""

cd ..

# Start backend
echo "[5/5] Starting Backend Server..."
echo ""
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
