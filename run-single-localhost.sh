#!/bin/bash

echo ""
echo "========================================"
echo "AI Application Compiler"
echo "Single Localhost Setup (One URL)"
echo "========================================"
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo ""
    echo "❌ ERROR: Docker is not installed"
    echo ""
    echo "Please install Docker Desktop from:"
    echo "https://www.docker.com/products/docker-desktop"
    echo ""
    exit 1
fi

echo "[✓] Docker detected"
echo ""

# Check if Docker daemon is running
if ! docker ps &> /dev/null; then
    echo ""
    echo "❌ ERROR: Docker daemon is not running"
    echo ""
    echo "Please start Docker Desktop and try again"
    echo ""
    exit 1
fi

echo "[✓] Docker daemon is running"
echo ""

# Check if port 8080 is available
if lsof -Pi :8080 -sTCP:LISTEN -t >/dev/null ; then
    echo ""
    echo "⚠️  Port 8080 is already in use"
    echo ""
    echo "You can:"
    echo "  1. Close the application using port 8080"
    echo "  2. Edit docker-compose.yml to use a different port"
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo "========================================"
echo "Starting Services..."
echo "========================================"
echo ""
echo "Building Docker images (this may take 2-3 minutes)..."
echo ""

docker compose up --build

echo ""
echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo ""
echo "Your app is running at:"
echo ""
echo "   ✅ http://localhost:8080"
echo ""
echo "Access from one link:"
echo "   • Frontend: http://localhost:8080"
echo "   • API: http://localhost:8080/api"
echo "   • Docs: http://localhost:8080/docs"
echo ""
