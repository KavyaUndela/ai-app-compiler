"""Deterministic system design service."""

from __future__ import annotations

from compiler_contracts import (
    ArchitectureLayerSchema,
    ArchitectureSchema,
    IntentSchema,
    ModuleSchema,
    NavigationSchema,
    PageSchema,
    RoleHierarchySchema,
    WorkflowSchema,
)

from .system_design_patterns import normalize_permissions, normalize_role_names, slugify, title_case_list


class SystemDesignService:
    """Convert an IntentSchema into a validated ArchitectureSchema.

    The service is deterministic: the same intent always produces the same
    architecture structure, module list, page map, navigation tree, workflows,
    and role hierarchy.
    """

    def design(self, intent: IntentSchema) -> ArchitectureSchema:
        roles = normalize_role_names(intent)
        permissions = normalize_permissions(intent)

        layers = self._build_layers()
        modules = self._build_modules(intent)
        pages = self._build_pages(intent, roles)
        navigation = self._build_navigation(pages, roles)
        workflows = self._build_workflows(intent, modules, pages, roles)
        role_hierarchy = self._build_role_hierarchy(intent, roles, permissions)

        return ArchitectureSchema(
            system_name=intent.application_name,
            architecture_style="deterministic layered compiler platform",
            layers=layers,
            modules=modules,
            pages=pages,
            navigation=navigation,
            workflows=workflows,
            role_hierarchy=role_hierarchy,
            integration_points=title_case_list(intent.integrations),
            deployment_units=["frontend", "backend", "database", "worker"],
            quality_attributes=["deterministic", "modular", "validated", "repairable", "observable"],
        )

    def _build_layers(self) -> list[ArchitectureLayerSchema]:
        return [
            ArchitectureLayerSchema(
                name="presentation",
                purpose="Owns user-facing pages and navigation.",
                responsibilities=["render pages", "collect user input", "display validation output"],
                depends_on=["application"],
            ),
            ArchitectureLayerSchema(
                name="application",
                purpose="Coordinates design synthesis and system workflows.",
                responsibilities=["orchestrate design", "manage workflows", "apply policy decisions"],
                depends_on=["domain", "infrastructure"],
            ),
            ArchitectureLayerSchema(
                name="domain",
                purpose="Defines intent, architecture, and governance concepts.",
                responsibilities=["model compiler stages", "define roles", "define workflow rules"],
                depends_on=[],
            ),
            ArchitectureLayerSchema(
                name="infrastructure",
                purpose="Provides persistence, telemetry, and external integrations.",
                responsibilities=["store artifacts", "integrate external systems", "emit telemetry"],
                depends_on=["domain"],
            ),
        ]

    def _build_modules(self, intent: IntentSchema) -> list[ModuleSchema]:
        entity_count = max(len(intent.entities), 1)
        has_integrations = bool(intent.integrations)
        modules = [
            ModuleSchema(
                name="system-designer",
                layer="application",
                description="Transforms extracted intent into a structured architecture.",
                responsibilities=["convert intent to architecture", "coordinate design decisions"],
                dependencies=["intent-orchestrator"],
            ),
            ModuleSchema(
                name="intent-orchestrator",
                layer="application",
                description="Normalizes intent signals and prepares them for design synthesis.",
                responsibilities=["aggregate entities", "aggregate roles", "aggregate rules"],
                dependencies=[],
            ),
            ModuleSchema(
                name="schema-generator",
                layer="application",
                description="Produces strict JSON schemas for generated application assets.",
                responsibilities=["generate schemas", "enforce contract shape"],
                dependencies=["system-designer"],
            ),
            ModuleSchema(
                name="validation-engine",
                layer="application",
                description="Validates architecture artifacts against strict contracts.",
                responsibilities=["validate artifacts", "report issues"],
                dependencies=["schema-generator"],
            ),
            ModuleSchema(
                name="repair-engine",
                layer="application",
                description="Applies deterministic repair steps to invalid design outputs.",
                responsibilities=["repair invalid artifacts", "revalidate output"],
                dependencies=["validation-engine"],
            ),
            ModuleSchema(
                name="runtime-simulator",
                layer="application",
                description="Simulates generated application behavior before deployment.",
                responsibilities=["simulate runtime", "verify deterministic behavior"],
                dependencies=["validation-engine"],
            ),
            ModuleSchema(
                name="presentation-console",
                layer="presentation",
                description="Displays generated pages, navigation, workflows, and validation results.",
                responsibilities=["render pages", "show architecture", "show repair output"],
                dependencies=["system-designer"],
            ),
            ModuleSchema(
                name="persistence-store",
                layer="infrastructure",
                description="Persists generated design artifacts and evaluation reports.",
                responsibilities=["store architecture", "store reports"],
                dependencies=[],
            ),
        ]

        if has_integrations:
            modules.append(
                ModuleSchema(
                    name="integration-adapters",
                    layer="infrastructure",
                    description="Wraps external integration targets described by the intent.",
                    responsibilities=["connect external systems", "prepare integration contracts"],
                    dependencies=["persistence-store"],
                )
            )

        if entity_count > 2:
            modules.append(
                ModuleSchema(
                    name="domain-models",
                    layer="domain",
                    description="Captures domain entities and compiler policies extracted from intent.",
                    responsibilities=["model entities", "model permissions", "model business rules"],
                    dependencies=[],
                )
            )

        return modules

    def _build_pages(self, intent: IntentSchema, roles: list[str]) -> list[PageSchema]:
        base_pages = [
            PageSchema(
                name="Dashboard",
                route="/dashboard",
                purpose="Summarize compiler status and high-level application intent.",
                primary_modules=["presentation-console", "system-designer"],
                allowed_roles=roles,
            ),
            PageSchema(
                name="Requirements",
                route="/requirements",
                purpose="Capture and review the natural-language requirements.",
                primary_modules=["intent-orchestrator", "presentation-console"],
                allowed_roles=roles,
            ),
            PageSchema(
                name="Architecture",
                route="/architecture",
                purpose="Inspect the synthesized architecture design.",
                primary_modules=["system-designer", "presentation-console"],
                allowed_roles=roles,
            ),
            PageSchema(
                name="Validation",
                route="/validation",
                purpose="Review validation results and contract compliance.",
                primary_modules=["validation-engine", "presentation-console"],
                allowed_roles=roles,
            ),
            PageSchema(
                name="Repair",
                route="/repair",
                purpose="Apply or inspect deterministic repair actions.",
                primary_modules=["repair-engine", "presentation-console"],
                allowed_roles=roles,
            ),
            PageSchema(
                name="Simulation",
                route="/simulation",
                purpose="Run runtime simulation against the design artifacts.",
                primary_modules=["runtime-simulator", "presentation-console"],
                allowed_roles=roles,
            ),
        ]

        if intent.integrations:
            base_pages.append(
                PageSchema(
                    name="Integrations",
                    route="/integrations",
                    purpose="Inspect external systems and adapter contracts.",
                    primary_modules=["integration-adapters", "presentation-console"],
                    allowed_roles=roles,
                )
            )

        return base_pages

    def _build_navigation(self, pages: list[PageSchema], roles: list[str]) -> list[NavigationSchema]:
        route_order = ["/dashboard", "/requirements", "/architecture", "/validation", "/repair", "/simulation", "/integrations"]
        page_lookup = {page.route: page for page in pages}
        navigation: list[NavigationSchema] = []
        for order, route in enumerate(route_order):
            page = page_lookup.get(route)
            if page is None:
                continue
            navigation.append(
                NavigationSchema(
                    label=page.name,
                    route=page.route,
                    target_page=page.name,
                    order=order,
                    visible_to_roles=roles,
                )
            )
        return navigation

    def _build_workflows(self, intent: IntentSchema, modules: list[ModuleSchema], pages: list[PageSchema], roles: list[str]) -> list[WorkflowSchema]:
        page_names = [page.name for page in pages]
        module_names = [module.name for module in modules]
        workflows = [
            WorkflowSchema(
                name="Requirement To Architecture",
                trigger="new requirement submitted",
                description="Translate the incoming requirement into a validated architecture.",
                actors=roles,
                steps=[
                    "Capture requirement text",
                    "Extract intent signals",
                    "Generate architecture",
                    "Validate output",
                    "Repair invalid output",
                    "Simulate runtime",
                ],
                related_pages=["Requirements", "Architecture", "Validation", "Repair", "Simulation"],
                related_modules=["intent-orchestrator", "system-designer", "schema-generator", "validation-engine", "repair-engine", "runtime-simulator"],
            ),
            WorkflowSchema(
                name="Review And Approval",
                trigger="architecture requires review",
                description="Let privileged roles review and approve the generated design.",
                actors=roles,
                steps=[
                    "Review architecture",
                    "Assess validation report",
                    "Approve or request repair",
                ],
                related_pages=["Dashboard", "Architecture", "Validation", "Repair"],
                related_modules=["presentation-console", "validation-engine", "repair-engine"],
            ),
        ]

        if intent.integrations:
            workflows.append(
                WorkflowSchema(
                    name="Integration Readiness",
                    trigger="external systems detected",
                    description="Prepare integration adapters and verify external connectivity.",
                    actors=roles,
                    steps=[
                        "List integrations",
                        "Generate adapter contracts",
                        "Verify integration readiness",
                    ],
                    related_pages=["Integrations"],
                    related_modules=["integration-adapters", "persistence-store"],
                )
            )

        return workflows

    def _build_role_hierarchy(self, intent: IntentSchema, roles: list[str], permissions: list[str]) -> list[RoleHierarchySchema]:
        inferred_roles = roles or ["User"]
        primary_role = inferred_roles[0]
        hierarchy: list[RoleHierarchySchema] = []

        for index, role in enumerate(inferred_roles):
            lower = role.casefold()
            if lower in {"admin", "administrator", "owner"}:
                parent_role = None
                level = 100
            elif lower in {"manager", "approver", "supervisor", "reviewer"}:
                parent_role = primary_role if role != primary_role else None
                level = 70
            elif lower in {"editor", "author", "operator"}:
                parent_role = primary_role if role != primary_role else None
                level = 50
            else:
                parent_role = primary_role if role != primary_role else None
                level = 10 + index

            role_permissions = [permission for permission in permissions if lower in permission.casefold()]
            if not role_permissions and permissions:
                role_permissions = permissions[:1] if role != primary_role else permissions
            if not role_permissions:
                role_permissions = [f"Access {role} workspace"]

            responsibilities = [f"Use the {role.lower()} experience"]
            if lower in {"admin", "administrator", "owner"}:
                responsibilities.append("Manage application policies and approvals")
            elif lower in {"manager", "approver", "supervisor", "reviewer"}:
                responsibilities.append("Review and approve generated architecture")

            hierarchy.append(
                RoleHierarchySchema(
                    role=role,
                    parent_role=parent_role,
                    level=level,
                    permissions=title_case_list(role_permissions),
                    responsibilities=title_case_list(responsibilities),
                )
            )

        return hierarchy