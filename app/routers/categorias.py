from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories.repositories import CategoriaRepository
from app.services.services import CategoriaService
from app.schemas.schemas import CategoriaCreate, CategoriaUpdate, CategoriaInDB, CategoriaWithProdutos

router = APIRouter(
    prefix="/categorias",
    tags=["categorias"],
    responses={404: {"description": "Categoria não encontrada"}}
)


def get_categoria_service(db: Session = Depends(get_db)):
    repository = CategoriaRepository(db)
    return CategoriaService(repository)


@router.get("/", response_model=List[CategoriaInDB])
def read_categorias(
    skip: int = 0, 
    limit: int = 100, 
    service: CategoriaService = Depends(get_categoria_service)
):
    """
    Retorna todas as categorias.
    """
    categorias = service.get_all(skip=skip, limit=limit)
    return categorias


@router.get("/{categoria_id}", response_model=CategoriaInDB)
def read_categoria(
    categoria_id: int, 
    service: CategoriaService = Depends(get_categoria_service)
):
    """
    Retorna uma categoria específica pelo ID.
    """
    categoria = service.get(categoria_id)
    if categoria is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Categoria com ID {categoria_id} não encontrada"
        )
    return categoria


@router.get("/slug/{slug}", response_model=CategoriaInDB)
def read_categoria_by_slug(
    slug: str, 
    service: CategoriaService = Depends(get_categoria_service)
):
    """
    Retorna uma categoria específica pelo slug.
    """
    categoria = service.get_by_slug(slug)
    if categoria is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Categoria com slug '{slug}' não encontrada"
        )
    return categoria


@router.post("/", response_model=CategoriaInDB, status_code=status.HTTP_201_CREATED)
def create_categoria(
    categoria: CategoriaCreate, 
    service: CategoriaService = Depends(get_categoria_service)
):
    """
    Cria uma nova categoria.
    """
    return service.create(categoria)


@router.put("/{categoria_id}", response_model=CategoriaInDB)
def update_categoria(
    categoria_id: int, 
    categoria: CategoriaUpdate, 
    service: CategoriaService = Depends(get_categoria_service)
):
    """
    Atualiza uma categoria existente.
    """
    db_categoria = service.update(categoria_id, categoria)
    if db_categoria is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Categoria com ID {categoria_id} não encontrada"
        )
    return db_categoria


@router.delete("/{categoria_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_categoria(
    categoria_id: int, 
    service: CategoriaService = Depends(get_categoria_service)
):
    """
    Remove uma categoria.
    """
    success = service.delete(categoria_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Categoria com ID {categoria_id} não encontrada"
        )
    return None
