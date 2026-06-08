AI-App-Compiler

Minimal scaffold for the AI-App-Compiler project.

Structure is a lightweight starting point for frontend (Next.js) and backend (FastAPI).

See folders:
- `frontend/` — Next.js app directory
- `backend/` — FastAPI API
- `docker/` — Dockerfiles
- `docker-compose.yml` — local compose config

Run locally:

1. Backend (Python):
```powershell
cd backend
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

2. Frontend (Next.js):
```bash
cd frontend
npm install
npm run dev
```

Railway deployment (suggested)

```
AI-App-Compiler
│
├── frontend/      → Railway Service 1
│
├── backend/       → Railway Service 2
│
└── PostgreSQL     → Railway Database
```

Main API Endpoints

```
POST /generate
POST /validate
POST /repair
POST /runtime-preview
GET  /metrics
GET  /health
```

Core Pipeline

```
User Prompt
	↓
Intent Extraction
	↓
System Design
	↓
Schema Generation
	↓
Validation Engine
	↓
Repair Engine
	↓
Runtime Simulator
	↓
Final Executable Configuration
```

