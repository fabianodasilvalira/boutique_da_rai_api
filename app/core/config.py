import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Perfumes API"
    API_V1_STR: str = "/api/v1"
    
    # Configuração do banco de dados
    DATABASE_URL: str = "sqlite:///./perfumes.db"
    
    # Flag para usar PostgreSQL
    USE_POSTGRES: bool = os.getenv("USE_POSTGRES", "False").lower() in ("true", "1", "t")
    
    # Configuração para PostgreSQL
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "db")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "perfumes_db")
    
    # Configuração para upload de arquivos
    UPLOAD_DIR: str = os.path.join(os.getcwd(), "uploads")
    MAX_UPLOAD_SIZE: int = 5 * 1024 * 1024  # 5MB
    
    # Configuração JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "CHAVE_SECRETA_TEMPORARIA_DEVE_SER_SUBSTITUIDA_EM_PRODUCAO")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    class Config:
        env_file = ".env"


settings = Settings()
