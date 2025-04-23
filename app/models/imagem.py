from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text

from app.core.database import Base


class Imagem(Base):
    __tablename__ = "imagens"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False, unique=True)
    filepath = Column(String(255), nullable=False)
    original_filename = Column(String(255), nullable=False)
    content_type = Column(String(100), nullable=False)
    entidade_tipo = Column(String(50), nullable=False)  # "produto" ou "categoria"
    entidade_id = Column(Integer, nullable=True)  # Pode ser nulo para imagens temporárias
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
