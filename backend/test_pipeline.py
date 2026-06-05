"""
Simple test to verify the compilation pipeline works
"""

from app.services.intent_extraction import extract_intent
from app.services.system_design import generate_design
from app.services.schema_generator import generate_schema
from app.services.validation_engine import validate_schema
from app.services.repair_engine import repair_schema
from app.services.runtime_simulator import generate_runtime_preview

def test_complete_pipeline():
    """Test the complete 6-stage pipeline"""
    
    # Sample prompt
    prompt = "Build a CRM with login, contacts, dashboard, role-based access, and premium plans"
    
    # Stage 1: Intent Extraction
    intent = extract_intent(prompt)
    assert intent.intent_id
    assert len(intent.entities) > 0
    assert len(intent.features) > 0
    assert len(intent.roles) > 0
    print("✓ Stage 1: Intent Extraction")
    
    # Stage 2: System Design
    design = generate_design(intent)
    assert design.design_id
    assert len(design.modules) > 0
    assert len(design.modules[0].pages) > 0
    print("✓ Stage 2: System Design")
    
    # Stage 3: Schema Generation
    schema = generate_schema(design)
    assert schema.schema_id
    assert len(schema.database_schema) > 0
    assert len(schema.api_schema) > 0
    assert schema.ui_schema
    assert schema.auth_schema
    print("✓ Stage 3: Schema Generation")
    
    # Stage 4: Validation Engine
    validation = validate_schema(schema)
    assert validation.validation_id
    assert validation.schema_id == schema.schema_id
    print(f"✓ Stage 4: Validation Engine ({len(validation.issues)} issues found)")
    
    # Stage 5: Repair Engine
    repair = repair_schema(validation, schema)
    assert repair.repair_id
    assert repair.validation_id == validation.validation_id
    print(f"✓ Stage 5: Repair Engine ({len(repair.patches)} patches generated)")
    
    # Stage 6: Runtime Simulator
    runtime_preview = generate_runtime_preview(schema)
    assert runtime_preview.preview_id
    assert len(runtime_preview.dynamic_forms) > 0
    assert len(runtime_preview.crud_pages) > 0
    assert runtime_preview.sample_data
    assert runtime_preview.preview_html
    print("✓ Stage 6: Runtime Simulator")
    
    print("\n" + "="*50)
    print("✓ ALL STAGES PASSED")
    print("="*50)
    print(f"\nSummary:")
    print(f"  Entities: {len(intent.entities)}")
    print(f"  Features: {len(intent.features)}")
    print(f"  Roles: {len(intent.roles)}")
    print(f"  Modules: {len(design.modules)}")
    print(f"  Database Tables: {len(schema.database_schema)}")
    print(f"  API Endpoints: {len(schema.api_schema)}")
    print(f"  Validation Issues: {len(validation.issues)}")
    print(f"  Repair Patches: {len(repair.patches)}")
    print(f"  Dynamic Forms: {len(runtime_preview.dynamic_forms)}")
    print(f"  CRUD Pages: {len(runtime_preview.crud_pages)}")

if __name__ == '__main__':
    test_complete_pipeline()
