"""Shared enums for schema models."""

from __future__ import annotations

from enum import Enum


class DatabaseEngine(str, Enum):
    POSTGRESQL = "postgresql"
    MYSQL = "mysql"
    SQLITE = "sqlite"


class HttpMethod(str, Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"


class IssueSeverity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


class AuthMode(str, Enum):
    DISABLED = "disabled"
    SESSION = "session"
    TOKEN = "token"
    HYBRID = "hybrid"


class UIFramework(str, Enum):
    NEXT_JS = "nextjs"
    REACT = "react"
    STREAMLIT = "streamlit"