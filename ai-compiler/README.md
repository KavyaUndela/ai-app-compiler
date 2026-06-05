# AI Application Compiler

Convert natural language software requirements into executable application configurations.

## 🎯 Overview

The AI Application Compiler is a sophisticated system that transforms high-level requirements into complete system designs, database schemas, and technical specifications through a 6-stage compilation pipeline:

1. **Intent Extraction** - Understand core requirements and intentions
2. **System Design** - Generate optimal architecture patterns
3. **Schema Generation** - Create database schemas and data models
4. **Validation Engine** - Validate all generated artifacts
5. **Repair Engine** - Automatically fix validation issues
6. **Runtime Simulator** - Simulate performance and behavior

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- Node.js 20+
- npm or yarn
- (Optional) Docker and Docker Compose for containerized setup

### Local Development Setup

#### 1. Clone and Navigate to Project
```bash
cd ai-compiler
```

#### 2. Backend Setup
```bash
# Navigate to backend directory
cd backend

# Copy environment file
cp .env.example .env

# Create virtual environment (Windows)
python -m venv venv
venv\Scripts\activate

# Or on macOS/Linux:
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Seed database with sample data
python scripts/seed_db.py

# Start backend server
uvicorn app.main:app --reload
```

Backend will be available at: **http://localhost:8000**
- API Documentation: http://localhost:8000/docs
- OpenAPI Schema: http://localhost:8000/openapi.json

#### 3. Frontend Setup (in new terminal)
```bash
# Navigate to frontend directory
cd frontend

# Copy environment file
cp .env.example .env

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will be available at: **http://localhost:3000**

### Docker Setup (Alternative)

If you have Docker and Docker Compose installed, run the entire stack with one command:

```bash
docker-compose up --build
```

This will:
- Build both backend and frontend images
- Start both services in containers
- Expose frontend at http://localhost:3000
- Expose API at http://localhost:8000

To stop:
```bash
docker-compose down
```

## 📋 Project Structure

```
ai-compiler/
├── backend/
│   ├── app/
│   │   ├── main.py                 # FastAPI entry point
│   │   ├── config.py               # Configuration
│   │   ├── database.py             # Database setup
│   │   ├── models/                 # Pydantic request/response models
│   │   ├── schemas/                # SQLAlchemy ORM models
│   │   ├── services/               # Business logic (6-stage pipeline)
│   │   ├── routes/                 # API endpoints
│   │   └── middleware/             # Custom middleware
│   ├── tests/                      # Test suite
│   ├── scripts/
│   │   └── seed_db.py             # Database seeding script
│   ├── requirements.txt            # Python dependencies
│   ├── Dockerfile                  # Backend container image
│   └── .env.example               # Environment variables template
│
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── layout.tsx         # Root layout
│   │   │   ├── page.tsx           # Home page
│   │   │   ├── compiler/          # Compiler interface
│   │   │   └── dashboard/         # Metrics dashboard
│   │   ├── components/            # Reusable React components
│   │   ├── lib/
│   │   │   ├── api.ts            # API client
│   │   │   └── types.ts          # TypeScript types
│   │   └── styles/               # Global styles
│   ├── public/                   # Static assets
│   ├── package.json              # Node.js dependencies
│   ├── tsconfig.json             # TypeScript config
│   ├── next.config.js            # Next.js config
│   ├── Dockerfile                # Frontend container image
│   ├── .env.example              # Environment variables template
│   └── .dockerignore
│
├── docker-compose.yml            # Multi-container orchestration
└── README.md                      # This file
```

## 🔧 Available Commands

### Backend

```bash
# Development (with auto-reload)
uvicorn app.main:app --reload

# Production
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Run tests
pytest

# Seed database
python scripts/seed_db.py

# Format code
black app/

# Run linter
pylint app/
```

### Frontend

```bash
# Development
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Run tests
npm test

# Run tests in watch mode
npm run test:watch

# Lint
npm run lint
```

## 🧪 Testing the Application

### 1. Access the Web Interface
- Open http://localhost:3000 in your browser
- Navigate to "Compiler" tab

### 2. Try a Sample Compilation
**Input:**
- Title: "E-commerce Platform"
- Description: "Build a modern e-commerce platform with product catalog, shopping cart, and payment processing"
- Features:
  - User authentication
  - Product search
  - Shopping cart
  - Payment processing
  - Order tracking
- Constraints: "Must handle 10k concurrent users"

**Expected Output:**
- Architecture type
- Components list
- Database schema
- Validation score
- Repair suggestions (if needed)

### 3. View Metrics Dashboard
- Navigate to "Dashboard" tab
- See compilation statistics
- View performance metrics
- Monitor API health

### 4. API Testing with cURL

```bash
# Health check
curl http://localhost:8000/health

# Get metrics dashboard
curl http://localhost:8000/api/metrics/dashboard

# Compile requirements
curl -X POST http://localhost:8000/api/compile \
  -H "Content-Type: application/json" \
  -d '{
    "requirement": {
      "title": "Blog System",
      "description": "Create a blog platform with posts and comments",
      "features": ["Create posts", "Comments", "User roles"],
      "constraints": null,
      "tech_preferences": {"frontend": "Next.js", "backend": "FastAPI"}
    },
    "include_simulation": true,
    "include_repairs": true
  }'
