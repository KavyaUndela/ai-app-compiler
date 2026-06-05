@echo off
REM AI Application Compiler - Windows Startup Script
REM This script sets up and runs the complete application stack locally

setlocal enabledelayedexpansion

echo.
echo ========================================
echo AI Application Compiler
echo Local Development Environment
echo ========================================
echo.

REM Check if Docker is installed
docker --version >nul 2>&1
if %errorlevel% equ 0 (
    echo [✓] Docker detected
    
    echo.
    echo Would you like to run with Docker? (Y/n)
    set /p use_docker="Enter choice: "
    
    if /i "!use_docker!"=="" set use_docker=y
    if /i "!use_docker!"=="y" (
        echo.
        echo Starting with Docker Compose...
        echo.
        docker compose up --build
        exit /b
    )
)

echo.
echo Running in LOCAL MODE
echo.

REM Backend Setup
echo ========================================
echo Setting up BACKEND
echo ========================================
cd backend

if not exist .venv (
    echo Creating Python virtual environment...
    python -m venv .venv
)

echo Activating virtual environment...
call .venv\Scripts\Activate.bat

echo Installing Python dependencies...
pip install -q -r requirements.txt

echo.
echo ========================================
echo Backend is ready!
echo ========================================
echo To start backend, run this command:
echo.
echo   uvicorn app.main:app --reload --port 8000
echo.
echo After starting, the API will be available at:
echo   http://localhost:8000/docs  (Interactive API docs)
echo.

cd ..

REM Frontend Setup
echo ========================================
echo Setting up FRONTEND
echo ========================================
cd frontend

if not exist node_modules (
    echo Installing Node dependencies...
    call npm install --silent
) else (
    echo Node dependencies already installed
)

echo.
echo ========================================
echo Frontend is ready!
echo ========================================
echo To start frontend, run this command:
echo.
echo   npm run dev
echo.
echo After starting, the UI will be available at:
echo   http://localhost:3000
echo.

cd ..

echo.
echo ========================================
echo NEXT STEPS
echo ========================================
echo.
echo 1. Open TWO NEW TERMINALS (or use your IDE terminals)
echo.
echo 2. Terminal 1 - START BACKEND:
echo    cd backend
echo    .venv\Scripts\Activate.bat
echo    uvicorn app.main:app --reload --port 8000
echo.
echo 3. Terminal 2 - START FRONTEND:
echo    cd frontend
echo    npm run dev
echo.
echo 4. Open browser to http://localhost:3000
echo.
echo 5. Try a sample prompt and click "Generate Configuration"
echo.
echo ========================================
echo OPTIONAL: Run Backend Tests
echo ========================================
echo.
echo   cd backend
echo    .venv\Scripts\Activate.bat
echo    python test_pipeline.py
echo.
echo ========================================
echo.
pause
