"""
Stage 5: Repair Engine Service
Automatically repairs invalid sections of generated schemas.
"""

from copy import deepcopy
import uuid
from typing import List
from app.models import RepairPatch, RepairResult, SchemaGenerationResult, ValidationResult

def repair_schema(validation: ValidationResult, schema: SchemaGenerationResult) -> RepairResult:
    """Automatically repair invalid sections of the schema."""
    
    repair_id = str(uuid.uuid4())
    patches: List[RepairPatch] = []
    
    # Process each validation issue and generate repairs
    for issue in validation.issues:
        if issue.severity == "error":
            # Generate a repair patch
            patch = None
            
            if "primary key" in issue.message.lower():
                patch = RepairPatch(
                    patch_id=str(uuid.uuid4()),
                    affected_component=issue.affected_component,
                    original_value="missing",
                    fixed_value="id UUID PRIMARY KEY",
                    explanation="Added UUID primary key to table",
                    confidence=0.95
                )
            
            elif "missing" in issue.message.lower() and "endpoint" in issue.message.lower():
                patch = RepairPatch(
                    patch_id=str(uuid.uuid4()),
                    affected_component=issue.affected_component,
                    original_value="missing",
                    fixed_value="POST /auth/login",
                    explanation="Added authentication endpoint",
                    confidence=0.90
                )
            
            elif "password" in issue.message.lower():
                patch = RepairPatch(
                    patch_id=str(uuid.uuid4()),
                    affected_component=issue.affected_component,
                    original_value=f"min_length: 6",
                    fixed_value="min_length: 8",
                    explanation="Increased password minimum length to 8 characters",
                    confidence=0.99
                )
            
            elif "token" in issue.message.lower():
                patch = RepairPatch(
                    patch_id=str(uuid.uuid4()),
                    affected_component=issue.affected_component,
                    original_value=f"token_expiry: 86400",
                    fixed_value="token_expiry: 3600",
                    explanation="Reduced token expiry from 24h to 1h for better security",
                    confidence=0.85
                )
            
            if patch:
                patches.append(patch)
        
        elif issue.severity == "warning":
            # Generate suggestion patches for warnings
            if "created_at" in issue.message.lower():
                patch = RepairPatch(
                    patch_id=str(uuid.uuid4()),
                    affected_component=issue.affected_component,
                    original_value="missing",
                    fixed_value="created_at DATETIME",
                    explanation="Added created_at timestamp field for audit",
                    confidence=0.88
                )
                patches.append(patch)
            
            elif "versioning" in issue.message.lower():
                patch = RepairPatch(
                    patch_id=str(uuid.uuid4()),
                    affected_component=issue.affected_component,
                    original_value="/auth/login",
                    fixed_value="/v1/auth/login",
                    explanation="Added API versioning prefix to all endpoints",
                    confidence=0.80
                )
                patches.append(patch)
            
            elif "theme" in issue.message.lower():
                patch = RepairPatch(
                    patch_id=str(uuid.uuid4()),
                    affected_component=issue.affected_component,
                    original_value="missing",
                    fixed_value="light",
                    explanation="Set default UI theme to light mode",
                    confidence=0.92
                )
                patches.append(patch)
    
    # Create repaired schema by fixing the most common invalid sections.
    repaired_schema = deepcopy(schema)
    if not validation.is_valid:
        existing_tables = {table.table_name: table for table in repaired_schema.database_schema}
        existing_paths = {endpoint.path for endpoint in repaired_schema.api_schema}

        for issue in validation.issues:
            message = issue.message.lower()

            if "primary key" in message:
                table_name = issue.affected_component.replace("table_", "")
                table = existing_tables.get(table_name)
                if table and not any(field.primary_key for field in table.fields):
                    table.fields.insert(0, table.fields[0].model_copy(update={"name": "id", "field_type": "uuid", "primary_key": True}))

            if "missing database table" in message:
                path = issue.message.split("'")[1] if "'" in issue.message else "items"
                table_name = path.strip("/").split("/")[0]
                if table_name not in existing_tables:
                    repaired_schema.database_schema.append(
                        repaired_schema.database_schema[0].model_copy(update={"table_name": table_name, "fields": repaired_schema.database_schema[0].fields})
                    )
                    existing_tables[table_name] = repaired_schema.database_schema[-1]

            if "missing api path" in message and "ui page" in message:
                path = issue.message.split("'")[-2] if "'" in issue.message else "/health"
                if path not in existing_paths:
                    repaired_schema.api_schema.append(
                        repaired_schema.api_schema[0].model_copy(update={"path": path, "description": f"Auto-repaired endpoint for {path}"})
                    )
                    existing_paths.add(path)

            if "theme" in message:
                repaired_schema.ui_schema["theme"] = "light"

            if "token" in message:
                repaired_schema.auth_schema["token_expiry"] = 3600

            if "password" in message:
                repaired_schema.auth_schema.setdefault("password_requirements", {})["min_length"] = 8

        # Ensure auth endpoints exist for runtime preview.
        if not any(endpoint.path == "/auth/login" for endpoint in repaired_schema.api_schema):
            repaired_schema.api_schema.append(
                repaired_schema.api_schema[0].model_copy(update={"method": "POST", "path": "/auth/login", "description": "Auto-added login endpoint"})
            )
    
    summary = f"Generated {len(patches)} repair patches: {len([p for p in patches if p.confidence > 0.9])} high confidence, {len([p for p in patches if p.confidence <= 0.9])} standard"
    
    return RepairResult(
        repair_id=repair_id,
        validation_id=validation.validation_id,
        patches=patches,
        repaired_schema=repaired_schema,
        summary=summary
    )
