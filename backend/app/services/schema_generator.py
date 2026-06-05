"""
Stage 3: Schema Generator Service
Generates database, API, and UI schemas from system design.
"""

import re
import uuid
from typing import Any, Dict, List
from app.models import APIEndpoint, DatabaseField, DatabaseTable, SchemaGenerationResult, SystemDesignSchema


def _normalize_name(value: str) -> str:
    normalized = re.sub(r"[^a-zA-Z0-9]+", "_", value.strip().lower()).strip("_")
    return normalized or "item"


def _pluralize(value: str) -> str:
    if value.endswith("s"):
        return value
    if value.endswith("y"):
        return value[:-1] + "ies"
    return value + "s"

def generate_schema(design: SystemDesignSchema) -> SchemaGenerationResult:
    """Generate database, API, and UI schemas from system design."""
    
    schema_id = str(uuid.uuid4())
    
    # ============= Generate Database Schema =============
    database_schema = []
    entity_names: List[str] = []

    for module in design.modules:
        if module.name == "DataManagement":
            for page in module.pages:
                for field in page.fields:
                    candidate = _normalize_name(field)
                    if candidate not in entity_names:
                        entity_names.append(candidate)
    
    # Users table
    database_schema.append(DatabaseTable(
        table_name="users",
        fields=[
            DatabaseField(name="id", field_type="uuid", primary_key=True),
            DatabaseField(name="email", field_type="string", unique=True),
            DatabaseField(name="password_hash", field_type="string"),
            DatabaseField(name="name", field_type="string"),
            DatabaseField(name="role", field_type="string"),
            DatabaseField(name="created_at", field_type="datetime"),
            DatabaseField(name="updated_at", field_type="datetime"),
        ],
        indexes=["email", "role"]
    ))
    
    # Data entities tables
    if not entity_names:
        entity_names = ["item"]

    for entity_name in entity_names:
        table_name = _pluralize(entity_name)
        database_schema.append(
            DatabaseTable(
                table_name=table_name,
                fields=[
                    DatabaseField(name="id", field_type="uuid", primary_key=True),
                    DatabaseField(name="user_id", field_type="uuid"),
                    DatabaseField(name="name", field_type="string"),
                    DatabaseField(name="description", field_type="string", nullable=True),
                    DatabaseField(name="status", field_type="string"),
                    DatabaseField(name="created_at", field_type="datetime"),
                    DatabaseField(name="updated_at", field_type="datetime"),
                ],
                indexes=["user_id", "created_at"],
            )
        )
    
    # ============= Generate API Schema =============
    api_schema = []
    
    # Authentication endpoints
    api_schema.extend([
        APIEndpoint(
            method="POST",
            path="/auth/login",
            description="User login",
            request_body={"email": "string", "password": "string"},
            response_body={"access_token": "string", "user": {"id": "uuid", "role": "string"}}
        ),
        APIEndpoint(
            method="POST",
            path="/auth/signup",
            description="User registration",
            request_body={"email": "string", "password": "string", "name": "string"},
            response_body={"id": "uuid", "email": "string", "name": "string"}
        ),
        APIEndpoint(
            method="POST",
            path="/auth/logout",
            description="User logout",
            required_roles=["User", "Admin"],
            response_body={"message": "string"}
        ),
    ])
    
    # CRUD endpoints for data entities
    for entity_name in entity_names:
        table_name = _pluralize(entity_name)
        api_schema.extend([
            APIEndpoint(
                method="GET",
                path=f"/{table_name}",
                description=f"List all {table_name}",
                required_roles=["User", "Admin"],
                response_body={"items": [{"id": "uuid", "name": "string"}]},
            ),
            APIEndpoint(
                method="POST",
                path=f"/{table_name}",
                description=f"Create new {entity_name}",
                required_roles=["User", "Admin"],
                request_body={"name": "string", "description": "string"},
                response_body={"id": "uuid", "name": "string"},
            ),
            APIEndpoint(
                method="GET",
                path=f"/{table_name}/{{id}}",
                description=f"Get {entity_name} details",
                required_roles=["User", "Admin"],
                response_body={"id": "uuid", "name": "string"},
            ),
            APIEndpoint(
                method="PUT",
                path=f"/{table_name}/{{id}}",
                description=f"Update {entity_name}",
                required_roles=["User", "Admin"],
                request_body={"name": "string", "description": "string"},
                response_body={"id": "uuid", "updated": "boolean"},
            ),
            APIEndpoint(
                method="DELETE",
                path=f"/{table_name}/{{id}}",
                description=f"Delete {entity_name}",
                required_roles=["Admin"],
                response_body={"deleted": "boolean"},
            ),
        ])
    
    # Dashboard endpoints
    api_schema.append(APIEndpoint(
        method="GET",
        path="/dashboard/stats",
        description="Get dashboard statistics",
        required_roles=["User", "Admin"],
        response_body={"total_users": "integer", "total_items": "integer", "recent_activity": "array"}
    ))
    
    # ============= Generate UI Schema =============
    ui_schema = {
        "theme": "light",
        "colors": {
            "primary": "#3b82f6",
            "secondary": "#8b5cf6",
            "danger": "#ef4444"
        },
        "components": {
            "forms": {
                "validation": "client-side",
                "error_display": "inline",
                "success_feedback": "toast"
            },
            "lists": {
                "pagination": True,
                "items_per_page": 20,
                "sortable": True,
                "filterable": True
            },
            "dashboard": {
                "chart_library": "recharts",
                "refresh_interval": 30
            }
        },
        "layouts": {
            "main": "sidebar_navigation",
            "responsive": True,
            "mobile_friendly": True
        },
        "pages": [
            {
                "name": page.name,
                "module": module.name,
                "component_type": page.component_type,
                "fields": page.fields,
                "required_roles": page.required_roles,
                "api_paths": [
                    "/auth/login" if page.name == "Login" else "/auth/signup" if page.name == "Signup" else "/auth/logout" if page.name == "Profile" else "/dashboard/stats" if page.name == "Overview" else f"/{_pluralize(entity)}"
                    for entity in (page.fields[:1] if page.fields else ["item"])
                ],
            }
            for module in design.modules
            for page in module.pages
        ],
    }
    
    # ============= Generate Auth Schema =============
    auth_schema = {
        "method": "JWT",
        "token_expiry": 3600,
        "refresh_token_expiry": 86400,
        "roles": ["User", "Admin"],
        "permissions": {
            "User": ["read", "write"],
            "Admin": ["read", "write", "delete", "manage"]
        },
        "mfa": False,
        "password_requirements": {
            "min_length": 8,
            "require_uppercase": True,
            "require_numbers": True,
            "require_special": False
        }
    }
    
    summary = f"Generated {len(database_schema)} database tables, {len(api_schema)} API endpoints, UI and Auth schemas"
    
    return SchemaGenerationResult(
        schema_id=schema_id,
        database_schema=database_schema,
        api_schema=api_schema,
        ui_schema=ui_schema,
        auth_schema=auth_schema
    )
