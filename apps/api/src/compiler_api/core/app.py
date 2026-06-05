"""FastAPI application factory for the compiler API."""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from compiler_api.routes.runtime import router as runtime_router
from compiler_api.routes.auth import router as auth_router


def create_app() -> FastAPI:
    app = FastAPI(title="AI Application Compiler", version="1.0.0")
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    app.include_router(runtime_router)
    app.include_router(auth_router)

    @app.get("/")
    async def root() -> dict[str, str]:
        return {
            "status": "success",
            "message": "AI Application Compiler API Running",
            "docs": "/docs"
        }

    return app


app = create_app()