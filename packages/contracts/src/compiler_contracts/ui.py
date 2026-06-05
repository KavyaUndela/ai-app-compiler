"""User interface schema."""

from __future__ import annotations

from pydantic import Field, model_validator

from .base import StrictBaseModel, ensure_non_empty_strings, ensure_unique_values, set_field_value
from .types import UIFramework


class UIComponentSchema(StrictBaseModel):
    name: str = Field(min_length=2, max_length=120, pattern=r"^[A-Za-z][A-Za-z0-9_]*$")
    component_type: str = Field(min_length=2, max_length=80)
    description: str = Field(min_length=10, max_length=2_000)
    props: list[str] = Field(default_factory=list)
    dependencies: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_component(self) -> "UIComponentSchema":
        set_field_value(self, "props", ensure_unique_values(self.props, "props"))
        set_field_value(self, "dependencies", ensure_unique_values(self.dependencies, "dependencies"))
        return self


class UIPageSchema(StrictBaseModel):
    name: str = Field(min_length=2, max_length=120, pattern=r"^[A-Za-z][A-Za-z0-9_]*$")
    route: str = Field(min_length=1, max_length=256, pattern=r"^/[^\s]*$")
    description: str = Field(min_length=10, max_length=2_000)
    components: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_page(self) -> "UIPageSchema":
        set_field_value(self, "components", ensure_non_empty_strings(self.components, "components"))
        return self


class UISchema(StrictBaseModel):
    framework: UIFramework = UIFramework.NEXT_JS
    application_name: str = Field(min_length=2, max_length=120)
    theme_name: str = Field(min_length=2, max_length=120)
    pages: list[UIPageSchema] = Field(default_factory=list)
    components: list[UIComponentSchema] = Field(default_factory=list)
    design_tokens: list[str] = Field(default_factory=list)
    accessibility_requirements: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_ui(self) -> "UISchema":
        if not self.pages:
            raise ValueError("pages must contain at least one page")
        if not self.components:
            raise ValueError("components must contain at least one component")

        page_routes = [page.route for page in self.pages]
        component_names = [component.name for component in self.components]
        ensure_unique_values(page_routes, "pages")
        ensure_unique_values(component_names, "components")

        known_components = set(component_names)
        missing_components = sorted(
            {
                component_name
                for page in self.pages
                for component_name in page.components
                if component_name not in known_components
            }
        )
        if missing_components:
            raise ValueError(f"pages reference unknown components: {', '.join(missing_components)}")

        set_field_value(self, "design_tokens", ensure_unique_values(self.design_tokens, "design_tokens"))
        set_field_value(
            self,
            "accessibility_requirements",
            ensure_unique_values(self.accessibility_requirements, "accessibility_requirements"),
        )
        return self