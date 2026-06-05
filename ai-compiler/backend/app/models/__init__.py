from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class RequirementInput(BaseModel):
    """Input requirements for compilation"""
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=10)
    features: List[str] = Field(default_factory=list)
    constraints: Optional[str] = None
    tech_preferences: Optional[Dict[str, Any]] = None

    class Config:
        json_schema_extra = {
            "example": {
                "title": "E-commerce Platform",
                "description": "Build a modern e-commerce platform with product catalog, shopping cart, and payment processing",
                "features": ["User authentication", "Product search", "Shopping cart", "Payment processing"],
                "constraints": "Must handle 10k concurrent users",
                "tech_preferences": {"frontend": "Next.js", "backend": "FastAPI"}
            }
        }


class IntentExtraction(BaseModel):
    """Extracted intent from requirements"""
    main_intent: str
    sub_intents: List[str]
    entities: Dict[str, Any]
    priority: str  # low, medium, high


class SystemDesign(BaseModel):
    """System design output"""
    architecture: str
    components: List[str]
    data_flow: str
    tech_stack: Dict[str, Any]
    scalability_notes: Optional[str] = None


class SchemaDefinition(BaseModel):
    """Generated schema definition"""
    tables: List[Dict[str, Any]]
    relationships: List[Dict[str, Any]]
    indexes: List[str]
    constraints: List[str]


class ValidationResult(BaseModel):
    """Validation result"""
    is_valid: bool
    errors: List[str] = []
    warnings: List[str] = []
    score: float = 0.0


class RepairAction(BaseModel):
    """Repair action"""
    action_type: str
    target: str
    description: str
    automatic: bool = False


class SimulationResult(BaseModel):
    """Runtime simulation result"""
    success: bool
    output: Optional[str] = None
    errors: List[str] = []
    performance_metrics: Dict[str, Any] = {}


class CompilationRequest(BaseModel):
    """Complete compilation request"""
    requirement: RequirementInput
    include_simulation: bool = True
    include_repairs: bool = True


class CompilationResponse(BaseModel):
    """Complete compilation response"""
    compilation_id: str
    requirement: RequirementInput
    intent: IntentExtraction
    design: SystemDesign
    schema: SchemaDefinition
    validation: ValidationResult
    repairs: List[RepairAction] = []
    simulation: Optional[SimulationResult] = None
    timestamp: datetime
    duration_ms: float
