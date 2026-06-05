@echo off
REM AI Compiler - Windows Startup Script
REM This script starts the full dev stack: infra, backend, and frontend

echo ========================================
echo AI Compiler - Full Stack Startup
echo ========================================

REM Check for Docker
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Docker not found. Please install Docker Desktop.
    exit /b 1
)

REM Start infra
echo.
echo [1/3] Starting infrastructure (Postgres, Redis)...
cd infra\docker
docker compose up -d
if %errorlevel% neq 0 (
    echo ERROR: Failed to start Docker Compose.
    exit /b 1
)
cd ..\..
timeout /t 10 /nobreak

REM Backend setup
echo.
echo [2/3] Setting up backend...
cd apps\api
if not exist ".venv" (
    python -m venv .venv
)
call .venv\Scripts\Activate.ps1 || cmd /c ".venv\Scripts\activate.bat"
python -m pip install --upgrade pip -q
pip install -r requirements.txt -q
if %errorlevel% neq 0 (
    echo ERROR: Failed to install backend dependencies.
    exit /b 1
)

REM Create .env if not exists
if not exist ".env" (
    copy .env.example .env
    echo Created .env file. Edit it with your secrets!
)

REM Start backend in new terminal window
echo Starting FastAPI backend...
start cmd /k "cd apps\api && .venv\Scripts\Activate.ps1 && uvicorn compiler_api.core.app:app --reload --host 0.0.0.0 --port 8000"
cd ..\..

REM Frontend setup
echo.
echo [3/3] Setting up frontend...
cd web
if not exist "node_modules" (
    npm install -q
)
if %errorlevel% neq 0 (
    echo ERROR: Failed to install frontend dependencies.
    exit /b 1
)

REM Start frontend in new terminal window
echo Starting Next.js frontend...
start cmd /k "cd web && npm run dev"
cd ..

echo.
echo ========================================
echo Stack startup complete!
echo ========================================
echo.
echo Frontend:  http://localhost:3000
echo Backend:   http://localhost:8000
echo pgAdmin:   http://localhost:8080 (admin@local / admin)
echo.
echo Check the two new terminal windows for logs.
echo Press Ctrl+C in each terminal to stop.
