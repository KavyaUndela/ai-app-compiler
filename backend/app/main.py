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

# Configure logging before any other setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Enable CORS for frontend - permissive for development, can be restricted for production
cors_origins = [
    "http://localhost:3000",
    "http://localhost:8080",
    "http://localhost:8000",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8080",
    # Add production URLs here
    # "https://yourdomain.com",
]

# Add wildcard for development only (remove in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins + ["*"],  # Wildcard for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.info(f"CORS enabled for origins: {cors_origins}")

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

# Import routes after app initialization
from app.api import routes as api_routes

# Log endpoint registration
logger.info("Registering API routes...")

# Mount API under both root and /api to support older deployments
# Root: /generate, /validate, etc. (backwards-compatibility)
app.include_router(api_routes.router, tags=["compiler"])
logger.info("Routes registered at root level: /generate, /validate, /repair, /runtime-preview")

# Also expose under /api prefix: /api/generate, /api/validate, ...
app.include_router(api_routes.router, prefix="/api", tags=["compiler"])
logger.info("Routes registered under /api prefix: /api/generate, /api/validate, /api/repair, /api/runtime-preview")

logger.info("API initialization complete")
