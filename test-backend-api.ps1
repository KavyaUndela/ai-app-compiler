# Test Backend API Endpoints
# This script verifies the backend is running and responding correctly

Write-Host ""
Write-Host "========================================"
Write-Host "Testing Backend API Endpoints"
Write-Host "========================================"
Write-Host ""

# Test 1: Health Check
Write-Host "[Test 1] Health Check - GET http://localhost:8000/api/health"
try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/api/health" -Method Get
    Write-Host "Response:" -ForegroundColor Green
    $response | ConvertTo-Json | Write-Host
} catch {
    Write-Host "Error: $($_)" -ForegroundColor Red
}
Write-Host ""

# Test 2: Generate with valid prompt
Write-Host "[Test 2] Generate Configuration - POST http://localhost:8000/api/generate"
Write-Host "Request body: {`"prompt`":`"Create a simple task management app with login`"}"
try {
    $body = @{
        prompt = "Create a simple task management app with login"
    } | ConvertTo-Json
    
    $response = Invoke-RestMethod -Uri "http://localhost:8000/api/generate" `
        -Method Post `
        -Headers @{"Content-Type" = "application/json"} `
        -Body $body
    Write-Host "Response:" -ForegroundColor Green
    $response | ConvertTo-Json | Write-Host
} catch {
    Write-Host "Error: $($_)" -ForegroundColor Red
}
Write-Host ""

# Test 3: Metrics
Write-Host "[Test 3] Get Metrics - GET http://localhost:8000/api/metrics"
try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/api/metrics" -Method Get
    Write-Host "Response:" -ForegroundColor Green
    $response | ConvertTo-Json | Write-Host
} catch {
    Write-Host "Error: $($_)" -ForegroundColor Red
}
Write-Host ""

Write-Host "========================================"
Write-Host "Tests Complete"
Write-Host "========================================"
