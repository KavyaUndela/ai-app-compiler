from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any, Dict

from .schemas import PromptRequest


app = FastAPI(title="AI-App-Compiler API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/metrics")
def metrics():
    # Placeholder metrics
    return {"requests": 0, "errors": 0}


@app.post("/generate")
def generate(payload: PromptRequest) -> Dict[str, Any]:
    # Placeholder: run intent extraction -> system design -> schema generation
    return {"status": "ok", "action": "generate", "prompt": payload.prompt}


@app.post("/validate")
def validate(payload: PromptRequest) -> Dict[str, Any]:
    # Placeholder: run validation engine
    return {"status": "ok", "action": "validate", "prompt": payload.prompt}


@app.post("/repair")
def repair(payload: PromptRequest) -> Dict[str, Any]:
    # Placeholder: run repair engine
    return {"status": "ok", "action": "repair", "prompt": payload.prompt}


@app.post("/runtime-preview")
def runtime_preview(payload: PromptRequest) -> Dict[str, Any]:
    # Placeholder: run runtime simulator and return preview
    return {"status": "ok", "action": "runtime-preview", "prompt": payload.prompt}


@app.get("/api/hello")
def hello():
    return {"message": "Hello from backend"}
