from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import CompilationRequest, CompilationResponse, RequirementInput
from app.services.intent_extractor import IntentExtractor
from app.services.designer import Designer
from app.services.schema_generator import SchemaGenerator
from app.services.validator import Validator
from app.services.repair_engine import RepairEngine
from app.services.simulator import Simulator
from app.schemas import Requirement, Compilation
import uuid
import time
from datetime import datetime

router = APIRouter(prefix="/api/compile", tags=["compilation"])


@router.post("/", response_model=CompilationResponse)
async def compile(request: CompilationRequest, db: Session = Depends(get_db)):
    """Compile requirements into application configuration"""
    
    start_time = time.time()
    compilation_id = str(uuid.uuid4())
    
    try:
        # Store requirement
        req_record = Requirement(
            id=str(uuid.uuid4()),
            title=request.requirement.title,
            description=request.requirement.description,
            features=request.requirement.features,
            constraints=request.requirement.constraints,
            tech_preferences=request.requirement.tech_preferences
        )
        db.add(req_record)
        db.commit()
        
        # Stage 1: Intent Extraction
        intent = IntentExtractor.extract(request.requirement)
        
        # Stage 2: System Design
        design = Designer.design(intent)
        
        # Stage 3: Schema Generation
        schema = SchemaGenerator.generate(design)
        
        # Stage 4: Validation
        validation = Validator.validate(schema)
        
        # Stage 5: Repair (if validation failed)
        repairs = []
        if request.include_repairs and not validation.is_valid:
            repairs = RepairEngine.repair(validation)
        
        # Stage 6: Simulation
        simulation = None
        if request.include_simulation:
            simulation = Simulator.simulate(schema)
        
        duration_ms = (time.time() - start_time) * 1000
        
        # Store compilation record
        comp_record = Compilation(
            id=compilation_id,
            requirement_id=req_record.id,
            intent_data=intent.dict(),
            design_data=design.dict(),
            schema_data=schema.dict(),
            validation_data=validation.dict(),
            repairs_data=[r.dict() for r in repairs],
            simulation_data=simulation.dict() if simulation else None,
            duration_ms=duration_ms,
            status="completed"
        )
        db.add(comp_record)
        db.commit()
        
        return CompilationResponse(
            compilation_id=compilation_id,
            requirement=request.requirement,
            intent=intent,
            design=design,
            schema=schema,
            validation=validation,
            repairs=repairs,
            simulation=simulation,
            timestamp=datetime.utcnow(),
            duration_ms=duration_ms
        )
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{compilation_id}", response_model=CompilationResponse)
async def get_compilation(compilation_id: str, db: Session = Depends(get_db)):
    """Get compilation by ID"""
    
    comp = db.query(Compilation).filter(Compilation.id == compilation_id).first()
    if not comp:
        raise HTTPException(status_code=404, detail="Compilation not found")
    
    req = db.query(Requirement).filter(Requirement.id == comp.requirement_id).first()
    
    return CompilationResponse(
        compilation_id=comp.id,
        requirement=RequirementInput(**req.dict()),
        intent=comp.intent_data,
        design=comp.design_data,
        schema=comp.schema_data,
        validation=comp.validation_data,
        repairs=comp.repairs_data,
        simulation=comp.simulation_data,
        timestamp=comp.created_at,
        duration_ms=comp.duration_ms
    )


@router.get("")
async def list_compilations(db: Session = Depends(get_db)):
    """List all compilations"""
    
    compilations = db.query(Compilation).order_by(Compilation.created_at.desc()).limit(50).all()
    return {
        "total": len(compilations),
        "compilations": [
            {
                "id": c.id,
                "title": db.query(Requirement).filter(Requirement.id == c.requirement_id).first().title,
                "status": c.status,
                "created_at": c.created_at,
                "duration_ms": c.duration_ms
            }
            for c in compilations
        ]
    }
