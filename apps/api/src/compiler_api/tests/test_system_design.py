"""Tests for the deterministic system design service."""

from __future__ import annotations

from compiler_api.services import IntentExtractionService, SystemDesignService


def test_design_service_converts_intent_to_architecture() -> None:
    requirement = (
        "Build a production-grade AI Application Compiler for product teams. "
        "Admins and editors should manage application requirements, approve workflows, "
        "and validate generated configurations. The platform must integrate with PostgreSQL, Slack, and email. "
        "Each generated plan must be deterministic, secure, and auditable."
    )

    intent = IntentExtractionService().extract(requirement)
    architecture = SystemDesignService().design(intent)

    assert architecture.system_name == intent.application_name
    assert architecture.layers
    assert architecture.modules
    assert architecture.pages
    assert architecture.navigation
    assert architecture.workflows
    assert architecture.role_hierarchy
    assert any(module.name == "system-designer" for module in architecture.modules)
    assert any(page.route == "/validation" for page in architecture.pages)
    assert any(node.target_page == "Architecture" for node in architecture.navigation)
    assert any(workflow.name == "Requirement To Architecture" for workflow in architecture.workflows)
    assert {role.role for role in architecture.role_hierarchy} >= {"Admin", "Editor"}


def test_design_service_is_deterministic() -> None:
    requirement = (
        "Create a customer support portal where managers can approve tickets and users can submit requests. "
        "The system should integrate with Salesforce and Slack and must enforce role-based access control."
    )

    intent = IntentExtractionService().extract(requirement)
    service = SystemDesignService()

    first = service.design(intent)
    second = service.design(intent)

    assert first == second