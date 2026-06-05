from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum

# ============= Input & Output Models =============

class GenerateRequest(BaseModel):
    prompt: str = Field(..., description="Natural language requirement")
    
class Entity(BaseModel):
    name: str
    entity_type: str  # "user", "data_object", "system"
    description: Optional[str] = None
    
class Feature(BaseModel):
    name: str
    description: str
    related_entities: List[str] = []
    
class Role(BaseModel):
    name: str
    permissions: List[str] = []
    description: Optional[str] = None

class IntentSchema(BaseModel):
    intent_id: str
    entities: List[Entity]
    features: List[Feature]
    roles: List[Role]
    workflows: List[str]
    summary: str

# ============= System Design Models =============

class PageSchema(BaseModel):
    name: str
    component_type: str  # "form", "list", "detail", "dashboard"
    fields: List[str]
    required_roles: List[str] = []

class Module(BaseModel):
    name: str
    pages: List[PageSchema]
    functions: List[str]

class SystemDesignSchema(BaseModel):
    design_id: str
    modules: List[Module]
    navigation: Dict[str, List[str]]
    auth_flow: str
    user_workflows: List[str]
    summary: str

# ============= Database Schema Models =============

class DatabaseField(BaseModel):
    name: str
    field_type: str  # "string", "integer", "datetime", "uuid", "boolean"
    nullable: bool = False
    primary_key: bool = False
    unique: bool = False

class DatabaseTable(BaseModel):
    table_name: str
    fields: List[DatabaseField]
    indexes: List[str] = []

class APIEndpoint(BaseModel):
    method: str  # "GET", "POST", "PUT", "DELETE"
    path: str
    description: str
    required_roles: List[str] = []
    request_body: Optional[Dict[str, Any]] = None
    response_body: Dict[str, Any]

class SchemaGenerationResult(BaseModel):
    schema_id: str
    database_schema: List[DatabaseTable]
    api_schema: List[APIEndpoint]
    ui_schema: Dict[str, Any]
    auth_schema: Dict[str, Any]

# ============= Validation Models =============

class ValidationIssue(BaseModel):
    issue_id: str
    severity: str  # "error", "warning"
    category: str  # "schema", "logic", "security", "performance"
    message: str
    affected_component: str
    suggestion: Optional[str] = None

class ValidationResult(BaseModel):
    validation_id: str
    schema_id: str
    issues: List[ValidationIssue]
    is_valid: bool
    summary: str

# ============= Repair Models =============

class RepairPatch(BaseModel):
    patch_id: str
    affected_component: str
    original_value: Any
    fixed_value: Any
    explanation: str
    confidence: float  # 0.0 to 1.0

class RepairResult(BaseModel):
    repair_id: str
    validation_id: str
    patches: List[RepairPatch]
    repaired_schema: Optional[SchemaGenerationResult] = None
    summary: str

# ============= Runtime Preview Models =============

class FormField(BaseModel):
    name: str
    label: str
    field_type: str
    required: bool = False
    options: Optional[List[str]] = None

class FormSchema(BaseModel):
    form_id: str
    title: str
    description: str
    fields: List[FormField]
    submit_action: str

class CRUDPage(BaseModel):
    page_id: str
    entity_name: str
    list_columns: List[str]
    create_form: FormSchema
    edit_form: FormSchema
    delete_confirmation: str

class RuntimePreview(BaseModel):
    preview_id: str
    schema_id: str
    dynamic_forms: List[FormSchema]
    crud_pages: List[CRUDPage]
    preview_html: Optional[str] = None
    sample_data: Dict[str, List[Any]]

# ============= Compilation Pipeline Result =============

class CompilationResult(BaseModel):
    compilation_id: str
    original_prompt: str
    intent: IntentSchema
    design: SystemDesignSchema
    schema: SchemaGenerationResult
    validation: ValidationResult
    repair: Optional[RepairResult] = None
    runtime_preview: RuntimePreview
    status: str  # "completed", "partial", "failed"
    summary: str
