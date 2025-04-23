from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories.repositories import ProdutoRepository
from app.services.services import ProdutoService
from app.schemas.schemas import ProdutoCreate, ProdutoUpdate, ProdutoInDB, ProdutoWithCategoria

router = APIRouter(
    prefix="/produtos",
    tags=["produtos"],
    responses={404: {"description": "Produto não encontrado"}}
)


def get_produto_service(db: Session = Depends(get_db)):
    repository = ProdutoRepository(db)
    return ProdutoService(repository)


@router.get("/", response_model=List[ProdutoInDB])
def read_produtos(
    skip: int = 0, 
    limit: int = 100, 
    service: ProdutoService = Depends(get_produto_service)
):
    """
    Retorna todos os produtos.
    """
    produtos = service.get_all(skip=skip, limit=limit)
    return produtos


@router.get("/destaques", response_model=List[ProdutoInDB])
def read_produtos_destaques(
    skip: int = 0, 
    limit: int = 100, 
    service: ProdutoService = Depends(get_produto_service)
):
    """
    Retorna produtos em destaque.
    """
    produtos = service.get_destaques(skip=skip, limit=limit)
    return produtos


@router.get("/categoria/{categoria_id}", response_model=List[ProdutoInDB])
def read_produtos_by_categoria(
    categoria_id: int,
    skip: int = 0, 
    limit: int = 100, 
    service: ProdutoService = Depends(get_produto_service)
):
    """
    Retorna produtos de uma categoria específica.
    """
    produtos = service.get_by_categoria(categoria_id, skip=skip, limit=limit)
    return produtos


@router.get("/{produto_id}", response_model=ProdutoInDB)
def read_produto(
    produto_id: int, 
    service: ProdutoService = Depends(get_produto_service)
):
    """
    Retorna um produto específico pelo ID.
    """
    produto = service.get(produto_id)
    if produto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Produto com ID {produto_id} não encontrado"
        )
    return produto


@router.post("/", response_model=ProdutoInDB, status_code=status.HTTP_201_CREATED)
def create_produto(
    produto: ProdutoCreate, 
    service: ProdutoService = Depends(get_produto_service)
):
    """
    Cria um novo produto.
    """
    return service.create(produto)


@router.put("/{produto_id}", response_model=ProdutoInDB)
def update_produto(
    produto_id: int, 
    produto: ProdutoUpdate, 
    service: ProdutoService = Depends(get_produto_service)
):
    """
    Atualiza um produto existente.
    """
    db_produto = service.update(produto_id, produto)
    if db_produto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Produto com ID {produto_id} não encontrado"
        )
    return db_produto


@router.delete("/{produto_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_produto(
    produto_id: int, 
    service: ProdutoService = Depends(get_produto_service)
):
    """
    Remove um produto.
    """
    success = service.delete(produto_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Produto com ID {produto_id} não encontrado"
        )
    return None
