"""Tests for the deterministic intent extraction service."""

from __future__ import annotations

import pytest

from compiler_api.services import IntentExtractionService


def test_extracts_compiler_intent_from_requirement_text() -> None:
    requirement = (
        "Build a production-grade AI Application Compiler for product teams. "
        "Admins and editors should manage application requirements, approve workflows, "
        "and validate generated configurations. The platform must integrate with PostgreSQL, Slack, and email. "
        "Each generated plan must be deterministic, secure, and auditable."
    )

    service = IntentExtractionService()
    intent = service.extract(requirement)

    assert intent.application_name == "Production Grade Ai Application Compiler For Product Teams"
    assert "Admin" in intent.roles
    assert "Editor" in intent.roles
    assert any(entity in intent.entities for entity in ("Application", "Compiler", "Postgresql", "Slack", "Email"))
    assert any("Approve" in permission for permission in intent.permissions)
    assert any("must be deterministic" in rule.casefold() for rule in intent.business_rules)
    assert intent.workflows
    assert set(intent.integrations) == {"Postgresql", "Slack", "Email"}
    assert intent.target_users == intent.roles


def test_extract_is_deterministic_for_same_input() -> None:
    requirement = (
        "Create a customer support portal where managers can approve tickets and users can submit requests. "
        "The system should integrate with Salesforce and Slack and must enforce role-based access control."
    )

    service = IntentExtractionService()
    first = service.extract(requirement)
    second = service.extract(requirement)

    assert first == second


def test_rejects_too_short_requirement_text() -> None:
    service = IntentExtractionService()

    with pytest.raises(ValueError):
        service.extract("too short")