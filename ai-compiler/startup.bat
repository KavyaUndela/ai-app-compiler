@echo off
REM AI Application Compiler - Complete Startup Script (Windows)

echo.
echo ========================================
echo AI Application Compiler - Local Setup
echo ========================================
echo.

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found. Please install Python 3.12+
    exit /b 1
)

REM Check Node.js
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Node.js not found. Please install Node.js 20+
    exit /b 1
)

echo [1/5] Setting up Backend...
cd backend

if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

call venv\Scripts\activate.bat

echo Installing backend dependencies...
pip install -q -r requirements.txt

if not exist .env (
    echo Creating .env file...
    copy .env.example .env
)

echo Seeding database...
python scripts/seed_db.py

echo.
echo [2/5] Backend ready!
echo.
echo To start backend, in this terminal run:
echo   uvicorn app.main:app --reload
echo.
echo Backend will be available at: http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo.

cd ..

REM Second terminal for frontend
start cmd /k "cd frontend & npm install & npm run dev"

echo.
echo [3/5] Frontend installing...
echo Wait for npm install to complete in the new window.
echo.

timeout /t 5 /nobreak

cd backend
call venv\Scripts\activate.bat
echo.
echo [4/5] Starting Backend Server...
echo.
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

echo.
echo [5/5] Setup Complete!
echo.
echo Frontend: http://localhost:3000
echo Backend: http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo.
pause
