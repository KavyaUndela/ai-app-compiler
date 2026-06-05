"""Intent extraction schema."""

from __future__ import annotations

from pydantic import Field, model_validator

from .base import StrictBaseModel, ensure_non_empty_strings, ensure_unique_values, set_field_value


class IntentSchema(StrictBaseModel):
    requirement_text: str = Field(min_length=20, max_length=20_000)
    application_name: str = Field(min_length=2, max_length=100, pattern=r"^[A-Za-z][A-Za-z0-9 _-]*$")
    problem_statement: str = Field(min_length=10, max_length=5_000)
    entities: list[str] = Field(default_factory=list)
    roles: list[str] = Field(default_factory=list)
    permissions: list[str] = Field(default_factory=list)
    business_rules: list[str] = Field(default_factory=list)
    workflows: list[str] = Field(default_factory=list)
    integrations: list[str] = Field(default_factory=list)
    primary_objectives: list[str] = Field(default_factory=list)
    constraints: list[str] = Field(default_factory=list)
    target_users: list[str] = Field(default_factory=list)
    success_criteria: list[str] = Field(default_factory=list)
    assumptions: list[str] = Field(default_factory=list)
    out_of_scope: list[str] = Field(default_factory=list)
    compliance_requirements: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_lists(self) -> "IntentSchema":
        set_field_value(self, "entities", ensure_unique_values(self.entities, "entities"))
        set_field_value(self, "roles", ensure_unique_values(self.roles, "roles"))
        set_field_value(self, "permissions", ensure_unique_values(self.permissions, "permissions"))
        set_field_value(self, "business_rules", ensure_unique_values(self.business_rules, "business_rules"))
        set_field_value(self, "workflows", ensure_unique_values(self.workflows, "workflows"))
        set_field_value(self, "integrations", ensure_unique_values(self.integrations, "integrations"))
        set_field_value(
            self,
            "primary_objectives",
            ensure_non_empty_strings(self.primary_objectives, "primary_objectives"),
        )
        set_field_value(self, "constraints", ensure_unique_values(self.constraints, "constraints"))
        set_field_value(self, "target_users", ensure_unique_values(self.target_users, "target_users"))
        set_field_value(
            self,
            "success_criteria",
            ensure_non_empty_strings(self.success_criteria, "success_criteria"),
        )
        set_field_value(self, "assumptions", ensure_unique_values(self.assumptions, "assumptions"))
        set_field_value(self, "out_of_scope", ensure_unique_values(self.out_of_scope, "out_of_scope"))
        set_field_value(
            self,
            "compliance_requirements",
            ensure_unique_values(self.compliance_requirements, "compliance_requirements"),
        )
        return self