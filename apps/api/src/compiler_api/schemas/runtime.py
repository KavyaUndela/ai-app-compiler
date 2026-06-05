"""Schemas for runtime simulation previews and API transport."""

from __future__ import annotations

from pydantic import Field, model_validator

from compiler_contracts import APISchema, AuthSchema, DatabaseSchema, UISchema
from compiler_contracts.base import StrictBaseModel, ensure_unique_values, set_field_value
from compiler_contracts.types import HttpMethod

from compiler_api.services.schema_generator import GeneratedSchemas


class RuntimeFormFieldPreview(StrictBaseModel):
    name: str
    label: str
    input_type: str
    required: bool = True
    options: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_field(self) -> "RuntimeFormFieldPreview":
        set_field_value(self, "options", ensure_unique_values(self.options, "options"))
        return self


class RuntimeFormPreview(StrictBaseModel):
    name: str
    title: str
    route: str
    submit_endpoint: str
    method: HttpMethod = HttpMethod.POST
    table_name: str
    fields: list[RuntimeFormFieldPreview] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_form(self) -> "RuntimeFormPreview":
        if not self.fields:
            raise ValueError("fields must contain at least one field")
        return self


class RuntimeCRUDPagePreview(StrictBaseModel):
    name: str
    title: str
    route: str
    table_name: str
    list_endpoint: str
    create_endpoint: str
    update_endpoint: str
    delete_endpoint: str
    columns: list[str] = Field(default_factory=list)
    read_only: bool = False

    @model_validator(mode="after")
    def validate_page(self) -> "RuntimeCRUDPagePreview":
        set_field_value(self, "columns", ensure_unique_values(self.columns, "columns"))
        return self


class RuntimeNavigationItemPreview(StrictBaseModel):
    label: str
    route: str
    kind: str
    order: int
    visible_to_roles: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_navigation(self) -> "RuntimeNavigationItemPreview":
        set_field_value(self, "visible_to_roles", ensure_unique_values(self.visible_to_roles, "visible_to_roles"))
        return self


class RuntimePreviewCard(StrictBaseModel):
    title: str
    description: str
    route: str
    preview_kind: str
    actions: list[str] = Field(default_factory=list)
    data_bindings: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_preview(self) -> "RuntimePreviewCard":
        set_field_value(self, "actions", ensure_unique_values(self.actions, "actions"))
        set_field_value(self, "data_bindings", ensure_unique_values(self.data_bindings, "data_bindings"))
        return self


class RuntimePreview(StrictBaseModel):
    forms: list[RuntimeFormPreview] = Field(default_factory=list)
    crud_pages: list[RuntimeCRUDPagePreview] = Field(default_factory=list)
    navigation: list[RuntimeNavigationItemPreview] = Field(default_factory=list)
    runtime_previews: list[RuntimePreviewCard] = Field(default_factory=list)
    summary: str
    deterministic_fingerprint: str

    @model_validator(mode="after")
    def validate_report(self) -> "RuntimePreview":
        set_field_value(self, "summary", self.summary.strip())
        if not self.forms:
            raise ValueError("forms must contain at least one form")
        if not self.crud_pages:
            raise ValueError("crud_pages must contain at least one CRUD page")
        if not self.navigation:
            raise ValueError("navigation must contain at least one item")
        if not self.runtime_previews:
            raise ValueError("runtime_previews must contain at least one preview")
        return self


class RuntimePreviewRequest(StrictBaseModel):
    database: DatabaseSchema
    api: APISchema
    ui: UISchema
    auth: AuthSchema

    def to_generated_schemas(self) -> GeneratedSchemas:
        return GeneratedSchemas(database=self.database, api=self.api, ui=self.ui, auth=self.auth)