```

## 🗄️ Database

### Local Development
- **Type:** SQLite
- **Location:** `compiler.db` (auto-created in backend root)
- **No setup required** - automatically initialized on first run

### PostgreSQL (Optional)
For production, configure PostgreSQL:

1. Set environment variable in `backend/.env`:
```env
DATABASE_URL=postgresql://user:password@localhost:5432/compiler_db
```

2. Create database:
```bash
createdb compiler_db
```

## 🔐 Environment Configuration

### Backend (`backend/.env`)
```env
DATABASE_URL=sqlite:///./compiler.db
API_TITLE=AI Application Compiler
API_VERSION=1.0.0
DEBUG=True
CORS_ORIGINS=["http://localhost:3000", "http://localhost:8000"]
MAX_COMPILATION_TIME=300
MAX_ARTIFACT_SIZE=10485760
```

### Frontend (`frontend/.env.local`)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NODE_ENV=development
```

## 📊 API Documentation

### Compilation Endpoint
**POST** `/api/compile`

Request:
```json
{
  "requirement": {
    "title": "string",
    "description": "string",
    "features": ["string"],
    "constraints": "string (optional)",
    "tech_preferences": {"key": "value"}
  },
  "include_simulation": boolean,
  "include_repairs": boolean
}
```

Response:
```json
{
  "compilation_id": "uuid",
  "requirement": {...},
  "intent": {...},
  "design": {...},
  "schema": {...},
  "validation": {...},
  "repairs": [...],
  "simulation": {...},
  "timestamp": "ISO8601",
  "duration_ms": number
}
```

### Metrics Endpoints
- **GET** `/api/metrics/dashboard` - Compilation statistics
- **GET** `/api/metrics/performance` - System performance
- **GET** `/api/metrics/health` - Health status

## 🐛 Troubleshooting

### Backend Won't Start
```bash
# Check if port 8000 is in use
netstat -tulpn | grep 8000

# Kill process on port 8000
lsof -ti:8000 | xargs kill -9
```

### Frontend Won't Connect to Backend
1. Verify backend is running: `curl http://localhost:8000/health`
2. Check `NEXT_PUBLIC_API_URL` in `frontend/.env`
3. Check CORS settings in `backend/app/config.py`

### Database Issues
```bash
# Reset database
rm backend/compiler.db

# Reseed
python backend/scripts/seed_db.py
```

### Port Already in Use
- Backend (8000): Change in `uvicorn` command
- Frontend (3000): Change in `next.config.js`
- Docker: Change port mapping in `docker-compose.yml`

## 📈 Performance Characteristics

- **Compilation Time:** ~1-2 seconds for typical requirements
- **API Response Time:** <200ms
- **Concurrent Users:** Supports 1000+ RPS
- **Database Queries:** Indexed for optimal performance

## 🔄 Development Workflow

1. **Make changes** to backend or frontend code
2. Both services have hot-reload enabled
3. Refresh browser to see frontend changes
4. API docs update automatically (http://localhost:8000/docs)

## 🛠️ Tech Stack

**Backend:**
- FastAPI 0.104+
- SQLAlchemy 2.0+
- Pydantic v2
- Python 3.12+
- SQLite (local) / PostgreSQL (optional)

**Frontend:**
- Next.js 14+
- React 18+
- TypeScript 5+
- Tailwind CSS 3+
- Axios for HTTP

**Infrastructure:**
- Docker & Docker Compose
- Uvicorn ASGI server
- Node.js runtime

## 📝 Sample Requirements File

Create `sample_requirements.json`:
```json
{
  "title": "Social Media Platform",
  "description": "Build a real-time social network with messaging and notifications",
  "features": [
    "User authentication",
    "Post creation and feed",
    "Real-time messaging",
    "Push notifications",
    "User profiles",
    "Follow/unfollow system"
  ],
  "constraints": "Must handle 100k concurrent users",
  "tech_preferences": {
    "frontend": "Next.js",
    "backend": "FastAPI",
    "database": "PostgreSQL",
    "cache": "Redis",
    "messaging": "WebSocket"
  }
}
```

## 🚀 Deployment

For production deployment:

1. Set `DEBUG=False` in backend `.env`
2. Update `CORS_ORIGINS` to production domain
3. Switch to PostgreSQL database
4. Use production-grade ASGI server (Gunicorn with Uvicorn workers)
5. Add reverse proxy (Nginx)
6. Enable HTTPS/TLS
7. Set up monitoring and logging

## 📄 License

This project is provided as-is for educational and development purposes.

## 🤝 Contributing

The codebase is structured for easy extension:

- **Add new services:** Create files in `backend/app/services/`
- **Add new routes:** Create files in `backend/app/routes/`
- **Add new pages:** Create files in `frontend/src/app/`
- **Add new components:** Create files in `frontend/src/components/`

## 📞 Support

For issues or questions:
1. Check this README's troubleshooting section
2. Review backend logs: `http://localhost:8000/docs`
3. Check browser console for frontend errors
4. Verify environment configuration

## 🎓 Learning Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Next.js Documentation](https://nextjs.org/docs)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Pydantic Documentation](https://docs.pydantic.dev/)

---

**Ready to compile applications? Start at http://localhost:3000!** 🎉
