import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="AI Application Compiler",
    description="Convert natural language requirements into executable application configs",
    version="1.0.0",
)

# Service version constant used by the health endpoint
SERVICE_NAME = "ai-app-compiler"
SERVICE_VERSION = "1.0.0"

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8080", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.api_route("/", methods=["GET", "HEAD"])
async def root() -> dict[str, str]:
    return {
        "status": "success",
        "message": "AI Application Compiler API Running",
        "docs": "/docs",
    }


@app.get("/health")
async def health() -> dict[str, str]:
    """Production health endpoint suitable for Railway health checks.

    Returns a small JSON payload with service name and version.
    """
    return {
        "status": "healthy",
        "service": SERVICE_NAME,
        "version": SERVICE_VERSION,
    }


@app.get("/api/health")
async def api_health() -> dict[str, str]:
    """Alias health endpoint under /api for platform checks."""
    return {
        "status": "healthy",
        "service": SERVICE_NAME,
        "version": SERVICE_VERSION,
    }

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import routes after app initialization
from app.api import routes as api_routes

# Mount API under both root and /api to support older deployments
# Root: /generate, /validate, etc. (backwards-compatibility)
app.include_router(api_routes.router, tags=["compiler"])

# Also expose under /api prefix: /api/generate, /api/validate, ...
app.include_router(api_routes.router, prefix="/api", tags=["compiler"])
