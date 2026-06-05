@echo off
setlocal enabledelayedexpansion

echo.
echo ========================================
echo AI Application Compiler
echo Single Localhost Setup (One URL)
echo ========================================
echo.

REM Check if Docker is installed
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ❌ ERROR: Docker is not installed or not in PATH
    echo.
    echo Please install Docker Desktop from:
    echo https://www.docker.com/products/docker-desktop
    echo.
    pause
    exit /b 1
)

echo [✓] Docker detected
echo.

REM Check if Docker daemon is running
docker ps >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ❌ ERROR: Docker daemon is not running
    echo.
    echo Please start Docker Desktop and try again
    echo.
    pause
    exit /b 1
)

echo [✓] Docker daemon is running
echo.

REM Check if port 8080 is available
netstat -ano | findstr ":8080 " >nul 2>&1
if %errorlevel% equ 0 (
    echo.
    echo ⚠️  Port 8080 is already in use
    echo.
    echo You can:
    echo   1. Close the application using port 8080
    echo   2. Edit docker-compose.yml to use a different port
    echo.
    choice /C YN /M "Continue anyway? (Y=Yes, N=No)"
    if !errorlevel! neq 1 exit /b 1
)

echo ========================================
echo Starting Services...
echo ========================================
echo.
echo Building Docker images (this may take 2-3 minutes)...
docker compose up --build

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Your app is running at:
echo.
echo   ✅ http://localhost:8080
echo.
echo Access from one link:
echo   • Frontend: http://localhost:8080
echo   • API: http://localhost:8080/api
echo   • Docs: http://localhost:8080/docs
echo.
echo.
pause
