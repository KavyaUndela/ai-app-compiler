"""API contract schema."""

from __future__ import annotations

from pydantic import Field, model_validator

from .base import StrictBaseModel, ensure_unique_values, set_field_value
from .types import HttpMethod


class EndpointSchema(StrictBaseModel):
    name: str = Field(min_length=2, max_length=120, pattern=r"^[A-Za-z][A-Za-z0-9_]*$")
    path: str = Field(min_length=1, max_length=256, pattern=r"^/[^\s]*$")
    method: HttpMethod
    description: str = Field(min_length=10, max_length=2_000)
    request_schema: str | None = Field(default=None, max_length=200)
    response_schema: str = Field(min_length=1, max_length=200)
    auth_required: bool = True
    tags: list[str] = Field(default_factory=list)
    idempotent: bool = False

    @model_validator(mode="after")
    def validate_tags(self) -> "EndpointSchema":
        set_field_value(self, "tags", ensure_unique_values(self.tags, "tags"))
        return self


class APISchema(StrictBaseModel):
    base_path: str = Field(default="/api", min_length=1, max_length=128, pattern=r"^/[^\s]*$")
    version: str = Field(min_length=1, max_length=32)
    endpoints: list[EndpointSchema] = Field(default_factory=list)
    middlewares: list[str] = Field(default_factory=list)
    cors_enabled: bool = True
    rate_limiting_enabled: bool = True
    openapi_enabled: bool = True

    @model_validator(mode="after")
    def validate_api(self) -> "APISchema":
        if not self.endpoints:
            raise ValueError("endpoints must contain at least one endpoint")

        endpoint_keys = [f"{endpoint.method.value} {endpoint.path}" for endpoint in self.endpoints]
        ensure_unique_values(endpoint_keys, "endpoints")
        set_field_value(self, "middlewares", ensure_unique_values(self.middlewares, "middlewares"))
        return self