from sqlalchemy import Column, String, DateTime, JSON, Float, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime


class Requirement(Base):
    """Stored requirement"""
    __tablename__ = "requirements"
    
    id = Column(String, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    features = Column(JSON, default=[])
    constraints = Column(Text, nullable=True)
    tech_preferences = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    compilations = relationship("Compilation", back_populates="requirement")


class Compilation(Base):
    """Compilation record"""
    __tablename__ = "compilations"
    
    id = Column(String, primary_key=True, index=True)
    requirement_id = Column(String, ForeignKey("requirements.id"), nullable=False)
    intent_data = Column(JSON)
    design_data = Column(JSON)
    schema_data = Column(JSON)
    validation_data = Column(JSON)
    repairs_data = Column(JSON, default=[])
    simulation_data = Column(JSON, nullable=True)
    duration_ms = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    status = Column(String(20), default="completed")  # pending, in_progress, completed, failed
    
    requirement = relationship("Requirement", back_populates="compilations")
    artifacts = relationship("Artifact", back_populates="compilation")
    metrics = relationship("Metric", back_populates="compilation")


class Artifact(Base):
    """Generated artifact"""
    __tablename__ = "artifacts"
    
    id = Column(String, primary_key=True, index=True)
    compilation_id = Column(String, ForeignKey("compilations.id"), nullable=False)
    artifact_type = Column(String(50))  # config, code, schema, doc
    content = Column(Text)
    filename = Column(String(255))
    size_bytes = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    compilation = relationship("Compilation", back_populates="artifacts")


class Metric(Base):
    """Compilation metrics"""
    __tablename__ = "metrics"
    
    id = Column(String, primary_key=True, index=True)
    compilation_id = Column(String, ForeignKey("compilations.id"), nullable=False)
    metric_name = Column(String(100))
    metric_value = Column(Float)
    unit = Column(String(50))
    recorded_at = Column(DateTime, default=datetime.utcnow)
    
    compilation = relationship("Compilation", back_populates="metrics")
