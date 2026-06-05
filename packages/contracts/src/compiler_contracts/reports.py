"""Validation reporting schema."""

from __future__ import annotations

from datetime import datetime

from pydantic import Field, model_validator

from .base import StrictBaseModel, ensure_unique_values
from .types import IssueSeverity


class ValidationIssueSchema(StrictBaseModel):
    code: str = Field(min_length=1, max_length=80, pattern=r"^[A-Z0-9_]+$")
    message: str = Field(min_length=1, max_length=2_000)
    severity: IssueSeverity
    path: list[str] = Field(default_factory=list)
    suggested_fix: str | None = Field(default=None, max_length=2_000)


class ValidationReport(StrictBaseModel):
    passed: bool
    generated_at: datetime
    issues: list[ValidationIssueSchema] = Field(default_factory=list)
    summary: str = Field(min_length=1, max_length=2_000)
    deterministic_fingerprint: str = Field(min_length=64, max_length=64, pattern=r"^[a-f0-9]{64}$")

    @model_validator(mode="after")
    def validate_report(self) -> "ValidationReport":
        issue_codes = [issue.code for issue in self.issues]
        ensure_unique_values(issue_codes, "issues")

        has_errors = any(issue.severity == IssueSeverity.ERROR for issue in self.issues)
        if self.passed and has_errors:
            raise ValueError("passed reports cannot contain error-severity issues")
        if not self.passed and not has_errors:
            raise ValueError("failed reports must contain at least one error-severity issue")
        return self