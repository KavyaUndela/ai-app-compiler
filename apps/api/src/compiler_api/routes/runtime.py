"""Runtime preview route."""

from __future__ import annotations

from fastapi import APIRouter

from compiler_api.schemas.runtime import RuntimePreview, RuntimePreviewRequest
from compiler_api.services import RuntimeSimulatorService


router = APIRouter(tags=["runtime"])


@router.post("/runtime-preview", response_model=RuntimePreview)
def runtime_preview(request: RuntimePreviewRequest) -> RuntimePreview:
    return RuntimeSimulatorService().simulate(request.to_generated_schemas())