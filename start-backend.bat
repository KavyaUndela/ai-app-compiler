@echo off
REM Start Backend API Server
echo.
echo ========================================
echo Starting Backend API Server
echo ========================================
echo.

cd /d "%~dp0backend"
echo Current directory: %cd%
echo.

echo Installing/checking dependencies...
pip install -q -r requirements.txt

echo.
echo Starting API server on http://localhost:8000
echo Press Ctrl+C to stop
echo.

python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

pause
