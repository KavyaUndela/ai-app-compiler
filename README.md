# AI Application Compiler

A local-first compiler-style AI system that converts natural language software requirements into executable application configurations.

## What it does

Pipeline:

Natural Language Prompt -> Intent Extraction -> System Design -> Schema Generation -> Validation Engine -> Repair Engine -> Runtime Simulator -> Executable Configuration

## Tech Stack

- Frontend: Next.js 15, TypeScript, Tailwind CSS, React Query
- Backend: FastAPI, Python 3.12
- Validation: Pydantic v2
- Local database: SQLite-friendly design, PostgreSQL-ready
- AI: Mock LLM service with Claude integration interface
- Deployment: Docker

## Project Structure

```text
ai-app-compiler/
  backend/
    app/
      api/
      services/
      models.py
      main.py
    requirements.txt
    Dockerfile
  frontend/
    src/
      app/
      components/
      pages/
      services/
      store/
      stores/
      styles/
      types/
    package.json
    Dockerfile
  docker-compose.yml
  docs/
  README.md
```

## Features

### Stage 1: Intent Extraction
Extracts entities, features, roles, permissions, and workflows from a natural language prompt.

### Stage 2: System Design
Converts intent into architecture, modules, pages, navigation, and user flows.

### Stage 3: Schema Generation
Generates:
- Database Schema
- API Schema
- UI Schema
- Auth Schema

### Stage 4: Validation Engine
Validates:
- JSON correctness
- Missing fields
- API-DB mismatch
- UI-API mismatch
- Role conflicts
- Relationship conflicts

### Stage 5: Repair Engine
Repairs only invalid sections and produces repair logs.

### Stage 6: Runtime Simulator
Generates dynamic forms, CRUD pages, and runtime preview output.

## Localhost URLs

- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API docs: http://localhost:8000/docs
- Health: http://localhost:8000/health

## Backend Setup

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

## Docker Setup

```bash
docker compose up --build
```

## API Endpoints

### POST /generate
Runs the full compiler pipeline.

Request:

```json
{
  "prompt": "Build a CRM with login, contacts, dashboard, role-based access, premium plans and payments."
}
```

### POST /validate
Validates a generated schema.

### POST /repair
Repairs invalid sections using validation output.

### POST /runtime-preview
Generates runtime preview data from a schema.

### GET /health
Returns backend health status.

## Sample Prompts

- CRM
- Hospital Management
- School ERP
- Inventory System

## Testing

Backend:

```bash
cd backend
pytest
```

Frontend build:

```bash
cd frontend
npm run build
```

## Notes

- The frontend uses `NEXT_PUBLIC_API_URL` and defaults to `http://localhost:8000`.
- The backend is designed to run locally without manual coding changes.
- Docker Compose exposes the requested local ports directly.
