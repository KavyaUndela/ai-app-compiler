from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas import Requirement, Compilation
import uuid
from datetime import datetime

def seed_database():
    """Seed database with sample data"""
    db = SessionLocal()
    
    try:
        # Check if data exists
        existing = db.query(Requirement).count()
        if existing > 0:
            print("Database already seeded")
            return
        
        # Create sample requirements
        requirements = [
            Requirement(
                id=str(uuid.uuid4()),
                title="E-commerce Platform",
                description="Build a modern e-commerce platform with product catalog, shopping cart, and payment processing",
                features=["User authentication", "Product search", "Shopping cart", "Payment processing", "Order tracking"],
                constraints="Must handle 10k concurrent users",
                tech_preferences={"frontend": "Next.js", "backend": "FastAPI", "database": "PostgreSQL"}
            ),
            Requirement(
                id=str(uuid.uuid4()),
                title="Blog Management System",
                description="Create a blog platform with post management, comments, and analytics",
                features=["Create/Edit posts", "Comment system", "User roles", "Analytics"],
                constraints="Low latency required for user interactions",
                tech_preferences={"frontend": "Next.js", "backend": "FastAPI"}
            ),
            Requirement(
                id=str(uuid.uuid4()),
                title="Task Management App",
                description="Develop a collaborative task management application",
                features=["Create tasks", "Team collaboration", "Real-time updates", "File attachments"],
                constraints=None,
                tech_preferences={"frontend": "Next.js", "backend": "FastAPI"}
            )
        ]
        
        for req in requirements:
            db.add(req)
        
        db.commit()
        
        # Create sample compilations
        for req in requirements:
            comp = Compilation(
                id=str(uuid.uuid4()),
                requirement_id=req.id,
                intent_data={
                    "main_intent": req.title.lower(),
                    "sub_intents": req.features[:2],
                    "priority": "high"
                },
                design_data={
                    "architecture": "Microservices",
                    "components": ["API Gateway", "Service Router", "Database"],
                    "tech_stack": req.tech_preferences or {}
                },
                schema_data={
                    "tables": 3,
                    "relationships": 2,
                    "indexes": 5
                },
                validation_data={
                    "is_valid": True,
                    "score": 0.95
                },
                repairs_data=[],
                simulation_data={
                    "success": True,
                    "performance_metrics": {
                        "avg_query_time_ms": 45,
                        "throughput_rps": 1000
                    }
                },
                duration_ms=1250,
                status="completed"
            )
            db.add(comp)
        
        db.commit()
        print("✅ Database seeded with sample data")
        
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
