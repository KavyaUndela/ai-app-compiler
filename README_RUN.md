Run instructions for AI Compiler (local dev)

Prereqs:
- Docker & Docker Compose
- Node.js (18+)
- Python 3.12

1) Start infra (Postgres + Redis + pgAdmin)

```bash
cd infra/docker
docker compose up -d
```

2) Backend

```bash
cd apps/api
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn compiler_api.core.app:app --reload --host 0.0.0.0 --port 8000
```

3) Frontend

```bash
cd web
npm install
npm run dev
# open http://localhost:3000
```

Environment variables
- Use `.env` files for DB URLs, Redis URL, and JWT secrets. Example in `apps/api`:

```
DATABASE_URL=postgresql+asyncpg://dev:dev@localhost:5432/ai_compiler
REDIS_URL=redis://localhost:6379/0
```

Notes
- The UI scaffold requires Tailwind CSS; `npm install` will install it and build CSS.
- If you want, I can run these commands here (install, start infra). Otherwise run them locally in your terminal.
