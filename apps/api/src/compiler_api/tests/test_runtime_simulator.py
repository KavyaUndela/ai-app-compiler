"""Tests for the deterministic runtime simulator and runtime preview route."""

from __future__ import annotations

from compiler_api.routes.runtime import runtime_preview
from compiler_api.schemas.runtime import RuntimePreviewRequest
from compiler_api.services import IntentExtractionService, RuntimeSimulatorService, SchemaGeneratorService, SystemDesignService


def _build_generated_bundle():
    requirement = (
        "Build a production-grade AI Application Compiler for product teams. "
        "Admins and editors should manage application requirements, approve workflows, "
        "and validate generated configurations. The platform must integrate with PostgreSQL, Slack, and email. "
        "Each generated plan must be deterministic, secure, and auditable."
    )
    intent = IntentExtractionService().extract(requirement)
    architecture = SystemDesignService().design(intent)
    return SchemaGeneratorService().generate(architecture)


def test_runtime_simulator_generates_forms_crud_navigation_and_previews() -> None:
    bundle = _build_generated_bundle()
    preview = RuntimeSimulatorService().simulate(bundle)

    assert preview.forms
    assert preview.crud_pages
    assert preview.navigation
    assert preview.runtime_previews
    assert any(form.table_name == "applications" for form in preview.forms)
    assert any(page.table_name == "roles" for page in preview.crud_pages)
    assert any(item.kind == "ui-page" for item in preview.navigation)
    assert any(card.preview_kind == "crud-page" for card in preview.runtime_previews)


def test_runtime_simulator_is_deterministic() -> None:
    bundle = _build_generated_bundle()
    service = RuntimeSimulatorService()

    first = service.simulate(bundle)
    second = service.simulate(bundle)

    assert first == second


def test_runtime_preview_route_returns_preview_payload() -> None:
    bundle = _build_generated_bundle()
    request = RuntimePreviewRequest(
        database=bundle.database,
        api=bundle.api,
        ui=bundle.ui,
        auth=bundle.auth,
    )

    payload = runtime_preview(request)

    assert payload.forms
    assert payload.crud_pages
    assert payload.navigation
    assert payload.runtime_previews