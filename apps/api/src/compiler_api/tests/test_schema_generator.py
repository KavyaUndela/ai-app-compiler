"""Tests for the deterministic schema generation service."""

from __future__ import annotations

from compiler_api.services import IntentExtractionService, SchemaGeneratorService, SystemDesignService


def _build_architecture():
    requirement = (
        "Build a production-grade AI Application Compiler for product teams. "
        "Admins and editors should manage application requirements, approve workflows, "
        "and validate generated configurations. The platform must integrate with PostgreSQL, Slack, and email. "
        "Each generated plan must be deterministic, secure, and auditable."
    )
    intent = IntentExtractionService().extract(requirement)
    return SystemDesignService().design(intent)


def test_schema_generator_builds_consistent_schemas() -> None:
    architecture = _build_architecture()
    result = SchemaGeneratorService().generate(architecture)

    assert result.database.database_name == "production_grade_ai_application_compiler_for_product_teams"
    assert result.api.base_path == "/api/v1"
    assert result.ui.application_name == architecture.system_name
    assert result.auth.roles == [role.role for role in architecture.role_hierarchy]

    table_names = {table.name for table in result.database.tables}
    assert {"applications", "roles", "permissions", "role_permissions", "modules", "pages", "workflows", "audit_logs"}.issubset(table_names)

    endpoint_paths = {endpoint.path for endpoint in result.api.endpoints}
    assert "/api/v1/architecture" in endpoint_paths
    assert any(path.startswith("/api/v1/pages/") for path in endpoint_paths)
    assert any(path.startswith("/api/v1/workflows/") for path in endpoint_paths)

    page_routes = {page.route for page in result.ui.pages}
    assert page_routes == {page.route for page in architecture.pages}

    component_names = {component.name for component in result.ui.components}
    assert all(component_name in component_names for page in result.ui.pages for component_name in page.components)


def test_schema_generator_preserves_cross_schema_consistency() -> None:
    architecture = _build_architecture()
    result = SchemaGeneratorService().generate(architecture)

    assert result.auth.roles == [role.role for role in architecture.role_hierarchy]

    page_names = {page.name for page in architecture.pages}
    api_page_endpoints = {endpoint.name for endpoint in result.api.endpoints if endpoint.path.startswith("/api/v1/pages/")}
    assert any(page_name.casefold().replace(" ", "_") in endpoint_name for page_name in page_names for endpoint_name in api_page_endpoints)

    db_table_names = {table.name for table in result.database.tables}
    assert "roles" in db_table_names and "pages" in db_table_names and "workflows" in db_table_names