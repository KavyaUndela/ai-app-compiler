# ✅ STARTUP CHECKLIST & EXACT COMMANDS

## Pre-Flight Checks

### System Requirements
- [ ] Python 3.12 or higher installed
  - Verify: `python --version` (should be 3.12+)
- [ ] Node.js 20 or higher installed
  - Verify: `node --version` (should be 20.x or higher)
- [ ] npm installed
  - Verify: `npm --version`
- [ ] Ports 3000 and 8000 are free
  - Windows: `netstat -ano | findstr :3000` or `:8000`
  - Unix: `lsof -i :3000` or `:8000`

### Project Location
- [ ] Verify project exists at:
  ```
  C:\Users\anush\OneDrive\Desktop\AI Enginner\ai-compiler
  ```

---

## 🚀 STARTUP METHOD 1: AUTOMATED (Windows)

**Fastest Method - One Click**

```batch
cd C:\Users\anush\OneDrive\Desktop\AI Enginner\ai-compiler
startup.bat
```

### What Happens Automatically
- [ ] Creates Python virtual environment
- [ ] Installs backend dependencies
- [ ] Creates backend .env file
- [ ] Seeds database with sample data
- [ ] Opens new terminal for frontend
- [ ] Starts frontend npm install
- [ ] Starts backend server
- [ ] Displays all URLs when ready

### Expected Output After Running
```
Backend running at: http://localhost:8000
Frontend running at: http://localhost:3000
API Docs at: http://localhost:8000/docs
```

### Next: Open Browser
1. Go to http://localhost:3000
2. Click "Start Compiling"
3. Fill in form
4. Click "Compile Application"

---

## 🐳 STARTUP METHOD 2: DOCKER (All Platforms)

**Easiest - No Manual Setup**

### Prerequisites
- Docker Desktop installed and running
- Ports 3000, 8000 free

### Command
```bash
cd C:\Users\anush\OneDrive\Desktop\AI Enginner\ai-compiler
docker-compose up --build
```

### Expected Output (wait for "ready" messages)
```
backend-service    | INFO:     Application startup complete [Press ENTER to continue]
frontend-service   | ▲ Ready in XXms
```

### Verify Services
```bash
# In another terminal
curl http://localhost:8000/health
curl http://localhost:3000
```

### Stop Services
Press `Ctrl+C` in terminal or:
```bash
docker-compose down
```

### Next: Open Browser
1. Go to http://localhost:3000
2. Proceed as in Method 1

---

## 🔨 STARTUP METHOD 3: MANUAL (Step-by-Step)

**For Understanding Each Step**

### Terminal 1: Backend Setup & Start

```bash
# Navigate to backend directory
cd "C:\Users\anush\OneDrive\Desktop\AI Enginner\ai-compiler\backend"

# Create Python virtual environment
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Copy environment template
copy .env.example .env

# Seed database with sample data
python scripts/seed_db.py

# Start backend server with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Expected Backend Output
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

✅ Backend ready at http://localhost:8000

### Terminal 2: Frontend Setup & Start

```bash
# Open new terminal/cmd window
# Navigate to frontend directory
cd "C:\Users\anush\OneDrive\Desktop\AI Enginner\ai-compiler\frontend"

# Copy environment template
copy .env.example .env.local

# Install Node dependencies
npm install

# Start development server
npm run dev
```

### Expected Frontend Output
```
▲ Next.js 14.0.0
  ▲ Local:        http://localhost:3000
