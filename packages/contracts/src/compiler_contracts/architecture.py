"""System architecture schema."""

from __future__ import annotations

from pydantic import Field, model_validator

from .base import StrictBaseModel, ensure_non_empty_strings, ensure_unique_values, set_field_value


class ArchitectureLayerSchema(StrictBaseModel):
    name: str = Field(min_length=2, max_length=80, pattern=r"^[A-Za-z][A-Za-z0-9 _-]*$")
    purpose: str = Field(min_length=10, max_length=2_000)
    responsibilities: list[str] = Field(default_factory=list)
    depends_on: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_layer(self) -> "ArchitectureLayerSchema":
        set_field_value(self, "responsibilities", ensure_non_empty_strings(self.responsibilities, "responsibilities"))
        set_field_value(self, "depends_on", ensure_unique_values(self.depends_on, "depends_on"))
        return self


class ModuleSchema(StrictBaseModel):
    name: str = Field(min_length=2, max_length=80, pattern=r"^[A-Za-z][A-Za-z0-9 _-]*$")
    layer: str = Field(min_length=2, max_length=80)
    description: str = Field(min_length=10, max_length=2_000)
    responsibilities: list[str] = Field(default_factory=list)
    dependencies: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_module(self) -> "ModuleSchema":
        set_field_value(self, "responsibilities", ensure_non_empty_strings(self.responsibilities, "responsibilities"))
        set_field_value(self, "dependencies", ensure_unique_values(self.dependencies, "dependencies"))
        return self


class PageSchema(StrictBaseModel):
    name: str = Field(min_length=2, max_length=120, pattern=r"^[A-Za-z][A-Za-z0-9 _-]*$")
    route: str = Field(min_length=1, max_length=256, pattern=r"^/[^\s]*$")
    purpose: str = Field(min_length=10, max_length=2_000)
    primary_modules: list[str] = Field(default_factory=list)
    allowed_roles: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_page(self) -> "PageSchema":
        set_field_value(self, "primary_modules", ensure_unique_values(self.primary_modules, "primary_modules"))
        set_field_value(self, "allowed_roles", ensure_unique_values(self.allowed_roles, "allowed_roles"))
        return self


class NavigationSchema(StrictBaseModel):
    label: str = Field(min_length=2, max_length=120)
    route: str = Field(min_length=1, max_length=256, pattern=r"^/[^\s]*$")
    target_page: str = Field(min_length=2, max_length=120)
    order: int = Field(ge=0, le=1000)
    visible_to_roles: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_navigation(self) -> "NavigationSchema":
        set_field_value(self, "visible_to_roles", ensure_unique_values(self.visible_to_roles, "visible_to_roles"))
        return self


class WorkflowSchema(StrictBaseModel):
    name: str = Field(min_length=2, max_length=120, pattern=r"^[A-Za-z][A-Za-z0-9 _-]*$")
    trigger: str = Field(min_length=3, max_length=120)
    description: str = Field(min_length=10, max_length=2_000)
    actors: list[str] = Field(default_factory=list)
    steps: list[str] = Field(default_factory=list)
    related_pages: list[str] = Field(default_factory=list)
    related_modules: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_workflow(self) -> "WorkflowSchema":
        set_field_value(self, "actors", ensure_unique_values(self.actors, "actors"))
        set_field_value(self, "steps", ensure_non_empty_strings(self.steps, "steps"))
        set_field_value(self, "related_pages", ensure_unique_values(self.related_pages, "related_pages"))
        set_field_value(self, "related_modules", ensure_unique_values(self.related_modules, "related_modules"))
        return self


class RoleHierarchySchema(StrictBaseModel):
    role: str = Field(min_length=2, max_length=120, pattern=r"^[A-Za-z][A-Za-z0-9 _-]*$")
    parent_role: str | None = Field(default=None, min_length=2, max_length=120)
    level: int = Field(ge=0, le=1000)
    permissions: list[str] = Field(default_factory=list)
    responsibilities: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_role(self) -> "RoleHierarchySchema":
        set_field_value(self, "permissions", ensure_unique_values(self.permissions, "permissions"))
        set_field_value(self, "responsibilities", ensure_non_empty_strings(self.responsibilities, "responsibilities"))
        return self


