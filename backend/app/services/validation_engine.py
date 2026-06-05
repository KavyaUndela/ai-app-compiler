"""
Stage 4: Validation Engine Service
Validates generated schemas against constraints and business rules.
"""

import re
import uuid
from typing import List

from app.models import SchemaGenerationResult, ValidationIssue, ValidationResult


def _table_from_path(path: str) -> str:
    clean = path.strip("/").split("/")[0]
    return clean.lower()

def validate_schema(schema: SchemaGenerationResult) -> ValidationResult:
    """Validate generated schema for correctness and consistency."""
    
    validation_id = str(uuid.uuid4())
    issues: List[ValidationIssue] = []
    
    # ============= Schema Validation Checks =============
    
    # 1. Check database schema
    if schema.database_schema:
        for table in schema.database_schema:
            # Check for primary key
            has_pk = any(f.primary_key for f in table.fields)
            if not has_pk:
                issues.append(ValidationIssue(
                    issue_id=str(uuid.uuid4()),
                    severity="error",
                    category="schema",
                    message=f"Table '{table.table_name}' missing primary key",
                    affected_component=f"table_{table.table_name}",
                    suggestion="Add a 'id' field with primary_key=True"
                ))
            
            # Check for timestamp fields
            field_names = [f.name for f in table.fields]
            if "created_at" not in field_names:
                issues.append(ValidationIssue(
                    issue_id=str(uuid.uuid4()),
                    severity="warning",
                    category="schema",
                    message=f"Table '{table.table_name}' missing 'created_at' field",
                    affected_component=f"table_{table.table_name}",
                    suggestion="Add 'created_at' datetime field for audit trail"
                ))
    
    # 2. Check API schema
    if schema.api_schema:
        # Check for common endpoints
        paths = [e.path for e in schema.api_schema]
        unique_methods_and_paths = {(endpoint.method, endpoint.path) for endpoint in schema.api_schema}

        if len(unique_methods_and_paths) != len(schema.api_schema):
            issues.append(ValidationIssue(
                issue_id=str(uuid.uuid4()),
                severity="error",
                category="schema",
                message="Duplicate API endpoint method/path combinations detected",
                affected_component="api_schema",
                suggestion="Ensure each endpoint method and path combination is unique"
            ))
        
        # Check for authentication endpoints
        has_login = any("/login" in p for p in paths)
        if not has_login:
            issues.append(ValidationIssue(
                issue_id=str(uuid.uuid4()),
                severity="warning",
                category="security",
                message="No authentication endpoint found",
                affected_component="api_schema",
                suggestion="Add POST /auth/login endpoint"
            ))
        
        # Check for role-based access control
        endpoints_with_roles = [e for e in schema.api_schema if e.required_roles]
        if not endpoints_with_roles:
            issues.append(ValidationIssue(
                issue_id=str(uuid.uuid4()),
                severity="warning",
                category="security",
                message="No role-based access control configured",
                affected_component="api_schema",
                suggestion="Add required_roles to protected endpoints"
            ))
        
        # Check API/DB alignment for CRUD routes
        table_names = {table.table_name for table in schema.database_schema}
        for endpoint in schema.api_schema:
            if endpoint.path.startswith("/auth") or endpoint.path.startswith("/dashboard"):
                continue

            matched_table = _table_from_path(endpoint.path)
            if matched_table not in table_names:
                issues.append(ValidationIssue(
                    issue_id=str(uuid.uuid4()),
                    severity="error",
                    category="logic",
                    message=f"API endpoint '{endpoint.path}' has no matching database table",
                    affected_component="api_schema",
                    suggestion=f"Add a '{matched_table}' table or update the endpoint path"
                ))
    
    # 3. Check auth schema
    if schema.auth_schema:
        if schema.auth_schema.get("token_expiry", 0) > 86400:
            issues.append(ValidationIssue(
                issue_id=str(uuid.uuid4()),
                severity="warning",
                category="security",
                message="Token expiry too long (over 24 hours)",
                affected_component="auth_schema",
                suggestion="Reduce token_expiry to 3600-7200 seconds"
            ))
        
        pwd_req = schema.auth_schema.get("password_requirements", {})
        if pwd_req.get("min_length", 0) < 8:
            issues.append(ValidationIssue(
                issue_id=str(uuid.uuid4()),
                severity="error",
                category="security",
                message="Password minimum length too short",
                affected_component="auth_schema",
                suggestion="Set min_length to at least 8"
            ))
    
    # 4. Check UI schema
    if schema.ui_schema:
        if not schema.ui_schema.get("theme"):
            issues.append(ValidationIssue(
                issue_id=str(uuid.uuid4()),
                severity="warning",
                category="logic",
                message="UI theme not specified",
                affected_component="ui_schema",
                suggestion="Specify 'light', 'dark', or 'system' theme"
            ))

        ui_pages = schema.ui_schema.get("pages", [])
        api_paths = {endpoint.path for endpoint in schema.api_schema}
        for page in ui_pages:
            page_api_paths = page.get("api_paths", [])
            for api_path in page_api_paths:
                if api_path not in api_paths:
                    issues.append(ValidationIssue(
                        issue_id=str(uuid.uuid4()),
                        severity="error",
                        category="logic",
                        message=f"UI page '{page.get('name', 'unknown')}' references missing API path '{api_path}'",
                        affected_component="ui_schema",
                        suggestion="Align the UI page action with an existing API endpoint"
                    ))
    
    # 5. Cross-schema validation
    db_tables = {t.table_name for t in schema.database_schema}
    api_paths = {e.path for e in schema.api_schema}
    
    if not db_tables:
        issues.append(ValidationIssue(
            issue_id=str(uuid.uuid4()),
            severity="error",
            category="schema",
            message="No database tables defined",
            affected_component="database_schema",
            suggestion="Generate database schema with at least 'users' table"
        ))
    
    if not api_paths:
        issues.append(ValidationIssue(
            issue_id=str(uuid.uuid4()),
            severity="error",
            category="schema",
            message="No API endpoints defined",
            affected_component="api_schema",
            suggestion="Generate API schema with at least authentication endpoints"
        ))

    # 6. Check role consistency
    auth_roles = set(schema.auth_schema.get("roles", [])) if schema.auth_schema else set()
    for endpoint in schema.api_schema:
        for role in endpoint.required_roles:
            if role not in auth_roles:
                issues.append(ValidationIssue(
                    issue_id=str(uuid.uuid4()),
                    severity="warning",
                    category="security",
                    message=f"Endpoint '{endpoint.path}' requires unknown role '{role}'",
                    affected_component="auth_schema",
                    suggestion="Add the role to auth_schema.roles or remove the endpoint requirement"
                ))
    
    # Determine if schema is valid
    errors = [i for i in issues if i.severity == "error"]
    is_valid = len(errors) == 0
    
    summary = f"Validation complete: {len(errors)} errors, {len(issues) - len(errors)} warnings"
    
    return ValidationResult(
        validation_id=validation_id,
        schema_id=schema.schema_id,
        issues=issues,
        is_valid=is_valid,
        summary=summary
    )
