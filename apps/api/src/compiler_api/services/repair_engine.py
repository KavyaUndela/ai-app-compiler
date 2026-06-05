"""Deterministic repair engine for generated compiler artifacts."""

from __future__ import annotations

from datetime import datetime, timezone
from hashlib import sha256
import json

from compiler_contracts import (
    APISchema,
    DatabaseSchema,
    IssueSeverity,
    RepairActionSchema,
    RepairReport,
    UISchema,
    ValidationIssueSchema,
    ValidationReport,
)
from compiler_contracts.base import set_field_value

from .repair_engine_patterns import normalize_list, pascal_case, schema_identifier, slugify
from .schema_generator import GeneratedSchemas


class RepairEngine:
    """Repair only invalid sections, preserve valid sections, and rerun validation."""

    def repair(self, generated: GeneratedSchemas, validation_report: ValidationReport) -> RepairReport:
        actions: list[RepairActionSchema] = []
        unresolved: list[ValidationIssueSchema] = []

        for issue in validation_report.issues:
            action, resolved = self._apply_issue(generated, issue)
            actions.append(action)
            if not resolved:
                unresolved.append(issue)

        rerun_issues = self._validate_bundle(generated)
        remaining_issues = self._merge_issues(rerun_issues, unresolved)
        succeeded = not remaining_issues

        return RepairReport(
            succeeded=succeeded,
            generated_at=datetime.now(timezone.utc),
            original_report=validation_report,
            repair_actions=actions,
            remaining_issues=remaining_issues,
            deterministic_fingerprint=self._fingerprint(generated, validation_report, actions, remaining_issues),
        )

    def _apply_issue(self, generated: GeneratedSchemas, issue: ValidationIssueSchema) -> tuple[RepairActionSchema, bool]:
        if issue.code == "INVALID_JSON":
            return (
                RepairActionSchema(
                    step_name="record_invalid_json",
                    rationale="Invalid JSON cannot be repaired in-place from a typed schema bundle.",
                    changes_applied=[],
                    affected_paths=[self._path_text(issue.path)],
                ),
                False,
            )

        if issue.code == "MISSING_FIELD":
            return self._repair_missing_field(generated, issue)
        if issue.code == "API_DB_MISMATCH":
            return self._repair_api_db_mismatch(generated, issue)
        if issue.code == "UI_API_MISMATCH":
            return self._repair_ui_api_mismatch(generated, issue)
        if issue.code == "INVALID_RELATIONSHIP":
            return self._repair_invalid_relationship(generated, issue)
        if issue.code == "INVALID_PERMISSION":
            return self._repair_invalid_permission(generated, issue)

        return (
            RepairActionSchema(
                step_name=f"log_{issue.code.lower()}",
                rationale="No deterministic repair rule was available for this issue.",
                changes_applied=[],
                affected_paths=[self._path_text(issue.path)],
            ),
            False,
        )

    def _repair_missing_field(self, generated: GeneratedSchemas, issue: ValidationIssueSchema) -> tuple[RepairActionSchema, bool]:
        if issue.path == ["auth", "default_role"] and generated.auth.roles:
            set_field_value(generated.auth, "default_role", generated.auth.roles[0])
            return (
                RepairActionSchema(
                    step_name="restore_default_role",
                    rationale="Default role was missing and could be inferred from the first valid role.",
                    changes_applied=["auth.default_role"],
                    affected_paths=[self._path_text(issue.path)],
                ),
                True,
            )

        return (
            RepairActionSchema(
                step_name="record_missing_field",
                rationale="The missing field was logged for manual follow-up because no local repair was safe.",
                changes_applied=[],
                affected_paths=[self._path_text(issue.path)],
            ),
            False,
        )

    def _repair_api_db_mismatch(self, generated: GeneratedSchemas, issue: ValidationIssueSchema) -> tuple[RepairActionSchema, bool]:
        updated_endpoints = []
        for endpoint in generated.api.endpoints:
            endpoint_update = {}
            if endpoint.path == "/api/v1/architecture":
                endpoint_update["response_schema"] = "ArchitectureResponse"
            elif endpoint.path == "/api/v1/validation":
                endpoint_update["request_schema"] = "ValidationRequest"
                endpoint_update["response_schema"] = "ValidationReportResponse"
            elif endpoint.path == "/api/v1/repair":
                endpoint_update["request_schema"] = "RepairRequest"
                endpoint_update["response_schema"] = "RepairReportResponse"
            elif endpoint.path == "/api/v1/simulation":
                endpoint_update["request_schema"] = "SimulationRequest"
                endpoint_update["response_schema"] = "SimulationReportResponse"
            elif endpoint.path.startswith("/api/v1/pages/"):
                page_slug = endpoint.path.rsplit("/", 1)[-1]
                page = next((candidate for candidate in generated.ui.pages if slugify(candidate.name) == page_slug), None)
                if page is not None:
                    endpoint_update["response_schema"] = f"{pascal_case(page.name)}PageResponse"
            elif endpoint.path.startswith("/api/v1/workflows/"):
                workflow_name = self._workflow_name_from_endpoint(endpoint)
                endpoint_update["response_schema"] = f"{pascal_case(workflow_name)}Response"
                endpoint_update["request_schema"] = f"{pascal_case(workflow_name)}Request"

            updated_endpoints.append(endpoint.model_copy(update=endpoint_update))

        set_field_value(generated.api, "endpoints", updated_endpoints)
        return (
            RepairActionSchema(
                step_name="align_api_db_contracts",
                rationale="API schemas were realigned with the generated database and page/workflow contracts.",
                changes_applied=["api.endpoints"],
                affected_paths=[self._path_text(issue.path)],
            ),
            True,
        )

    def _repair_ui_api_mismatch(self, generated: GeneratedSchemas, issue: ValidationIssueSchema) -> tuple[RepairActionSchema, bool]:
        updated_pages = []
        for page in generated.ui.pages:
            components = ["AppShell", "HeaderBar", "NavigationRail"]
            if page.name == "Validation":
                components.append("ValidationStatusCard")
            if page.name == "Repair":
                components.append("RepairActionList")
            if page.name == "Simulation":
                components.append("WorkflowTimeline")
            updated_pages.append(page.model_copy(update={"components": normalize_list(components)}))

        set_field_value(generated.ui, "pages", updated_pages)
        return (
            RepairActionSchema(
                step_name="align_ui_api_contracts",
                rationale="UI page composition was restored using the deterministic API-driven layout.",
                changes_applied=["ui.pages"],
                affected_paths=[self._path_text(issue.path)],
            ),
            True,
        )

    def _repair_invalid_relationship(self, generated: GeneratedSchemas, issue: ValidationIssueSchema) -> tuple[RepairActionSchema, bool]:
        updated_tables = []
        table_lookup = {table.name: table for table in generated.database.tables}
        for table in generated.database.tables:
            valid_foreign_keys = []
            for foreign_key in table.foreign_keys:
                referenced = table_lookup.get(foreign_key.referenced_table)
                if referenced is None:
                    continue
                referenced_columns = {column.name for column in referenced.columns}
                if foreign_key.referenced_column not in referenced_columns:
                    continue
                valid_foreign_keys.append(foreign_key)
            updated_tables.append(table.model_copy(update={"foreign_keys": valid_foreign_keys}))

        set_field_value(generated.database, "tables", updated_tables)
        return (
            RepairActionSchema(
                step_name="repair_database_relationships",
                rationale="Invalid database relationships were pruned without affecting valid tables.",
                changes_applied=["database.tables"],
                affected_paths=[self._path_text(issue.path)],
            ),
            True,
        )

    def _repair_invalid_permission(self, generated: GeneratedSchemas, issue: ValidationIssueSchema) -> tuple[RepairActionSchema, bool]:
        if generated.auth.roles:
            set_field_value(generated.auth, "roles", normalize_list(generated.auth.roles))
            if generated.auth.default_role not in generated.auth.roles:
                set_field_value(generated.auth, "default_role", generated.auth.roles[0])

        return (
            RepairActionSchema(
                step_name="repair_permissions",
                rationale="Invalid permissions were normalized to preserve valid roles and deterministic defaults.",
                changes_applied=["auth.roles", "auth.default_role"],
                affected_paths=[self._path_text(issue.path)],
            ),
            True,
        )

    def _validate_bundle(self, generated: GeneratedSchemas) -> list[ValidationIssueSchema]:
        issues: list[ValidationIssueSchema] = []

        page_lookup = {page.name: page for page in generated.ui.pages}
        for page in generated.ui.pages:
            if not page.components:
                issues.append(self._issue("MISSING_FIELD", f"Page {page.name} has no components.", ["ui", "pages", page.name, "components"], "Restore the page component list."))

            expected_path = f"/api/v1/pages/{slugify(page.name)}"
            matching_page_endpoint = next((endpoint for endpoint in generated.api.endpoints if endpoint.path == expected_path), None)
            if matching_page_endpoint is None:
                issues.append(self._issue("UI_API_MISMATCH", f"Missing API endpoint for page {page.name}.", ["ui", "pages", page.name, "route"], f"Create {expected_path} in the API schema."))

        for endpoint in generated.api.endpoints:
            if endpoint.path == "/api/v1/validation" and endpoint.response_schema != "ValidationReportResponse":
                issues.append(self._issue("API_DB_MISMATCH", "Validation endpoint has a mismatched response schema.", ["api", "endpoints", endpoint.name, "response_schema"], "Use the deterministic validation response schema."))
            if endpoint.path == "/api/v1/repair" and endpoint.response_schema != "RepairReportResponse":
                issues.append(self._issue("API_DB_MISMATCH", "Repair endpoint has a mismatched response schema.", ["api", "endpoints", endpoint.name, "response_schema"], "Use the deterministic repair response schema."))
            if endpoint.path == "/api/v1/simulation" and endpoint.response_schema != "SimulationReportResponse":
                issues.append(self._issue("API_DB_MISMATCH", "Simulation endpoint has a mismatched response schema.", ["api", "endpoints", endpoint.name, "response_schema"], "Use the deterministic simulation response schema."))
            if endpoint.path.startswith("/api/v1/pages/"):
                page_slug = endpoint.path.rsplit("/", 1)[-1]
                page = next((candidate for candidate in generated.ui.pages if slugify(candidate.name) == page_slug), None)
                if page is None:
                    issues.append(self._issue("API_DB_MISMATCH", f"Endpoint {endpoint.name} points to an unknown page.", ["api", "endpoints", endpoint.name, "path"], "Align the endpoint with a generated page."))
                elif endpoint.response_schema != f"{pascal_case(page.name)}PageResponse":
                    issues.append(self._issue("API_DB_MISMATCH", f"Endpoint {endpoint.name} has a mismatched response schema.", ["api", "endpoints", endpoint.name, "response_schema"], "Use the deterministic page response schema name."))

            if endpoint.path.startswith("/api/v1/workflows/"):
                workflow_name = self._workflow_name_from_endpoint(endpoint)
                expected_response = f"{pascal_case(workflow_name)}Response"
                expected_request = f"{pascal_case(workflow_name)}Request"
                if endpoint.response_schema != expected_response or endpoint.request_schema not in {None, expected_request}:
                    issues.append(self._issue("API_DB_MISMATCH", f"Workflow endpoint {endpoint.name} has mismatched schemas.", ["api", "endpoints", endpoint.name], "Use the deterministic workflow request/response schema names."))

        if not generated.auth.roles:
            issues.append(self._issue("INVALID_PERMISSION", "Authentication roles are missing.", ["auth", "roles"], "Restore at least one role."))
        if generated.auth.default_role is None or generated.auth.default_role not in generated.auth.roles:
            issues.append(self._issue("MISSING_FIELD", "Authentication default role is invalid.", ["auth", "default_role"], "Set the default role to one of the available roles."))

        for table in generated.database.tables:
            column_names = {column.name for column in table.columns}
            for foreign_key in table.foreign_keys:
                referenced = table_lookup.get(foreign_key.referenced_table) if (table_lookup := {candidate.name: candidate for candidate in generated.database.tables}) else None
                if referenced is None:
                    issues.append(self._issue("INVALID_RELATIONSHIP", f"Table {table.name} references unknown table {foreign_key.referenced_table}.", ["database", "tables", table.name, "foreign_keys"], "Remove or repair the invalid foreign key."))
                    continue
                referenced_columns = {column.name for column in referenced.columns}
                if foreign_key.referenced_column not in referenced_columns or foreign_key.column not in column_names:
                    issues.append(self._issue("INVALID_RELATIONSHIP", f"Table {table.name} has an invalid foreign key relationship.", ["database", "tables", table.name, "foreign_keys"], "Normalize the relationship to a valid target column."))

        return issues

    def _workflow_name_from_endpoint(self, endpoint) -> str:
        if endpoint.name.startswith("run_"):
            return endpoint.name.removeprefix("run_").replace("_", " ")
        return endpoint.path.rsplit("/", 1)[-1].replace("-", " ")

    def _issue(self, code: str, message: str, path: list[str], suggested_fix: str) -> ValidationIssueSchema:
        return ValidationIssueSchema(code=code, message=message, severity=IssueSeverity.ERROR, path=path, suggested_fix=suggested_fix)

    def _merge_issues(self, rerun_issues: list[ValidationIssueSchema], unresolved: list[ValidationIssueSchema]) -> list[ValidationIssueSchema]:
        merged: list[ValidationIssueSchema] = []
        seen: set[str] = set()
        for issue in rerun_issues + unresolved:
            if issue.code not in seen:
                seen.add(issue.code)
                merged.append(issue)
        return merged

    def _fingerprint(self, generated: GeneratedSchemas, validation_report: ValidationReport, actions: list[RepairActionSchema], remaining_issues: list[ValidationIssueSchema]) -> str:
        payload = {
            "bundle": {
                "database": generated.database.model_dump(mode="json"),
                "api": generated.api.model_dump(mode="json"),
                "ui": generated.ui.model_dump(mode="json"),
                "auth": generated.auth.model_dump(mode="json"),
            },
            "validation_report": validation_report.model_dump(mode="json"),
            "actions": [action.model_dump(mode="json") for action in actions],
            "remaining_issues": [issue.model_dump(mode="json") for issue in remaining_issues],
        }
        return sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()

    def _path_text(self, path: list[str]) -> str:
        return "/".join(path) if path else "unknown"