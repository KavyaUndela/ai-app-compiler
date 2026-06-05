"""Deterministic helpers for runtime simulation previews."""

from __future__ import annotations

import re


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-")
    return slug or "section"


def pascal_case(value: str) -> str:
    parts = [part for part in re.split(r"[^A-Za-z0-9]+", value) if part]
    return "".join(part[:1].upper() + part[1:].lower() for part in parts) or "Generated"


def title_case_list(values: list[str]) -> list[str]:
    ordered: list[str] = []
    seen: set[str] = set()
    for value in values:
        normalized = re.sub(r"\s+", " ", value.strip())
        if not normalized:
            continue
        key = normalized.casefold()
        if key not in seen:
            seen.add(key)
            ordered.append(normalized)
    return ordered