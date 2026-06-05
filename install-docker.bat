@echo off
setlocal enabledelayedexpansion

echo.
echo ========================================
echo Docker Desktop Installer
echo ========================================
echo.
echo This will install Docker Desktop on Windows.
echo.
echo Requirements:
echo  - Windows 10/11 Pro, Enterprise, or Education
echo  - 4GB RAM minimum (8GB recommended)
echo  - Hyper-V enabled
echo.
pause

echo.
echo Downloading Docker Desktop installer...
echo.

REM Download Docker Desktop installer
powershell -Command "& {
    $url = 'https://desktop.docker.com/win/stable/amd64/Docker%20Desktop%20Installer.exe'
    $output = '%TEMP%\DockerInstaller.exe'
    Write-Host 'Downloading from: '$url
    Write-Host 'Saving to: '$output
    
    try {
        [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
        $client = New-Object System.Net.WebClient
        $client.DownloadFile($url, $output)
        Write-Host 'Download complete!'
        Write-Host $output
        exit 0
    } catch {
        Write-Host 'Download failed: '$_.Exception.Message
        exit 1
    }
}"

if %errorlevel% neq 0 (
    echo.
    echo Download failed. Please download manually from:
    echo https://www.docker.com/products/docker-desktop
    echo.
    pause
    exit /b 1
)

echo.
echo Starting Docker Desktop installation...
echo.
echo IMPORTANT: When prompted:
echo   1. Check "Install required Windows components"
echo   2. Check "Add Docker Desktop to the PATH"
echo   3. Complete the installation
echo   4. Restart your computer when finished
echo.
pause

REM Run the installer
"%TEMP%\DockerInstaller.exe"

echo.
echo ========================================
echo Installation Started!
echo ========================================
echo.
echo NEXT STEPS:
echo  1. Complete the Docker Desktop installation
echo  2. Restart your computer
echo  3. Open a new terminal
echo  4. Run: docker --version
echo  5. Run: cd "C:\Users\anush\OneDrive\Desktop\AI Enginner"
echo  6. Run: docker compose up --build
echo.
pause
