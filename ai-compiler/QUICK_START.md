# 🚀 AI Application Compiler - Quick Start Guide

## System Requirements
- **Python:** 3.12 or higher
- **Node.js:** 20 or higher
- **npm:** 10 or higher

## Option 1: Automated Setup (Recommended)

### Windows
```cmd
cd ai-compiler
startup.bat
```

This will:
1. Create Python virtual environment
2. Install backend dependencies
3. Seed database with sample data
4. Start frontend installation in new terminal
5. Start backend server at http://localhost:8000

### macOS/Linux
```bash
cd ai-compiler
chmod +x startup.sh
./startup.sh
```

---

## Option 2: Manual Setup

### Backend Setup (Terminal 1)

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Seed database with sample data
python scripts/seed_db.py

# Start backend server
uvicorn app.main:app --reload
```

✅ Backend ready at: **http://localhost:8000**
📖 API Docs at: **http://localhost:8000/docs**

### Frontend Setup (Terminal 2)

```bash
# Navigate to frontend
cd frontend

# Copy environment file
cp .env.example .env.local

# Install dependencies
npm install

# Start development server
npm run dev
```

✅ Frontend ready at: **http://localhost:3000**

---

## Option 3: Docker Setup (Easiest)

### Prerequisites
- Docker Desktop installed and running

### Launch Everything with One Command

```bash
cd ai-compiler
docker-compose up --build
```

Wait for both services to be ready, then:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

Stop with: `Ctrl+C` or `docker-compose down`

---

## ✅ Verify Setup

### Check Backend Health
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{"status": "healthy"}
```

### Check Frontend
Open http://localhost:3000 in browser

### Check API Documentation
Visit http://localhost:8000/docs (interactive Swagger UI)

---

## 🧪 Test the Compiler

### Via Web Interface (Easiest)

1. Open http://localhost:3000
2. Click "Start Compiling" (or navigate to /compiler)
3. Fill in form:
   - **Title:** "E-commerce Platform"
   - **Description:** "A modern e-commerce platform with shopping cart and payments"
   - **Features:**
     ```
     User authentication
     Product search
     Shopping cart
     Payment processing
     Order tracking
     ```
   - **Constraints:** "Must handle 10k concurrent users"
4. Click "Compile Application"
5. View results including:
   - Architecture design
   - System components
   - Validation score
   - Performance estimates

### Via API (cURL)

```bash
curl -X POST http://localhost:8000/api/compile \
  -H "Content-Type: application/json" \
  -d '{
    "requirement": {
      "title": "Task Management App",
      "description": "Collaborative task manager with real-time updates",
      "features": ["Create tasks", "Team collaboration", "Real-time updates"],
      "constraints": "Must be responsive on mobile",
      "tech_preferences": {"frontend": "Next.js", "backend": "FastAPI"}
    },
    "include_simulation": true,
    "include_repairs": true
  }'
```

---

## 📊 View Metrics

Navigate to **Dashboard** (http://localhost:3000/dashboard) to see:
- Compilation statistics
- Success rates
- API performance metrics
- Recent compilations

---

## 🔧 Development

### Backend Changes
- Backend auto-reloads with `--reload` flag
- Edit files in `backend/app/` and refresh API

### Frontend Changes
- Frontend auto-reloads on file save
- Edit files in `frontend/src/` and refresh browser

### Add New Models
Edit `backend/app/models/__init__.py`

### Add New Services
Create file in `backend/app/services/`

### Add New Pages
Create file in `frontend/src/app/`

---

## 🗄️ Database

### View Database Content
- Database file: `backend/compiler.db`
- Auto-created SQLite database
- Seeded with sample data on startup

### Reset Database
```bash
# Delete database
rm backend/compiler.db

# Reseed
python backend/scripts/seed_db.py
```

---

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Windows - Find and kill process on port 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/macOS - Find process on port 8000
lsof -i :8000
kill -9 <PID>
```

### Backend Won't Connect
1. Verify backend is running: `curl http://localhost:8000/health`
2. Check frontend `.env.local` has `NEXT_PUBLIC_API_URL=http://localhost:8000`

### Frontend Build Errors
```bash
cd frontend
rm -rf node_modules .next
npm install
npm run dev
```

### Database Lock Error
```bash
# Remove database and reseed
rm backend/compiler.db
python backend/scripts/seed_db.py
```

---

## 📁 Project Structure

```
ai-compiler/
├── backend/                # FastAPI application
│   ├── app/
│   │   ├── main.py        # Entry point
│   │   ├── models/        # Request/response models
│   │   ├── schemas/       # Database models
│   │   ├── services/      # Business logic
│   │   └── routes/        # API endpoints
│   ├── scripts/
│   │   └── seed_db.py     # Database seeding
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
│
├── frontend/              # Next.js application
│   ├── src/
│   │   ├── app/          # Pages and layouts
│   │   ├── components/   # React components
│   │   ├── lib/          # Utilities
│   │   └── styles/       # CSS
│   ├── package.json
│   ├── Dockerfile
│   └── .env.example
│
├── docker-compose.yml    # Multi-container setup
├── startup.bat          # Windows startup script
├── startup.sh           # Unix startup script
└── README.md            # Full documentation
```

---

## 🎓 Next Steps

1. **Explore the Codebase**
   - Check `backend/app/main.py` for API structure
   - Review `backend/app/services/` for compilation logic
   - Browse `frontend/src/app/` for UI pages

2. **Modify and Extend**
   - Add new pipeline stages in services
   - Create new pages in frontend
   - Customize styling with Tailwind CSS

3. **Production Deployment**
   - Switch to PostgreSQL database
   - Build Docker images
   - Deploy to cloud platform

---

## 📞 Quick Commands Reference

```bash
# Backend
cd backend && source venv/bin/activate && uvicorn app.main:app --reload

# Frontend
cd frontend && npm run dev

# Docker
docker-compose up --build

# Reset everything
rm -rf backend/compiler.db frontend/node_modules backend/venv
```

---

## ✨ Features Included

✅ 6-stage compilation pipeline
✅ Intent extraction
✅ System design generation
✅ Schema generation
✅ Validation engine
✅ Repair engine
✅ Runtime simulation
✅ Real-time metrics dashboard
✅ API documentation (Swagger UI)
✅ Sample data included
✅ Docker containerization
✅ TypeScript support
✅ Tailwind CSS styling

---

## 🎯 You're All Set!

Start with **Option 1 or 3** above for the quickest setup, then:
1. Open http://localhost:3000
2. Navigate to "Compiler"
3. Fill in your project details
4. Click "Compile"
5. View your generated system design!

**Happy compiling! 🎉**
