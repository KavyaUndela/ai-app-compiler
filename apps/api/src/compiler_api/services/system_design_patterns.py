"""Deterministic helpers for architecture synthesis from intent."""

from __future__ import annotations

import re

from compiler_contracts import IntentSchema


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


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-")
    return slug or "section"


def normalize_role_names(intent: IntentSchema) -> list[str]:
    candidates = intent.roles or intent.target_users or ["user"]
    roles = []
    for candidate in candidates:
        normalized = re.sub(r"\s+", " ", candidate.strip())
        if not normalized:
            continue
        roles.append(normalized.title())
    return title_case_list(roles)


def normalize_permissions(intent: IntentSchema) -> list[str]:
    permissions = []
    for permission in intent.permissions:
        normalized = re.sub(r"\s+", " ", permission.strip())
        if normalized:
            permissions.append(normalized)
    return title_case_list(permissions)
