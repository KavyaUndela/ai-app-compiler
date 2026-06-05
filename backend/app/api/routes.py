"""
Root compiler API routes.
"""

from __future__ import annotations

import uuid
from copy import deepcopy
from typing import Dict

from pydantic import BaseModel, ConfigDict, Field
from fastapi import APIRouter, HTTPException

from app.models import (
    CompilationResult,
    GenerateRequest,
    IntentSchema,
    RuntimePreview,
    SchemaGenerationResult,
    SystemDesignSchema,
    ValidationResult,
    RepairResult,
)
from fastapi import status
from app.services.intent_extraction import extract_intent
from app.services.system_design import generate_design
from app.services.schema_generator import generate_schema
from app.services.validation_engine import validate_schema
from app.services.repair_engine import repair_schema
from app.services.runtime_simulator import generate_runtime_preview

router = APIRouter()

compilations_store: Dict[str, CompilationResult] = {}
metrics_store = {
    "generations": 0,
    "validations": 0,
    "repairs": 0,
    "runtime_previews": 0,
}


class RepairRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    validation: ValidationResult = Field(...)
    schema_payload: SchemaGenerationResult = Field(..., alias="schema")


class RuntimePreviewRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    schema_payload: SchemaGenerationResult = Field(..., alias="schema")


class MetricsResponse(BaseModel):
    compilations: int
    generations: int
    validations: int
    repairs: int
    runtime_previews: int


def _compile(prompt: str) -> CompilationResult:
    intent: IntentSchema = extract_intent(prompt)
    design: SystemDesignSchema = generate_design(intent)
    schema: SchemaGenerationResult = generate_schema(design)
    validation: ValidationResult = validate_schema(schema)

    repair: RepairResult | None = None
    if not validation.is_valid:
        repair = repair_schema(validation, schema)

    runtime_preview: RuntimePreview = generate_runtime_preview(schema)

    status = "completed" if validation.is_valid else "partial"
    summary = (
        f"Compiled prompt into {len(design.modules)} modules, "
        f"{len(schema.database_schema)} tables and {len(schema.api_schema)} endpoints."
    )

    return CompilationResult(
        compilation_id=str(uuid.uuid4()),
        original_prompt=prompt,
        intent=intent,
        design=design,
        schema=schema,
        validation=validation,
        repair=repair,
        runtime_preview=runtime_preview,
        status=status,
        summary=summary,
    )


@router.get("/health")
def health() -> dict:
    return {"status": "healthy", "service": "ai-application-compiler", "version": "1.0.0"}


@router.post("/generate", response_model=CompilationResult)
def generate_configuration(request: GenerateRequest) -> CompilationResult:
    try:
        result = _compile(request.prompt)
        compilations_store[result.compilation_id] = result
        metrics_store["generations"] += 1
        metrics_store["validations"] += 1
        metrics_store["runtime_previews"] += 1
        if result.repair and result.repair.patches:
            metrics_store["repairs"] += 1
        return result
    except Exception as exc:  # pragma: no cover - route guard
        raise HTTPException(status_code=500, detail=f"Compilation failed: {exc}") from exc


@router.post("/validate", response_model=ValidationResult)
def validate_configuration(schema: SchemaGenerationResult) -> ValidationResult:
    try:
        metrics_store["validations"] += 1
        return validate_schema(schema)
    except Exception as exc:  # pragma: no cover - route guard
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/repair", response_model=RepairResult)
def repair_configuration(payload: RepairRequest) -> RepairResult:
    try:
        metrics_store["repairs"] += 1
        return repair_schema(payload.validation, payload.schema_payload)
    except Exception as exc:  # pragma: no cover - route guard
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/runtime-preview", response_model=RuntimePreview)
def runtime_preview(payload: RuntimePreviewRequest) -> RuntimePreview:
    try:
        metrics_store["runtime_previews"] += 1
        return generate_runtime_preview(payload.schema_payload)
    except Exception as exc:  # pragma: no cover - route guard
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/metrics", response_model=MetricsResponse)
def metrics() -> MetricsResponse:
    return MetricsResponse(
        compilations=len(compilations_store),
        generations=metrics_store["generations"],
        validations=metrics_store["validations"],
        repairs=metrics_store["repairs"],
        runtime_previews=metrics_store["runtime_previews"],
    )


@router.get("/compilations/{compilation_id}", response_model=CompilationResult)
def get_compilation(compilation_id: str) -> CompilationResult:
    if compilation_id not in compilations_store:
        raise HTTPException(status_code=404, detail="Compilation not found")
    return compilations_store[compilation_id]


@router.get("/compilations")
def list_compilations(limit: int = 10) -> dict:
    items = list(compilations_store.values())[-limit:]
    return {
        "total": len(compilations_store),
        "items": [
            {
                "compilation_id": item.compilation_id,
                "prompt": item.original_prompt[:100],
                "status": item.status,
                "modules": len(item.design.modules),
                "endpoints": len(item.schema.api_schema),
            }
            for item in items
        ],
    }


# --- Minimal auth endpoints to satisfy frontend during local development ---
class SignupRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    name: str
    email: str
    password: str


class SigninRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    email: str
    password: str


@router.post("/auth/signup", status_code=status.HTTP_201_CREATED)
def signup(payload: SignupRequest) -> dict:
    # NOTE: This is a lightweight stub for local development only.
    # In production this should create a user, hash the password,
    # and return an auth token.
    user = {"name": payload.name, "email": payload.email}
    return {"user": user, "token": "dev-token"}


@router.post("/auth/signin")
def signin(payload: SigninRequest) -> dict:
    # Lightweight stub: always succeed and return a fake token.
    # For demo: echo back a user object and token expected by frontend
    user = {"name": "Demo User", "email": payload.email}
    return {"user": user, "token": "dev-token"}


@router.get("/auth/me")
def me(token: str = None) -> dict:
    # Very small demo: accept the hard-coded dev-token and return a user
    if token != "dev-token":
        raise HTTPException(status_code=401, detail="Invalid token")
    return {"user": {"name": "Demo User", "email": "test@example.com"}}
