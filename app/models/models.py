from datetime import datetime
from typing import Optional, List
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship

from app.core.database import Base


class Categoria(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    descricao = Column(String(255))
    imagem_url = Column(String(255))
    slug = Column(String(100), unique=True, index=True)
    
    # Relacionamentos
    produtos = relationship("Produto", back_populates="categoria")
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    descricao = Column(String(255))
    preco = Column(Float, nullable=False)
    imagem_url = Column(String(255))
    categoria_id = Column(Integer, ForeignKey("categorias.id"))
    destaque = Column(Boolean, default=False)
    estoque = Column(Integer, default=0)
    
    # Relacionamentos
    categoria = relationship("Categoria", back_populates="produtos")
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class QuizPergunta(Base):
    __tablename__ = "quiz_perguntas"

    id = Column(Integer, primary_key=True, index=True)
    pergunta = Column(String(255), nullable=False)
    ordem = Column(Integer, nullable=False)
    
    # Relacionamentos
    opcoes = relationship("QuizOpcao", back_populates="pergunta")
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class QuizOpcao(Base):
    __tablename__ = "quiz_opcoes"

    id = Column(Integer, primary_key=True, index=True)
    pergunta_id = Column(Integer, ForeignKey("quiz_perguntas.id"))
    texto = Column(String(255), nullable=False)
    valor_id = Column(String(50), nullable=False)
    imagem_url = Column(String(255))
    
    # Relacionamentos
    pergunta = relationship("QuizPergunta", back_populates="opcoes")
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class QuizResultado(Base):
    __tablename__ = "quiz_resultados"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    descricao = Column(String(255))
    recomendacao = Column(String(255))
    imagem_url = Column(String(255))
    produto_recomendado_id = Column(Integer, ForeignKey("produtos.id"), nullable=True)
    
    # Relacionamentos
    produto_recomendado = relationship("Produto")
    regras = relationship("QuizRegra", back_populates="resultado")
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class QuizRegra(Base):
    __tablename__ = "quiz_regras"

    id = Column(Integer, primary_key=True, index=True)
    combinacao_respostas = Column(JSON)
    resultado_id = Column(Integer, ForeignKey("quiz_resultados.id"))
    
    # Relacionamentos
    resultado = relationship("QuizResultado", back_populates="regras")
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Contato(Base):
    __tablename__ = "contatos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    telefone = Column(String(20))
    assunto = Column(String(100))
    mensagem = Column(Text, nullable=False)
    respondido = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True, index=True)
    senha_hash = Column(String(255), nullable=False)
    ativo = Column(Boolean, default=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    ultimo_acesso = Column(DateTime, nullable=True)
