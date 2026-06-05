#!/bin/bash
# AI Compiler - Linux/macOS Startup Script
# This script starts the full dev stack: infra, backend, and frontend

set -e

echo "========================================"
echo "AI Compiler - Full Stack Startup"
echo "========================================"

# Check for Docker
if ! command -v docker &> /dev/null; then
    echo "ERROR: Docker not found. Please install Docker Desktop."
    exit 1
fi

# Get repo root
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$REPO_ROOT"

# Start infra
echo ""
echo "[1/3] Starting infrastructure (Postgres, Redis)..."
cd infra/docker
docker compose up -d
sleep 15
cd "$REPO_ROOT"

# Backend setup
echo ""
echo "[2/3] Setting up backend..."
cd apps/api
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi
source .venv/bin/activate
python -m pip install --upgrade pip -q
pip install -r requirements.txt -q

# Create .env if not exists
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "Created .env file. Edit it with your secrets!"
fi

# Start backend
echo "Starting FastAPI backend..."
uvicorn compiler_api.core.app:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
cd "$REPO_ROOT"
sleep 5

# Frontend setup
echo ""
echo "[3/3] Setting up frontend..."
cd web
if [ ! -d "node_modules" ]; then
    npm install -q
fi

# Start frontend
echo "Starting Next.js frontend..."
npm run dev &
FRONTEND_PID=$!
cd "$REPO_ROOT"

echo ""
echo "========================================"
echo "Stack startup complete!"
echo "========================================"
echo ""
echo "Frontend:  http://localhost:3000"
echo "Backend:   http://localhost:8000"
echo "pgAdmin:   http://localhost:8080 (admin@local / admin)"
echo ""
echo "Press Ctrl+C to stop all services"

# Keep script running
wait
