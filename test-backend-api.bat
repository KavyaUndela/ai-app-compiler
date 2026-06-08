@echo off
REM Test Backend API Endpoints
REM This script verifies the backend is running and responding correctly

echo.
echo ========================================
echo Testing Backend API Endpoints
echo ========================================
echo.

REM Test 1: Health Check
echo [Test 1] Health Check - GET http://localhost:8000/api/health
curl -X GET http://localhost:8000/api/health
echo.
echo.

REM Test 2: Generate with valid prompt
echo [Test 2] Generate Configuration - POST http://localhost:8000/api/generate
echo Request body: {"prompt":"Create a simple task management app with login"}
curl -X POST http://localhost:8000/api/generate ^
  -H "Content-Type: application/json" ^
  -d "{\"prompt\":\"Create a simple task management app with login\"}"
echo.
echo.

REM Test 3: Metrics
echo [Test 3] Get Metrics - GET http://localhost:8000/api/metrics
curl -X GET http://localhost:8000/api/metrics
echo.
echo.

echo ========================================
echo Tests Complete
echo ========================================
pause
