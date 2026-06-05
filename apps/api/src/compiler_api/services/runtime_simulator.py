"""Deterministic runtime simulator for generated schemas."""

from __future__ import annotations

from datetime import datetime, timezone
from hashlib import sha256
import json

from compiler_contracts import (
    DatabaseSchema,
    RuntimeCrudPageSchema,
    RuntimeFieldSchema,
    RuntimeFormSchema,
    RuntimeNavigationSchema,
    RuntimePreviewSchema,
    RuntimeSimulationReport,
    TableSchema,
)

from .runtime_simulator_patterns import pascal_case, slugify, title_case_list
from .schema_generator import GeneratedSchemas


INTERNAL_TABLES = {"audit_logs", "module_dependencies", "page_components", "workflow_steps"}


class RuntimeSimulatorService:
    """Generate runtime-facing forms, CRUD pages, navigation, and previews."""

    def simulate(self, generated: GeneratedSchemas) -> RuntimeSimulationReport:
        forms = self._build_forms(generated.database)
        crud_pages = self._build_crud_pages(generated.database, forms)
        navigation = self._build_navigation(generated, crud_pages)
        previews = self._build_previews(generated, crud_pages)

        report = RuntimeSimulationReport(
            generated_at=datetime.now(timezone.utc),
            summary=f"Rendered {len(forms)} forms, {len(crud_pages)} CRUD pages, and {len(navigation)} navigation items.",
            forms=forms,
            crud_pages=crud_pages,
            navigation=navigation,
            runtime_previews=previews,
            deterministic_fingerprint="0" * 64,
        )
        fingerprint = self._fingerprint(generated, report)
        return report.model_copy(update={"deterministic_fingerprint": fingerprint})

    def _build_forms(self, database: DatabaseSchema) -> list[RuntimeFormSchema]:
        forms: list[RuntimeFormSchema] = []
        for table in database.tables:
            if self._is_read_only_table(table):
                continue

            fields = self._build_fields(table)
            if not fields:
                continue

            forms.append(
                RuntimeFormSchema(
                    name=f"{pascal_case(table.name)}Form",
                    route=f"/runtime/forms/{slugify(table.name)}",
                    resource=table.name,
                    mode="create",
                    fields=fields,
                    submit_endpoint=f"/api/v1/{slugify(table.name)}",
                )
            )
        return forms

    def _build_crud_pages(self, database: DatabaseSchema, forms: list[RuntimeFormSchema]) -> list[RuntimeCrudPageSchema]:
        form_lookup = {form.resource: form for form in forms}
        crud_pages: list[RuntimeCrudPageSchema] = []
        for table in database.tables:
            if self._is_read_only_table(table):
                continue

            form = form_lookup.get(table.name)
            if form is None:
                continue

            operations = ["list", "create", "update", "delete"]
            if self._is_relationship_table(table):
                operations = ["list", "create", "delete"]

            crud_pages.append(
                RuntimeCrudPageSchema(
                    name=f"{pascal_case(table.name)}CrudPage",
                    route=f"/runtime/{slugify(table.name)}",
                    resource=table.name,
                    operations=operations,
                    form=form,
                    source_table=table.name,
                )
            )
        return crud_pages

    def _build_navigation(self, generated: GeneratedSchemas, crud_pages: list[RuntimeCrudPageSchema]) -> list[RuntimeNavigationSchema]:
        visible_roles = title_case_list(generated.auth.roles)
        navigation: list[RuntimeNavigationSchema] = []

        for order, page in enumerate(generated.ui.pages):
            navigation.append(
                RuntimeNavigationSchema(
                    label=page.name,
                    route=page.route,
                    target_page=page.name,
                    visible_to_roles=visible_roles,
                )
            )

        for index, crud_page in enumerate(crud_pages):
            navigation.append(
                RuntimeNavigationSchema(
                    label=pascal_case(crud_page.resource),
                    route=crud_page.route,
                    target_page=crud_page.name,
                    visible_to_roles=visible_roles,
                )
            )

        return navigation

    def _build_previews(
        self,
        generated: GeneratedSchemas,
        crud_pages: list[RuntimeCrudPageSchema],
    ) -> list[RuntimePreviewSchema]:
        previews: list[RuntimePreviewSchema] = []

        for page in generated.ui.pages:
            previews.append(
                RuntimePreviewSchema(
                    title=page.name,
                    route=page.route,
                    preview_type="ui-page",
                    forms=[],
                    actions=title_case_list([f"Open {page.route}", "Render page", "Navigate"]),
                    notes=title_case_list([f"Components: {', '.join(page.components)}", f"Route: {page.route}"]),
                )
            )

        for crud_page in crud_pages:
            previews.append(
                RuntimePreviewSchema(
                    title=crud_page.name,
                    route=crud_page.route,
                    preview_type="crud-page",
                    forms=[crud_page.form.name],
                    actions=title_case_list(
                        [
                            f"List {crud_page.resource}",
                            f"Create {crud_page.resource}",
                            f"Update {crud_page.resource}",
                            f"Delete {crud_page.resource}",
                        ]
                    ),
                    notes=title_case_list([
                        f"Operations: {', '.join(crud_page.operations)}",
                        f"Source table: {crud_page.source_table}",
                    ]),
                )
            )

        return previews

    def _build_fields(self, table: TableSchema) -> list[RuntimeFieldSchema]:
        fields: list[RuntimeFieldSchema] = []
        for column in table.columns:
            if column.name == "id":
                continue

            validations = []
            if not column.nullable:
                validations.append("required")
            if column.unique:
                validations.append("unique")

            fields.append(
                RuntimeFieldSchema(
                    name=column.name,
                    label=pascal_case(column.name),
                    field_type=self._map_field_type(column.data_type),
                    source_column=column.name,
                    required=not column.nullable,
                    read_only=column.primary_key,
                    options=self._field_options(column.name),
                    validations=validations,
                )
            )

        if not fields:
            fields.append(
                RuntimeFieldSchema(
                    name=f"{table.name}_search",
                    label=pascal_case(table.name),
                    field_type="text",
                    source_column=table.name,
                    required=True,
                    read_only=False,
                    options=[],
                    validations=["required"],
                )
            )

        return fields

    def _field_options(self, column_name: str) -> list[str]:
        if column_name.endswith("_id"):
            return [f"Select {column_name.removesuffix('_id')} record"]
        return []

    def _map_field_type(self, data_type: str) -> str:
        lowered = data_type.casefold()
        if lowered in {"integer", "int", "bigint", "smallint"}:
            return "number"
        if lowered in {"boolean", "bool"}:
            return "checkbox"
        if lowered in {"timestamp", "timestamptz", "date", "datetime"}:
            return "datetime"
        if lowered == "jsonb":
            return "json"
        return "text"

    def _is_relationship_table(self, table: TableSchema) -> bool:
        return table.name.endswith(("_permissions", "_dependencies", "_steps", "_components")) or len(table.foreign_keys) >= 2

    def _is_read_only_table(self, table: TableSchema) -> bool:
        return table.name in INTERNAL_TABLES

    def _fingerprint(self, generated: GeneratedSchemas, report: RuntimeSimulationReport) -> str:
        payload = {
            "database": generated.database.model_dump(mode="json"),
            "api": generated.api.model_dump(mode="json"),
            "ui": generated.ui.model_dump(mode="json"),
            "auth": generated.auth.model_dump(mode="json"),
            "report": report.model_dump(mode="json"),
        }
        return sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()
