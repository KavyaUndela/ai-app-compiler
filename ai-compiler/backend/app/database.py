from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings
import os

# Create database URL
if settings.POSTGRES_URL:
    SQLALCHEMY_DATABASE_URL = settings.POSTGRES_URL
else:
    # Use SQLite for local development
    database_path = os.path.join(os.path.dirname(__file__), '../../compiler.db')
    SQLALCHEMY_DATABASE_URL = f"sqlite:///{database_path}"

# Create engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in SQLALCHEMY_DATABASE_URL else {},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Dependency for database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)
