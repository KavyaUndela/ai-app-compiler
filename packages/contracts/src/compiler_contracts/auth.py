"""Authentication schema."""

from __future__ import annotations

from pydantic import Field, model_validator

from .base import StrictBaseModel, ensure_non_empty_strings, ensure_unique_values, set_field_value
from .types import AuthMode


class AuthProviderSchema(StrictBaseModel):
    name: str = Field(min_length=2, max_length=120, pattern=r"^[A-Za-z][A-Za-z0-9_]*$")
    issuer: str = Field(min_length=1, max_length=500)
    client_id: str = Field(min_length=1, max_length=200)
    client_secret_env_var: str = Field(min_length=1, max_length=200, pattern=r"^[A-Z][A-Z0-9_]*$")
    scopes: list[str] = Field(default_factory=list)
    redirect_uri: str | None = Field(default=None, max_length=500)

    @model_validator(mode="after")
    def validate_provider(self) -> "AuthProviderSchema":
        set_field_value(self, "scopes", ensure_non_empty_strings(self.scopes, "scopes"))
        return self


class AuthSessionSchema(StrictBaseModel):
    session_timeout_minutes: int = Field(default=60, ge=1, le=7 * 24 * 60)
    refresh_token_enabled: bool = True
    csrf_protection_enabled: bool = True


class AuthSchema(StrictBaseModel):
    mode: AuthMode = AuthMode.DISABLED
    enabled: bool = False
    providers: list[AuthProviderSchema] = Field(default_factory=list)
    roles: list[str] = Field(default_factory=list)
    default_role: str | None = Field(default=None, min_length=1, max_length=120)
    admin_contact: str | None = Field(default=None, max_length=320, pattern=r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
    session: AuthSessionSchema = Field(default_factory=AuthSessionSchema)

    @model_validator(mode="after")
    def validate_auth(self) -> "AuthSchema":
        if self.enabled and self.mode == AuthMode.DISABLED:
            raise ValueError("enabled auth configurations must declare a non-disabled mode")
        if self.mode != AuthMode.DISABLED and not self.providers:
            raise ValueError("non-disabled auth modes require at least one provider")

        set_field_value(self, "roles", ensure_non_empty_strings(self.roles, "roles"))
        if self.default_role is not None and self.default_role not in self.roles:
            raise ValueError("default_role must match one of roles")

        provider_names = [provider.name for provider in self.providers]
        ensure_unique_values(provider_names, "providers")
        return self