class ArchitectureSchema(StrictBaseModel):
    system_name: str = Field(min_length=2, max_length=120)
    architecture_style: str = Field(min_length=3, max_length=80)
    layers: list[ArchitectureLayerSchema] = Field(default_factory=list)
    modules: list[ModuleSchema] = Field(default_factory=list)
    pages: list[PageSchema] = Field(default_factory=list)
    navigation: list[NavigationSchema] = Field(default_factory=list)
    workflows: list[WorkflowSchema] = Field(default_factory=list)
    role_hierarchy: list[RoleHierarchySchema] = Field(default_factory=list)
    integration_points: list[str] = Field(default_factory=list)
    deployment_units: list[str] = Field(default_factory=list)
    quality_attributes: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_architecture(self) -> "ArchitectureSchema":
        if not self.layers:
            raise ValueError("layers must contain at least one layer")
        if not self.modules:
            raise ValueError("modules must contain at least one module")
        if not self.pages:
            raise ValueError("pages must contain at least one page")
        if not self.navigation:
            raise ValueError("navigation must contain at least one item")
        if not self.workflows:
            raise ValueError("workflows must contain at least one workflow")
        if not self.role_hierarchy:
            raise ValueError("role_hierarchy must contain at least one role")

        layer_names = [layer.name for layer in self.layers]
        module_names = [module.name for module in self.modules]
        page_names = [page.name for page in self.pages]
        navigation_labels = [node.label for node in self.navigation]
        workflow_names = [workflow.name for workflow in self.workflows]
        role_names = [role.role for role in self.role_hierarchy]

        ensure_unique_values(layer_names, "layers")
        ensure_unique_values(module_names, "modules")
        ensure_unique_values(page_names, "pages")
        ensure_unique_values(navigation_labels, "navigation")
        ensure_unique_values(workflow_names, "workflows")
        ensure_unique_values(role_names, "role_hierarchy")

        known_layers = set(layer_names)
        invalid_layers = sorted({module.layer for module in self.modules if module.layer not in known_layers})
        if invalid_layers:
            raise ValueError(f"modules reference unknown layers: {', '.join(invalid_layers)}")

        known_pages = set(page_names)
        invalid_navigation_pages = sorted({node.target_page for node in self.navigation if node.target_page not in known_pages})
        if invalid_navigation_pages:
            raise ValueError(f"navigation references unknown pages: {', '.join(invalid_navigation_pages)}")

        known_modules = set(module_names)
        invalid_workflow_modules = sorted(
            {
                module_name
                for workflow in self.workflows
                for module_name in workflow.related_modules
                if module_name not in known_modules
            }
        )
        if invalid_workflow_modules:
            raise ValueError(f"workflows reference unknown modules: {', '.join(invalid_workflow_modules)}")

        invalid_workflow_pages = sorted(
            {
                page_name
                for workflow in self.workflows
                for page_name in workflow.related_pages
                if page_name not in known_pages
            }
        )
        if invalid_workflow_pages:
            raise ValueError(f"workflows reference unknown pages: {', '.join(invalid_workflow_pages)}")

        known_roles = set(role_names)
        invalid_parent_roles = sorted({role.parent_role for role in self.role_hierarchy if role.parent_role and role.parent_role not in known_roles})
        if invalid_parent_roles:
            raise ValueError(f"role_hierarchy references unknown parent roles: {', '.join(invalid_parent_roles)}")

        invalid_page_roles = sorted(
            {role_name for page in self.pages for role_name in page.allowed_roles if role_name not in known_roles}
        )
        if invalid_page_roles:
            raise ValueError(f"pages reference unknown roles: {', '.join(invalid_page_roles)}")

        invalid_navigation_roles = sorted(
            {role_name for node in self.navigation for role_name in node.visible_to_roles if role_name not in known_roles}
        )
        if invalid_navigation_roles:
            raise ValueError(f"navigation references unknown roles: {', '.join(invalid_navigation_roles)}")

        set_field_value(self, "integration_points", ensure_unique_values(self.integration_points, "integration_points"))
        set_field_value(self, "deployment_units", ensure_unique_values(self.deployment_units, "deployment_units"))
        set_field_value(self, "quality_attributes", ensure_unique_values(self.quality_attributes, "quality_attributes"))
        return self