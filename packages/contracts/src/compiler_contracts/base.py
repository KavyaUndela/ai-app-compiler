"""Shared strict base classes and validation helpers."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class StrictBaseModel(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        strict=True,
        populate_by_name=True,
        validate_assignment=True,
        str_strip_whitespace=True,
    )


def ensure_non_empty_strings(values: list[str], field_name: str) -> list[str]:
    if not values:
        raise ValueError(f"{field_name} must contain at least one item")

    normalized = [value.strip() for value in values]
    if any(not value for value in normalized):
        raise ValueError(f"{field_name} cannot contain blank strings")

    if len(set(normalized)) != len(normalized):
        raise ValueError(f"{field_name} must contain unique values")

    return normalized


def ensure_unique_values(values: list[str], field_name: str) -> list[str]:
    normalized = [value.strip() for value in values]
    if len(set(normalized)) != len(normalized):
        raise ValueError(f"{field_name} must contain unique values")
    if any(not value for value in normalized):
        raise ValueError(f"{field_name} cannot contain blank strings")
    return normalized


def set_field_value(model: StrictBaseModel, field_name: str, value: object) -> None:
    object.__setattr__(model, field_name, value)