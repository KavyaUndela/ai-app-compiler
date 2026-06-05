# AI Compiler - Startup Guide

## Prerequisites

Before running the project, ensure you have:

- **Docker Desktop** (with Docker Compose) — [Install](https://www.docker.com/products/docker-desktop)
- **Node.js 18+** — [Install](https://nodejs.org/)
- **Python 3.12** — [Install](https://www.python.org/)
- **Git** — [Install](https://git-scm.com/)

Verify installations:
```bash
docker --version
docker compose version
node --version
python --version
```

## One-Command Startup

### Windows (PowerShell or Command Prompt)

From repository root:

```powershell
.\start-stack.bat
```

This will:
1. Start Postgres, Redis, pgAdmin via Docker Compose
2. Create Python venv and install backend deps
3. Create `.env` from `.env.example`
4. Start FastAPI dev server (port 8000)
5. Install frontend deps and start Next.js (port 3000)

### macOS / Linux (Bash)

From repository root:

```bash
chmod +x start-stack.sh
./start-stack.sh
```

Same steps as Windows script.

## Manual Startup (if automated script fails)

### 1. Start Infrastructure

```bash
cd infra/docker
docker compose up -d
```

Check services:
```bash
docker compose ps
```

### 2. Backend Setup & Run

**Windows PowerShell:**
```powershell
cd apps/api
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
# Copy .env.example to .env and edit
copy .env.example .env
uvicorn compiler_api.core.app:app --reload --host 0.0.0.0 --port 8000
```

**macOS / Linux:**
```bash
cd apps/api
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
uvicorn compiler_api.core.app:app --reload --host 0.0.0.0 --port 8000
```

### 3. Frontend Setup & Run

**Any OS (new terminal):**
```bash
cd web
npm install
npm run dev
```

### 4. Optional: Background Workers

**Windows PowerShell (new terminal):**
```powershell
cd apps/api
.venv\Scripts\Activate.ps1
celery -A compiler_api.workers worker --loglevel=info
```

**macOS / Linux (new terminal):**
```bash
cd apps/api
source .venv/bin/activate
celery -A compiler_api.workers worker --loglevel=info
```

## Service URLs

Once running:

| Service  | URL                       | Notes                     |
|----------|---------------------------|---------------------------|
| Frontend | http://localhost:3000     | Next.js UI dashboard      |
| Backend  | http://localhost:8000     | FastAPI with Swagger UI   |
| pgAdmin  | http://localhost:8080     | Postgres admin panel      |
| Postgres | localhost:5432            | DB connection only        |
| Redis    | localhost:6379            | Cache/queue only          |

## Environment Variables

Create `apps/api/.env` (copy from `.env.example`):

```
DATABASE_URL=postgresql+asyncpg://dev:dev@localhost:5432/ai_compiler
REDIS_URL=redis://localhost:6379/0
JWT_SECRET=change-me-in-production
LOG_LEVEL=info
```

## Troubleshooting

### Docker command not found
- Install Docker Desktop: https://www.docker.com/products/docker-desktop
- Restart terminal/IDE after installation

### pip install fails (network error)
- Check internet connection
- Verify PyPI access: `pip index versions pip`
- If behind proxy, configure pip: `pip config set global.proxy [user:passwd@]proxy.server:port`
- Use offline cache or internal registry if available

### npm install fails
- Clear npm cache: `npm cache clean --force`
- Delete `node_modules` and `package-lock.json`, then retry

### Port already in use
- Backend (8000): `netstat -ano | findstr :8000` (Windows) or `lsof -i :8000` (Mac/Linux)
- Frontend (3000): Similar commands for port 3000
- Change ports in uvicorn/Next.js commands if needed

### Database connection refused
- Ensure Docker containers are running: `docker compose ps`
- Check logs: `docker compose logs postgres`
- Wait 15s for Postgres to initialize

### Backend won't start (ImportError)
- Ensure `.venv` is activated
- Try reinstalling: `pip install -r requirements.txt --force-reinstall`
- Check PYTHONPATH includes `apps/api/src`

## Development Workflow

1. **Terminal 1** (stays running): Backend
   ```powershell
   cd apps/api && .venv\Scripts\Activate.ps1 && uvicorn compiler_api.core.app:app --reload
   ```

2. **Terminal 2** (stays running): Frontend
   ```bash
   cd web && npm run dev
   ```

3. **Terminal 3** (optional): Workers
   ```powershell
   cd apps/api && .venv\Scripts\Activate.ps1 && celery -A compiler_api.workers worker
   ```

4. **Browser**: Open http://localhost:3000

## Stopping the Stack

From each terminal, press `Ctrl+C` to stop services.

To stop Docker containers:
```bash
cd infra/docker
docker compose down
```

To remove all data (database, volumes):
```bash
cd infra/docker
docker compose down -v
```

## Next Steps

- Explore the UI at http://localhost:3000
- Check backend API docs: http://localhost:8000/docs (Swagger UI)
- Review code in `apps/api/src` and `web/src`
- Run tests: `pytest` in `apps/api` or `npm test` in `web`

## Support

For issues:
1. Check logs in running terminals
2. Check Docker logs: `docker compose logs -f`
3. Review error messages in browser console (F12)
4. Verify all prerequisites are installed
