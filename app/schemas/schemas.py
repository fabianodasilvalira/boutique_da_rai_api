from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr


# Base Schemas
class CategoriaBase(BaseModel):
    nome: str
    descricao: Optional[str] = None
    imagem_url: Optional[str] = None
    slug: str


class ProdutoBase(BaseModel):
    nome: str
    descricao: Optional[str] = None
    preco: float = Field(gt=0)
    imagem_url: Optional[str] = None
    categoria_id: int
    destaque: bool = False
    estoque: int = 0


class QuizPerguntaBase(BaseModel):
    pergunta: str
    ordem: int


class QuizOpcaoBase(BaseModel):
    pergunta_id: int
    texto: str
    valor_id: str
    imagem_url: Optional[str] = None


class QuizResultadoBase(BaseModel):
    nome: str
    descricao: Optional[str] = None
    recomendacao: Optional[str] = None
    imagem_url: Optional[str] = None
    produto_recomendado_id: Optional[int] = None


class QuizRegraBase(BaseModel):
    combinacao_respostas: dict
    resultado_id: int


class ContatoBase(BaseModel):
    nome: str
    email: EmailStr
    telefone: Optional[str] = None
    assunto: Optional[str] = None
    mensagem: str


class UsuarioBase(BaseModel):
    nome: str
    email: EmailStr
    ativo: bool = True


# Create Schemas
class CategoriaCreate(CategoriaBase):
    pass


class ProdutoCreate(ProdutoBase):
    pass


class QuizPerguntaCreate(QuizPerguntaBase):
    pass


class QuizOpcaoCreate(QuizOpcaoBase):
    pass


class QuizResultadoCreate(QuizResultadoBase):
    pass


class QuizRegraCreate(QuizRegraBase):
    pass


class ContatoCreate(ContatoBase):
    pass


class UsuarioCreate(UsuarioBase):
    senha: str


# Update Schemas
class CategoriaUpdate(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    imagem_url: Optional[str] = None
    slug: Optional[str] = None


class ProdutoUpdate(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    preco: Optional[float] = None
    imagem_url: Optional[str] = None
    categoria_id: Optional[int] = None
    destaque: Optional[bool] = None
    estoque: Optional[int] = None


class QuizPerguntaUpdate(BaseModel):
    pergunta: Optional[str] = None
    ordem: Optional[int] = None


class QuizOpcaoUpdate(BaseModel):
    pergunta_id: Optional[int] = None
    texto: Optional[str] = None
    valor_id: Optional[str] = None
    imagem_url: Optional[str] = None


class QuizResultadoUpdate(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    recomendacao: Optional[str] = None
    imagem_url: Optional[str] = None
    produto_recomendado_id: Optional[int] = None


class QuizRegraUpdate(BaseModel):
    combinacao_respostas: Optional[dict] = None
    resultado_id: Optional[int] = None


class ContatoUpdate(BaseModel):
    respondido: Optional[bool] = None


class UsuarioUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    ativo: Optional[bool] = None
    senha: Optional[str] = None


# Response Schemas
class CategoriaInDB(CategoriaBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProdutoInDB(ProdutoBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class QuizPerguntaInDB(QuizPerguntaBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class QuizOpcaoInDB(QuizOpcaoBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class QuizResultadoInDB(QuizResultadoBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class QuizRegraInDB(QuizRegraBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ContatoInDB(ContatoBase):
    id: int
    respondido: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UsuarioInDB(UsuarioBase):
    id: int
    created_at: datetime
    ultimo_acesso: Optional[datetime] = None

    class Config:
        from_attributes = True


# Response Schemas with Relationships
class ProdutoWithCategoria(ProdutoInDB):
    categoria: CategoriaInDB


class CategoriaWithProdutos(CategoriaInDB):
    produtos: List[ProdutoInDB] = []


class QuizPerguntaWithOpcoes(QuizPerguntaInDB):
    opcoes: List[QuizOpcaoInDB] = []


class QuizResultadoWithProduto(QuizResultadoInDB):
    produto_recomendado: Optional[ProdutoInDB] = None


# Token Schema
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
