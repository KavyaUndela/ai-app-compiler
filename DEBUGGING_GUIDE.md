# Frontend-Backend Communication Debugging Guide

## Overview
This guide explains how to diagnose and fix "Network Error" issues when generating blueprints.

## Current Setup

### Backend Endpoints
- **Development**: `http://localhost:8000`
- **Endpoints Available**:
  - GET `/health` - Health check
  - GET `/api/health` - API health check
  - POST `/generate` or `/api/generate` - Generate configuration
  - POST `/validate` or `/api/validate` - Validate schema
  - POST `/repair` or `/api/repair` - Repair schema
  - POST `/runtime-preview` or `/api/runtime-preview` - Get runtime preview

### Frontend Environment Variables
```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

The frontend API service appends the endpoint to this base URL:
- `/api/generate` → `http://localhost:8000/api/generate`
- `/api/health` → `http://localhost:8000/api/health`

## Debugging Steps

### 1. Check Backend Health
```bash
# Terminal
curl http://localhost:8000/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "ai-app-compiler",
  "version": "1.0.0"
}
```

### 2. Check Frontend Console Logs
Open browser DevTools (F12) → Console tab:

Look for logs like:
```
API Configuration: {
  API_URL: "http://localhost:8000/api",
  ENV_SET: true,
  ENVIRONMENT: "development"
}
```

### 3. Monitor API Requests
In browser DevTools → Network tab:
1. Generate blueprint
2. Look for request to `/api/generate`
3. Check:
   - **Status**: Should be 200 (success) or 500 (server error)
   - **Request Headers**: Look for `Content-Type: application/json`
   - **Response Headers**: Look for `Access-Control-Allow-Origin`
   - **Response Body**: Should contain compilation result or error details

### 4. Backend Logs
When running backend locally, check console output for:
```
INFO:root:Received generate request with prompt: ...
INFO:root:Successfully generated configuration: ...
```

Or error logs:
```
ERROR:root:Compilation failed: ...
```

## Common Issues and Solutions

### Issue: "Network Error" in UI
**Symptoms**: "Failed to generate configuration: Network Error" message

**Possible Causes**:
1. Backend not running
2. NEXT_PUBLIC_API_URL not set correctly
3. CORS headers missing
4. Backend endpoint not found

**Solutions**:
1. Verify backend is running: `curl http://localhost:8000/api/health`
2. Check NEXT_PUBLIC_API_URL in browser console (DevTools → Console)
3. Check browser Network tab for CORS error headers
4. Check backend logs for request reception

### Issue: "Failed to generate configuration: 404"
**Symptoms**: Backend endpoint not found

**Possible Causes**:
- Frontend calling wrong endpoint path
- Backend routes not properly registered

**Solutions**:
- Verify endpoints in backend logs show routes registered at startup
- Check frontend is using `/api/generate` not `/generate`

### Issue: "Failed to generate configuration: 500"
**Symptoms**: Server error

**Possible Causes**:
- Issue in compilation logic
- Missing dependencies
- Invalid request format

**Solutions**:
- Check backend logs for detailed error
- Verify backend logs show stack trace with `exc_info=True`
- Check if all services (intent_extraction, schema_generator, etc.) are working

## Environment Configuration

### Development Setup
Create `frontend/.env.local`:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api
NEXT_PUBLIC_DEBUG=true
```

### Production Setup
Set environment variable during deployment:
```bash
# Example for Vercel
vercel env add NEXT_PUBLIC_API_URL https://your-backend.com/api
```

## Monitoring & Logging

### Frontend Logging
The frontend now includes:
- API initialization logs
- Request/response logging via axios interceptors
- Detailed error messages with API URL

To view: Browser DevTools → Console tab

### Backend Logging
The backend now includes:
- Startup logs showing registered endpoints
- Request logs with timestamp
- Error logs with full stack trace

To view: Terminal where backend is running

## Testing Checklist

- [ ] Backend health check returns 200
- [ ] Frontend console shows correct API_URL
- [ ] Network tab shows POST request to `/api/generate`
- [ ] Network response is 200 or has error details
- [ ] Backend logs show "Received generate request"
- [ ] Backend logs show "Successfully generated" or error
- [ ] Error message in UI shows API URL for debugging
- [ ] CORS headers present in response (`Access-Control-Allow-Origin`)

## Performance Monitoring

If requests are slow:
1. Check backend logs for compilation time
2. Check Network tab for response time
3. Monitor backend CPU/memory usage
4. Profile individual services (intent_extraction, schema_generator, etc.)

## Next Steps if Still Failing

1. **Isolate**: Test each component independently
   - Backend health: `curl http://localhost:8000/api/health`
   - Backend generate: `curl -X POST http://localhost:8000/api/generate -d '{"prompt":"test"}' -H 'Content-Type: application/json'`

2. **Logs**: Increase logging verbosity if needed
   - Set `logging.basicConfig(level=logging.DEBUG)` in backend
   - Check browser console for full error stack

3. **Network**: Verify network connectivity
   - Check firewall rules
   - Verify ports are open (8000 for backend, 3000 for frontend)
   - Test from frontend container/VM if deployed

4. **CORS**: If CORS error persists
   - Add frontend URL to CORS origins in backend/app/main.py
   - Test with `curl -H "Origin: http://frontend-url" ...`

## References
- [Backend Routes](../backend/app/api/routes.py)
- [Frontend API Service](../frontend/src/services/api.ts)
- [Backend CORS Setup](../backend/app/main.py)