```

✅ Frontend ready at http://localhost:3000

---

## ✅ VERIFY EVERYTHING WORKS

### Step 1: Check Backend Health
```bash
curl http://localhost:8000/health
```

**Expected Response:**
```json
{"status":"healthy"}
```

### Step 2: Check API Docs
1. Open http://localhost:8000/docs in browser
2. Should see Swagger UI with all endpoints

### Step 3: Check Frontend Loads
1. Open http://localhost:3000 in browser
2. Should see home page with title "AI Application Compiler"

### Step 4: Test Full Pipeline
1. Click "Start Compiling" button
2. Fill in form:
   - **Title:** "E-commerce Platform"
   - **Description:** "Modern e-commerce with shopping cart and payment processing"
   - **Features:** (one per line)
     ```
     User authentication
     Product search
     Shopping cart
     Payment processing
     Order tracking
     ```
   - **Constraints:** "Must handle 10k concurrent users"
3. Click "Compile Application"
4. Wait for result (should take 1-2 seconds)
5. View compilation results

### Step 5: Check Dashboard
1. Click "Dashboard" in navigation
2. Should see metrics, statistics, and charts
3. Should list recent compilations

---

## 🧪 SAMPLE TEST COMPILATIONS

### Test 1: Simple Blog
```json
{
  "title": "Blog System",
  "description": "Simple blog platform with posts and comments",
  "features": ["Create posts", "Comments", "User roles"],
  "constraints": null,
  "tech_preferences": {"frontend": "Next.js", "backend": "FastAPI"}
}
```

### Test 2: Task Manager
```json
{
  "title": "Task Management",
  "description": "Collaborative task manager with real-time updates",
  "features": ["Create tasks", "Team collaboration", "Real-time updates"],
  "constraints": "Mobile responsive",
  "tech_preferences": {"frontend": "Next.js", "backend": "FastAPI"}
}
```

### Test 3: Complex E-commerce
```json
{
  "title": "Enterprise E-commerce",
  "description": "Large-scale e-commerce with inventory management, analytics, and multi-vendor support",
  "features": [
    "User authentication",
    "Product catalog",
    "Shopping cart",
    "Payment processing",
    "Order tracking",
    "Inventory management",
    "Analytics dashboard",
    "Multi-vendor support"
  ],
  "constraints": "Must handle 100k concurrent users, <100ms response time",
  "tech_preferences": {
    "frontend": "Next.js",
    "backend": "FastAPI",
    "database": "PostgreSQL",
    "cache": "Redis"
  }
}
```

---

## 🛠️ TROUBLESHOOTING

### Issue: "Port 3000 already in use"

**Solution:**
```bash
# Find and kill process on port 3000
netstat -ano | findstr :3000
taskkill /PID <PID_FROM_ABOVE> /F

# Or change port in frontend/next.config.js
```

### Issue: "Port 8000 already in use"

**Solution:**
```bash
# Find and kill process on port 8000
netstat -ano | findstr :8000
taskkill /PID <PID_FROM_ABOVE> /F

# Or change port in backend startup command
```

### Issue: "Python not found"

**Solution:**
- Install Python 3.12+ from python.org
- Add Python to PATH
- Restart terminal
- Verify: `python --version`

### Issue: "Node not found"

**Solution:**
- Install Node.js 20+ from nodejs.org
- Add Node to PATH
- Restart terminal
- Verify: `node --version`

### Issue: "Module not found" (Python)

**Solution:**
```bash
# Ensure virtual environment is activated
cd backend
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: "Module not found" (Node)

**Solution:**
```bash
cd frontend
# Delete node_modules and reinstall
rmdir /s node_modules  # Windows
rm -rf node_modules  # Mac/Linux

npm install
```

### Issue: "Cannot connect to localhost:8000 from frontend"

**Solution:**
1. Check `.env.local` in frontend folder
2. Should contain: `NEXT_PUBLIC_API_URL=http://localhost:8000`
3. Restart frontend: `npm run dev`

### Issue: "Database is locked"

**Solution:**
```bash
# Stop all processes
# Delete database
cd backend
del compiler.db  # Windows
rm compiler.db  # Mac/Linux

# Reseed
python scripts/seed_db.py

# Restart backend
```

### Issue: "CORS Error in browser"

