"""Repair reporting schema."""

from __future__ import annotations

from datetime import datetime

from pydantic import Field, model_validator

from .base import StrictBaseModel, ensure_unique_values, set_field_value
from .reports import ValidationIssueSchema, ValidationReport


class RepairActionSchema(StrictBaseModel):
    step_name: str = Field(min_length=1, max_length=120)
    rationale: str = Field(min_length=1, max_length=2_000)
    changes_applied: list[str] = Field(default_factory=list)
    affected_paths: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_action(self) -> "RepairActionSchema":
        set_field_value(self, "changes_applied", ensure_unique_values(self.changes_applied, "changes_applied"))
        set_field_value(self, "affected_paths", ensure_unique_values(self.affected_paths, "affected_paths"))
        return self


class RepairReport(StrictBaseModel):
    succeeded: bool
    generated_at: datetime
    original_report: ValidationReport
    repair_actions: list[RepairActionSchema] = Field(default_factory=list)
    remaining_issues: list[ValidationIssueSchema] = Field(default_factory=list)
    deterministic_fingerprint: str = Field(min_length=64, max_length=64, pattern=r"^[a-f0-9]{64}$")

    @model_validator(mode="after")
    def validate_repair_report(self) -> "RepairReport":
        action_names = [action.step_name for action in self.repair_actions]
        ensure_unique_values(action_names, "repair_actions")

        remaining_codes = [issue.code for issue in self.remaining_issues]
        ensure_unique_values(remaining_codes, "remaining_issues")

        if self.succeeded and self.remaining_issues:
            raise ValueError("successful repair reports cannot contain remaining issues")
        if not self.succeeded and not self.repair_actions:
            raise ValueError("failed repair reports must include at least one repair action")
        return self