"""Deterministic schema generation service."""

from __future__ import annotations

from dataclasses import dataclass

from compiler_contracts import (
    APISchema,
    ArchitectureSchema,
    AuthMode,
    AuthProviderSchema,
    AuthSchema,
    AuthSessionSchema,
    ColumnSchema,
    DatabaseEngine,
    DatabaseSchema,
    EndpointSchema,
    ForeignKeySchema,
    HttpMethod,
    IndexSchema,
    TableSchema,
    UISchema,
    UIComponentSchema,
    UIFramework,
    UIPageSchema,
)

from .schema_generator_patterns import component_name, schema_identifier, slugify, title_case_list


@dataclass(frozen=True)
class GeneratedSchemas:
    database: DatabaseSchema
    api: APISchema
    ui: UISchema
    auth: AuthSchema


class SchemaGeneratorService:
    """Convert a validated architecture into executable schema artifacts.

    The service is deterministic and cross-schema consistent: page routes,
    modules, roles, and workflows are reused across the database, API, UI,
    and auth schemas.
    """

    def generate(self, architecture: ArchitectureSchema) -> GeneratedSchemas:
        database = self._build_database_schema(architecture)
        api = self._build_api_schema(architecture)
        ui = self._build_ui_schema(architecture)
        auth = self._build_auth_schema(architecture)
        return GeneratedSchemas(database=database, api=api, ui=ui, auth=auth)

    def _build_database_schema(self, architecture: ArchitectureSchema) -> DatabaseSchema:
        roles = [role.role for role in architecture.role_hierarchy]
        modules = [module.name for module in architecture.modules]
        pages = [page.name for page in architecture.pages]
        workflows = [workflow.name for workflow in architecture.workflows]
        permissions = sorted(
            {
                permission
                for role in architecture.role_hierarchy
                for permission in role.permissions
            }
        )

        tables = [
            TableSchema(
                name="applications",
                description="Core application metadata.",
                columns=[
                    ColumnSchema(name="id", data_type="uuid", nullable=False, primary_key=True),
                    ColumnSchema(name="name", data_type="text", nullable=False, unique=True),
                    ColumnSchema(name="architecture_style", data_type="text", nullable=False),
                    ColumnSchema(name="created_at", data_type="timestamptz", nullable=False),
                ],
                indexes=[IndexSchema(name="applications_name_idx", columns=["name"], unique=True)],
            ),
            TableSchema(
                name="roles",
                description="Application roles and hierarchy.",
                columns=[
                    ColumnSchema(name="id", data_type="uuid", nullable=False, primary_key=True),
                    ColumnSchema(name="application_id", data_type="uuid", nullable=False),
                    ColumnSchema(name="role_name", data_type="text", nullable=False, unique=True),
                    ColumnSchema(name="parent_role_id", data_type="uuid", nullable=True),
                    ColumnSchema(name="level", data_type="integer", nullable=False),
                ],
                foreign_keys=[
                    ForeignKeySchema(column="application_id", referenced_table="applications", referenced_column="id"),
                    ForeignKeySchema(column="parent_role_id", referenced_table="roles", referenced_column="id"),
                ],
                indexes=[IndexSchema(name="roles_application_idx", columns=["application_id"], unique=False)],
            ),
            TableSchema(
                name="permissions",
                description="Permission catalog derived from role capabilities.",
                columns=[
                    ColumnSchema(name="id", data_type="uuid", nullable=False, primary_key=True),
                    ColumnSchema(name="application_id", data_type="uuid", nullable=False),
                    ColumnSchema(name="permission_name", data_type="text", nullable=False, unique=True),
                    ColumnSchema(name="description", data_type="text", nullable=False),
                ],
                foreign_keys=[
                    ForeignKeySchema(column="application_id", referenced_table="applications", referenced_column="id"),
                ],
            ),
            TableSchema(
                name="role_permissions",
                description="Join table between roles and permissions.",
                columns=[
                    ColumnSchema(name="id", data_type="uuid", nullable=False, primary_key=True),
                    ColumnSchema(name="role_id", data_type="uuid", nullable=False),
                    ColumnSchema(name="permission_id", data_type="uuid", nullable=False),
                ],
                foreign_keys=[
                    ForeignKeySchema(column="role_id", referenced_table="roles", referenced_column="id"),
                    ForeignKeySchema(column="permission_id", referenced_table="permissions", referenced_column="id"),
                ],
            ),
            TableSchema(
                name="modules",
                description="Synthesized system modules.",
                columns=[
                    ColumnSchema(name="id", data_type="uuid", nullable=False, primary_key=True),
                    ColumnSchema(name="application_id", data_type="uuid", nullable=False),
                    ColumnSchema(name="module_name", data_type="text", nullable=False, unique=True),
                    ColumnSchema(name="layer", data_type="text", nullable=False),
                    ColumnSchema(name="description", data_type="text", nullable=False),
                ],
                foreign_keys=[
                    ForeignKeySchema(column="application_id", referenced_table="applications", referenced_column="id"),
                ],
            ),
            TableSchema(
                name="pages",
                description="User-facing application pages.",
                columns=[
                    ColumnSchema(name="id", data_type="uuid", nullable=False, primary_key=True),
                    ColumnSchema(name="application_id", data_type="uuid", nullable=False),
                    ColumnSchema(name="page_name", data_type="text", nullable=False, unique=True),
                    ColumnSchema(name="route", data_type="text", nullable=False, unique=True),
                    ColumnSchema(name="purpose", data_type="text", nullable=False),
                ],
                foreign_keys=[
                    ForeignKeySchema(column="application_id", referenced_table="applications", referenced_column="id"),
                ],
            ),
            TableSchema(
                name="workflows",
                description="Operational workflows derived from the architecture.",
                columns=[
                    ColumnSchema(name="id", data_type="uuid", nullable=False, primary_key=True),
                    ColumnSchema(name="application_id", data_type="uuid", nullable=False),
                    ColumnSchema(name="workflow_name", data_type="text", nullable=False, unique=True),
                    ColumnSchema(name="trigger_text", data_type="text", nullable=False),
                    ColumnSchema(name="description", data_type="text", nullable=False),
                ],
                foreign_keys=[
                    ForeignKeySchema(column="application_id", referenced_table="applications", referenced_column="id"),
                ],
            ),
            TableSchema(
                name="audit_logs",
                description="Deterministic audit trail for generated artifacts.",
                columns=[
                    ColumnSchema(name="id", data_type="uuid", nullable=False, primary_key=True),
                    ColumnSchema(name="application_id", data_type="uuid", nullable=False),
                    ColumnSchema(name="actor_role", data_type="text", nullable=False),
                    ColumnSchema(name="event_type", data_type="text", nullable=False),
                    ColumnSchema(name="payload", data_type="jsonb", nullable=False),
                ],
                foreign_keys=[
                    ForeignKeySchema(column="application_id", referenced_table="applications", referenced_column="id"),
                ],
            ),
        ]

        if modules:
            tables.append(
                TableSchema(
                    name="module_dependencies",
                    description="Cross-module dependency graph.",
                    columns=[
                        ColumnSchema(name="id", data_type="uuid", nullable=False, primary_key=True),
                        ColumnSchema(name="module_id", data_type="uuid", nullable=False),
                        ColumnSchema(name="depends_on_module_id", data_type="uuid", nullable=False),
                    ],
                    foreign_keys=[
                        ForeignKeySchema(column="module_id", referenced_table="modules", referenced_column="id"),
                        ForeignKeySchema(column="depends_on_module_id", referenced_table="modules", referenced_column="id"),
                    ],
                )
            )

        if pages:
            tables.append(
                TableSchema(
                    name="page_components",
                    description="Links pages to the components they render.",
                    columns=[
                        ColumnSchema(name="id", data_type="uuid", nullable=False, primary_key=True),
                        ColumnSchema(name="page_id", data_type="uuid", nullable=False),
                        ColumnSchema(name="component_name", data_type="text", nullable=False),
                    ],
                    foreign_keys=[
                        ForeignKeySchema(column="page_id", referenced_table="pages", referenced_column="id"),
                    ],
                )
            )

        if workflows:
            tables.append(
                TableSchema(
                    name="workflow_steps",
                    description="Ordered execution steps for workflows.",
                    columns=[
                        ColumnSchema(name="id", data_type="uuid", nullable=False, primary_key=True),
                        ColumnSchema(name="workflow_id", data_type="uuid", nullable=False),
                        ColumnSchema(name="step_order", data_type="integer", nullable=False),
                        ColumnSchema(name="step_text", data_type="text", nullable=False),
                    ],
                    foreign_keys=[
                        ForeignKeySchema(column="workflow_id", referenced_table="workflows", referenced_column="id"),
                    ],
                )
            )

        return DatabaseSchema(
            engine=DatabaseEngine.POSTGRESQL,
            database_name=schema_identifier(architecture.system_name),
            tables=tables,
            schemas=["public"],
        )

    def _build_api_schema(self, architecture: ArchitectureSchema) -> APISchema:
        endpoints = [
            EndpointSchema(
                name="health_check",
                path="/api/v1/health",
                method=HttpMethod.GET,
                description="Return service health and readiness.",
                response_schema="HealthCheckResponse",
                auth_required=False,
                tags=["system"],
                idempotent=True,
            ),
            EndpointSchema(
                name="get_architecture",
                path="/api/v1/architecture",
                method=HttpMethod.GET,
                description="Return the synthesized architecture.",
                response_schema="ArchitectureResponse",
                auth_required=True,
                tags=["architecture"],
                idempotent=True,
            ),
            EndpointSchema(
                name="validate_schema",
                path="/api/v1/validation",
                method=HttpMethod.POST,
                description="Validate generated schemas and architecture artifacts.",
                request_schema="ValidationRequest",
                response_schema="ValidationReportResponse",
                auth_required=True,
                tags=["validation"],
            ),
            EndpointSchema(
                name="repair_schema",
                path="/api/v1/repair",
                method=HttpMethod.POST,
                description="Repair invalid generated artifacts.",
                request_schema="RepairRequest",
                response_schema="RepairReportResponse",
                auth_required=True,
                tags=["repair"],
            ),
            EndpointSchema(
                name="simulate_runtime",
                path="/api/v1/simulation",
                method=HttpMethod.POST,
                description="Simulate the generated application runtime.",
                request_schema="SimulationRequest",
                response_schema="SimulationReportResponse",
                auth_required=True,
                tags=["simulation"],
            ),
        ]

        for page in architecture.pages:
            endpoints.append(
                EndpointSchema(
                    name=f"get_{slugify(page.name)}",
                    path=f"/api/v1/pages/{slugify(page.name)}",
                    method=HttpMethod.GET,
                    description=f"Return the generated payload for {page.name}.",
                    response_schema=f"{page.name.replace(' ', '')}PageResponse",
                    auth_required=True,
                    tags=[page.name, "ui"],
                    idempotent=True,
                )
            )

        for workflow in architecture.workflows:
            workflow_identifier = "_".join(part for part in __import__("re").split(r"[^A-Za-z0-9]+", workflow.name.lower()) if part)
            if not workflow_identifier:
                workflow_identifier = "workflow"
            if workflow_identifier[0].isdigit():
                workflow_identifier = f"workflow_{workflow_identifier}"
            endpoints.append(
                EndpointSchema(
                    name=f"run_{workflow_identifier}",
                    path=f"/api/v1/workflows/{slugify(workflow.name)}",
                    method=HttpMethod.POST,
                    description=f"Trigger {workflow.name.lower()}.",
                    request_schema=f"{workflow.name.replace(' ', '')}Request",
                    response_schema=f"{workflow.name.replace(' ', '')}Response",
                    auth_required=True,
                    tags=[workflow.name, "workflow"],
                )
            )

        return APISchema(
            base_path="/api/v1",
            version="1.0.0",
            endpoints=endpoints,
            middlewares=["request-id", "authentication", "authorization", "validation", "audit"],
        )

    def _build_ui_schema(self, architecture: ArchitectureSchema) -> UISchema:
        shared_components = [
            "AppShell",
            "HeaderBar",
            "NavigationRail",
            "ValidationStatusCard",
            "RepairActionList",
            "WorkflowTimeline",
        ]
        module_component_map = {module.name: component_name(module.name) for module in architecture.modules}
        page_components = list(module_component_map.values()) + shared_components

        components = [
            UIComponentSchema(
                name=name,
                component_type="layout" if name in {"AppShell", "NavigationRail", "HeaderBar"} else "panel",
                description=f"Generated component for {name}.",
            )
            for name in page_components
        ]

        pages = []
        for page in architecture.pages:
            associated_component_names = [module_component_map[module_name] for module_name in page.primary_modules if module_name in module_component_map]
            associated_component_names.extend(["AppShell", "HeaderBar", "NavigationRail"])
            if page.name == "Validation":
                associated_component_names.append("ValidationStatusCard")
            if page.name == "Repair":
                associated_component_names.append("RepairActionList")
            if page.name == "Simulation":
                associated_component_names.append("WorkflowTimeline")

            pages.append(
                UIPageSchema(
                    name=page.name,
                    route=page.route,
                    description=page.purpose,
                    components=title_case_list(associated_component_names),
                )
            )

        return UISchema(
            framework=UIFramework.NEXT_JS,
            application_name=architecture.system_name,
            theme_name="compiler-control-room",
            pages=pages,
            components=components,
            design_tokens=["surface-1", "surface-2", "accent", "muted", "border"],
            accessibility_requirements=["keyboard navigable", "semantic landmarks", "sufficient contrast"],
        )

    def _build_auth_schema(self, architecture: ArchitectureSchema) -> AuthSchema:
        roles = [role.role for role in architecture.role_hierarchy]
        lowest_role = min(architecture.role_hierarchy, key=lambda item: item.level).role
        app_slug = slugify(architecture.system_name)

        return AuthSchema(
            mode=AuthMode.HYBRID,
            enabled=True,
            providers=[
                AuthProviderSchema(
                    name="oidc",
                    issuer=f"https://auth.local/{app_slug}",
                    client_id=f"{app_slug}-web",
                    client_secret_env_var=f"{app_slug.upper().replace('-', '_')}_AUTH_SECRET",
                    scopes=["openid", "profile", "email"],
                    redirect_uri=f"https://app.local/{app_slug}/auth/callback",
                )
            ],
            roles=roles,
            default_role=lowest_role,
            admin_contact=f"admin@{app_slug}.local",
            session=AuthSessionSchema(session_timeout_minutes=60, refresh_token_enabled=True, csrf_protection_enabled=True),
        )