**Solution:**
1. Verify backend is running: `curl http://localhost:8000/health`
2. Check CORS_ORIGINS in backend/app/config.py
3. Should include `http://localhost:3000`
4. Restart backend

---

## 📱 ACCESSING THE APPLICATION

### After Startup

| Service | URL | Purpose |
|---------|-----|---------|
| Frontend | http://localhost:3000 | Main application |
| Backend API | http://localhost:8000 | API endpoints |
| API Docs | http://localhost:8000/docs | Interactive Swagger UI |
| ReDoc | http://localhost:8000/redoc | Alternative API docs |
| Compiler | http://localhost:3000/compiler | Compilation interface |
| Dashboard | http://localhost:3000/dashboard | Metrics dashboard |

---

## 🎯 COMMON WORKFLOWS

### Workflow 1: Quick Test
1. Run startup.bat
2. Wait for "ready" messages
3. Open http://localhost:3000/compiler
4. Enter requirements
5. Click compile
6. View results

### Workflow 2: Development
1. Start backend: Terminal 1
2. Start frontend: Terminal 2
3. Edit code in your IDE
4. Changes auto-reload
5. Refresh browser to see changes

### Workflow 3: Debug API
1. Start backend
2. Open http://localhost:8000/docs
3. Try out endpoints directly
4. See request/response
5. Check backend logs in terminal

### Workflow 4: Reset Everything
1. Stop both services (Ctrl+C)
2. Delete backend/compiler.db
3. Run startup.bat again
4. Database reseeds automatically

---

## 📝 IMPORTANT FILES

### Configuration
- `backend/.env` - Backend config (auto-created)
- `frontend/.env.local` - Frontend config (auto-created)
- `docker-compose.yml` - Docker setup

### Scripts
- `startup.bat` - Windows automation
- `startup.sh` - Unix automation
- `backend/scripts/seed_db.py` - Database seeding

### Documentation
- `README.md` - Full documentation
- `QUICK_START.md` - Quick reference
- `ARCHITECTURE.md` - System design
- `PROJECT_SUMMARY.md` - Overview

---

## 🎓 LEARNING RESOURCES

### Understanding the Code
1. Start with `backend/app/main.py` - Entry point
2. Review `backend/app/services/` - Business logic
3. Check `frontend/src/app/` - Pages
4. Read `ARCHITECTURE.md` - System overview

### API Testing
- Use http://localhost:8000/docs for interactive testing
- Or use cURL commands from QUICK_START.md
- Or use Postman (import from API docs)

### Frontend Development
- Edit files in `frontend/src/`
- Changes auto-reload with `npm run dev`
- Check browser console for errors
- Use React DevTools browser extension

### Backend Development
- Edit files in `backend/app/`
- Changes auto-reload with `--reload` flag
- Check terminal for error logs
- Use http://localhost:8000/docs to test

---

## ✅ FINAL CHECKLIST BEFORE RUNNING

### System Check
- [ ] Python 3.12+ installed and in PATH
- [ ] Node.js 20+ installed and in PATH
- [ ] npm installed
- [ ] Ports 3000, 8000 are free
- [ ] ~500MB disk space available

### Project Check
- [ ] Extracted/cloned complete project
- [ ] All files present (verify 42+ files)
- [ ] Readable file permissions

### Selection Check
- [ ] Decided on startup method (1, 2, or 3)
- [ ] Read relevant instructions above
- [ ] Ready to copy/paste commands

### Ready?
- [ ] Yes! Follow instructions for your chosen method

---

## 🎉 YOU'RE READY!

Choose your startup method above and follow exact commands.

### Quick Links
- **Windows Users:** Use `startup.bat` (Method 1)
- **Docker Users:** Use Method 2
- **Learning Mode:** Use Method 3

**Estimated startup time:**
- Method 1: 3-5 minutes
- Method 2: 2-3 minutes
- Method 3: 5-7 minutes

---

**Everything is ready. Just pick a method and run the commands!** 🚀
