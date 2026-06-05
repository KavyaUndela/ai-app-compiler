@echo off
REM Health check script - verify all services are running

echo Checking AI Compiler services...
echo.

REM Check Frontend
echo [1/5] Frontend (http://localhost:3000)...
curl -s http://localhost:3000 >nul 2>&1 && echo OK || echo DOWN

REM Check Backend API
echo [2/5] Backend API (http://localhost:8000)...
curl -s http://localhost:8000/docs >nul 2>&1 && echo OK || echo DOWN

REM Check Backend Health
echo [3/5] Backend Health (http://localhost:8000/health)...
curl -s http://localhost:8000/health >nul 2>&1 && echo OK || echo DOWN

REM Check Postgres
echo [4/5] Postgres (localhost:5432)...
docker exec ai_enginner-postgres-1 pg_isready -U dev >nul 2>&1 && echo OK || echo DOWN

REM Check Redis
echo [5/5] Redis (localhost:6379)...
docker exec ai_enginner-redis-1 redis-cli ping >nul 2>&1 && echo OK || echo DOWN

echo.
echo Done!
