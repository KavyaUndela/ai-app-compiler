@echo off
REM Start both Backend and Frontend
echo.
echo ========================================
echo Starting Backend and Frontend
echo ========================================
echo.

REM Start Backend in new window
echo Starting Backend API Server on port 8000...
start "Backend API" cmd /k "cd /d "%~dp0backend" && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

REM Wait for backend to start
timeout /t 3 /nobreak

REM Start Frontend in new window
echo Starting Frontend on port 3000...
start "Frontend UI" cmd /k "cd /d "%~dp0frontend" && npm run dev"

echo.
echo ========================================
echo Services Starting...
echo ========================================
echo Backend: http://localhost:8000/api/health
echo Frontend: http://localhost:3000
echo.
echo Press any key to close this window...
pause >nul
