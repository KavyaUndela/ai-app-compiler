import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="AI Application Compiler",
    description="Convert natural language requirements into executable application configs",
    version="1.0.0",
)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8080", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
