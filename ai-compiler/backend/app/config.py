from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""
    
    # API Settings
    API_TITLE: str = "AI Application Compiler"
    API_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # Database Settings
    DATABASE_URL: str = "sqlite:///./compiler.db"
    POSTGRES_URL: Optional[str] = None
    
    # CORS Settings
    CORS_ORIGINS: list = ["http://localhost:3000", "http://localhost:8000"]
    
    # App Settings
    MAX_COMPILATION_TIME: int = 300  # seconds
    MAX_ARTIFACT_SIZE: int = 10485760  # 10MB
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
