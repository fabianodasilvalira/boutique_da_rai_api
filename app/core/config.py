import os
from pathlib import Path
from typing import Any, Dict, Optional

from pydantic import field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Perfumes API"
    DATABASE_URL: str  # Declare a variável DATABASE_URL

    
    # Database
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///./perfumes.db"
    SQLALCHEMY_TEST_DATABASE_URI: str = "sqlite:///./test.db"
    
    # Para futura migração para PostgreSQL
    POSTGRES_SERVER: Optional[str] = None
    POSTGRES_USER: Optional[str] = None
    POSTGRES_PASSWORD: Optional[str] = None
    POSTGRES_DB: Optional[str] = None
    
    @field_validator("SQLALCHEMY_DATABASE_URI", mode="before")
    def assemble_db_connection(cls, v: Optional[str], info: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        
        postgres_server = info.data.get("POSTGRES_SERVER")
        if postgres_server:
            postgres_user = info.data.get("POSTGRES_USER")
            postgres_password = info.data.get("POSTGRES_PASSWORD")
            postgres_db = info.data.get("POSTGRES_DB")
            
            return f"postgresql://{postgres_user}:{postgres_password}@{postgres_server}/{postgres_db}"
        
        # Fallback para SQLite
        sqlite_db = Path("./perfumes.db").absolute()
        return f"sqlite:///{sqlite_db}"
    
    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
