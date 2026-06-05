@echo off
setlocal enabledelayedexpansion

cd /d "%~dp0"

echo Starting backend on http://localhost:8000...
start "backend" cmd /k "cd /d "%~dp0backend" && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

echo Starting frontend on http://localhost:3000...
start "frontend" cmd /k "cd /d "%~dp0frontend" && set NEXT_PUBLIC_API_URL=http://localhost:8080/api && npm run dev"

echo Starting local proxy on http://localhost:8080...
start "proxy" cmd /k "cd /d "%~dp0frontend" && npm run proxy"

echo.
echo Your full localhost app is now available at:

echo   http://localhost:8080

echo.
echo If any process fails to start, check the terminal windows for errors.
pause
