"""Deterministic helpers for schema generation from architecture."""

from __future__ import annotations

import re


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-")
    return slug or "section"


def schema_identifier(value: str) -> str:
    identifier = re.sub(r"[^a-z0-9]+", "_", value.casefold()).strip("_")
    if not identifier:
        identifier = "schema"
    if identifier[0].isdigit():
        identifier = f"schema_{identifier}"
    return identifier


def component_name(value: str) -> str:
    parts = [part for part in re.split(r"[^A-Za-z0-9]+", value) if part]
    if not parts:
        return "GeneratedComponent"
    return "".join(part[:1].upper() + part[1:] for part in parts) + "Component"


def title_case_list(values: list[str]) -> list[str]:
    ordered: list[str] = []
    seen: set[str] = set()
    for value in values:
        normalized = re.sub(r"\s+", " ", value.strip())
        if not normalized:
            continue
        key = normalized.casefold()
        if key in seen:
            continue
        seen.add(key)
        ordered.append(normalized)
    return ordered
