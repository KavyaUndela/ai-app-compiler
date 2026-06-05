"""Runtime simulation schema models."""

from __future__ import annotations

from datetime import datetime

from pydantic import Field, model_validator

from .base import StrictBaseModel, ensure_non_empty_strings, ensure_unique_values, set_field_value


class RuntimeFieldSchema(StrictBaseModel):
    name: str = Field(min_length=1, max_length=120)
    label: str = Field(min_length=1, max_length=120)
    field_type: str = Field(min_length=1, max_length=80)
    source_column: str = Field(min_length=1, max_length=120)
    required: bool = True
    read_only: bool = False
    options: list[str] = Field(default_factory=list)
    validations: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_field(self) -> "RuntimeFieldSchema":
        set_field_value(self, "options", ensure_unique_values(self.options, "options"))
        set_field_value(self, "validations", ensure_unique_values(self.validations, "validations"))
        return self


class RuntimeFormSchema(StrictBaseModel):
    name: str = Field(min_length=1, max_length=120)
    route: str = Field(min_length=1, max_length=256, pattern=r"^/[^\s]*$")
    resource: str = Field(min_length=1, max_length=120)
    mode: str = Field(min_length=1, max_length=32)
    fields: list[RuntimeFieldSchema] = Field(default_factory=list)
    submit_endpoint: str = Field(min_length=1, max_length=256)

    @model_validator(mode="after")
    def validate_form(self) -> "RuntimeFormSchema":
        if not self.fields:
            raise ValueError("fields must contain at least one field")
        field_names = [field.name for field in self.fields]
        set_field_value(self, "fields", self.fields)
        ensure_unique_values(field_names, "fields")
        return self


class RuntimeCrudPageSchema(StrictBaseModel):
    name: str = Field(min_length=1, max_length=120)
    route: str = Field(min_length=1, max_length=256, pattern=r"^/[^\s]*$")
    resource: str = Field(min_length=1, max_length=120)
    operations: list[str] = Field(default_factory=list)
    form: RuntimeFormSchema
    source_table: str = Field(min_length=1, max_length=120)

    @model_validator(mode="after")
    def validate_page(self) -> "RuntimeCrudPageSchema":
        if not self.operations:
            raise ValueError("operations must contain at least one operation")
        set_field_value(self, "operations", ensure_non_empty_strings(self.operations, "operations"))
        return self


class RuntimeNavigationSchema(StrictBaseModel):
    label: str = Field(min_length=1, max_length=120)
    route: str = Field(min_length=1, max_length=256, pattern=r"^/[^\s]*$")
    target_page: str = Field(min_length=1, max_length=120)
    visible_to_roles: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_navigation(self) -> "RuntimeNavigationSchema":
        set_field_value(self, "visible_to_roles", ensure_unique_values(self.visible_to_roles, "visible_to_roles"))
        return self


class RuntimePreviewSchema(StrictBaseModel):
    title: str = Field(min_length=1, max_length=120)
    route: str = Field(min_length=1, max_length=256, pattern=r"^/[^\s]*$")
    preview_type: str = Field(min_length=1, max_length=80)
    forms: list[str] = Field(default_factory=list)
    actions: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_preview(self) -> "RuntimePreviewSchema":
        set_field_value(self, "forms", ensure_unique_values(self.forms, "forms"))
        set_field_value(self, "actions", ensure_unique_values(self.actions, "actions"))
        set_field_value(self, "notes", ensure_unique_values(self.notes, "notes"))
        return self


class RuntimeSimulationReport(StrictBaseModel):
    generated_at: datetime
    summary: str = Field(min_length=1, max_length=2_000)
    forms: list[RuntimeFormSchema] = Field(default_factory=list)
    crud_pages: list[RuntimeCrudPageSchema] = Field(default_factory=list)
    navigation: list[RuntimeNavigationSchema] = Field(default_factory=list)
    previews: list[RuntimePreviewSchema] = Field(default_factory=list)
    deterministic_fingerprint: str = Field(min_length=64, max_length=64, pattern=r"^[a-f0-9]{64}$")

    @model_validator(mode="after")
    def validate_report(self) -> "RuntimeSimulationReport":
        form_names = [form.name for form in self.forms]
        page_names = [page.name for page in self.crud_pages]
        preview_titles = [preview.title for preview in self.previews]
        nav_labels = [item.label for item in self.navigation]
        ensure_unique_values(form_names, "forms")
        ensure_unique_values(page_names, "crud_pages")
        ensure_unique_values(preview_titles, "previews")
        ensure_unique_values(nav_labels, "navigation")
        return self