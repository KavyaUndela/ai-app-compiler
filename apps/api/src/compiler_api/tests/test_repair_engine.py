"""Tests for the deterministic repair engine."""

from __future__ import annotations

from datetime import datetime, timezone

from compiler_api.services import IntentExtractionService, RepairEngine, SchemaGeneratorService, SystemDesignService
from compiler_contracts import IssueSeverity, ValidationIssueSchema, ValidationReport


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


def test_repair_engine_repairs_targeted_sections_and_reruns_validation() -> None:
    bundle = _build_generated_bundle()

    endpoints = list(bundle.api.endpoints)
    endpoints[2] = endpoints[2].model_copy(update={"response_schema": "BrokenResponse"})
    object.__setattr__(bundle.api, "endpoints", endpoints)

    pages = list(bundle.ui.pages)
    pages[1] = pages[1].model_copy(update={"components": []})
    object.__setattr__(bundle.ui, "pages", pages)

    object.__setattr__(bundle.auth, "default_role", "Ghost")

    report = ValidationReport(
        passed=False,
        generated_at=datetime.now(timezone.utc),
        issues=[
            ValidationIssueSchema(
                code="API_DB_MISMATCH",
                message="Validation endpoint response schema does not match generated artifacts.",
                severity=IssueSeverity.ERROR,
                path=["api", "endpoints", "validate_schema", "response_schema"],
                suggested_fix="Restore the deterministic validation response schema.",
            ),
            ValidationIssueSchema(
                code="UI_API_MISMATCH",
                message="Requirements page has lost its component mapping.",
                severity=IssueSeverity.ERROR,
                path=["ui", "pages", "Requirements", "components"],
                suggested_fix="Restore the page component list.",
            ),
            ValidationIssueSchema(
                code="INVALID_PERMISSION",
                message="Default role is invalid.",
                severity=IssueSeverity.ERROR,
                path=["auth", "default_role"],
                suggested_fix="Set the default role to the first available role.",
            ),
        ],
        summary="Synthetic validation failure for repair testing.",
        deterministic_fingerprint="2" * 64,
    )

    repair_report = RepairEngine().repair(bundle, report)

    assert repair_report.original_report == report
    assert repair_report.succeeded is True
    assert repair_report.remaining_issues == []
    assert len(repair_report.repair_actions) == 3
    assert bundle.database == _build_generated_bundle().database
    assert bundle.api.endpoints[2].response_schema == "ValidationReportResponse"
    assert bundle.ui.pages[1].components
    assert bundle.auth.default_role == bundle.auth.roles[0]


def test_repair_engine_repairs_invalid_relationships_only() -> None:
    bundle = _build_generated_bundle()

    tables = list(bundle.database.tables)
    role_permissions = tables[3]
    foreign_keys = list(role_permissions.foreign_keys)
    foreign_keys[0] = foreign_keys[0].model_copy(update={"referenced_table": "missing_table"})
    tables[3] = role_permissions.model_copy(update={"foreign_keys": foreign_keys})
    object.__setattr__(bundle.database, "tables", tables)

    report = ValidationReport(
        passed=False,
        generated_at=datetime.now(timezone.utc),
        issues=[
            ValidationIssueSchema(
                code="INVALID_RELATIONSHIP",
                message="Role permissions table contains an invalid foreign key.",
                severity=IssueSeverity.ERROR,
                path=["database", "tables", "role_permissions", "foreign_keys"],
                suggested_fix="Remove the invalid foreign key while preserving the valid relation.",
            )
        ],
        summary="Synthetic relationship failure for repair testing.",
        deterministic_fingerprint="3" * 64,
    )

    repair_report = RepairEngine().repair(bundle, report)

    assert repair_report.succeeded is True
    assert repair_report.remaining_issues == []
    assert len(repair_report.repair_actions) == 1
    assert all(foreign_key.referenced_table != "missing_table" for foreign_key in bundle.database.tables[3].foreign_keys)
    assert any(foreign_key.referenced_table == "permissions" for foreign_key in bundle.database.tables[3].foreign_keys)


def test_repair_engine_preserves_unrepairable_invalid_json_issue() -> None:
    bundle = _build_generated_bundle()

    report = ValidationReport(
        passed=False,
        generated_at=datetime.now(timezone.utc),
        issues=[
            ValidationIssueSchema(
                code="INVALID_JSON",
                message="One generated payload could not be parsed as JSON.",
                severity=IssueSeverity.ERROR,
                path=["api", "endpoints", "validation"],
                suggested_fix="Repair the upstream serializer.",
            )
        ],
        summary="Synthetic JSON failure for repair testing.",
        deterministic_fingerprint="4" * 64,
    )

    repair_report = RepairEngine().repair(bundle, report)

    assert repair_report.succeeded is False
    assert repair_report.remaining_issues and repair_report.remaining_issues[0].code == "INVALID_JSON"
    assert repair_report.repair_actions[0].step_name == "record_invalid_json"