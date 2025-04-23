from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories.repositories import ContatoRepository
from app.services.services import ContatoService
from app.schemas.schemas import ContatoCreate, ContatoUpdate, ContatoInDB

router = APIRouter(
    prefix="/contatos",
    tags=["contatos"],
    responses={404: {"description": "Contato não encontrado"}}
)


def get_contato_service(db: Session = Depends(get_db)):
    repository = ContatoRepository(db)
    return ContatoService(repository)


@router.get("/", response_model=List[ContatoInDB])
def read_contatos(
    skip: int = 0, 
    limit: int = 100, 
    service: ContatoService = Depends(get_contato_service)
):
    """
    Retorna todos os contatos.
    """
    contatos = service.get_all(skip=skip, limit=limit)
    return contatos


@router.get("/nao-respondidos", response_model=List[ContatoInDB])
def read_contatos_nao_respondidos(
    skip: int = 0, 
    limit: int = 100, 
    service: ContatoService = Depends(get_contato_service)
):
    """
    Retorna contatos não respondidos.
    """
    contatos = service.get_nao_respondidos(skip=skip, limit=limit)
    return contatos


@router.get("/{contato_id}", response_model=ContatoInDB)
def read_contato(
    contato_id: int, 
    service: ContatoService = Depends(get_contato_service)
):
    """
    Retorna um contato específico pelo ID.
    """
    contato = service.get(contato_id)
    if contato is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Contato com ID {contato_id} não encontrado"
        )
    return contato


@router.post("/", response_model=ContatoInDB, status_code=status.HTTP_201_CREATED)
def create_contato(
    contato: ContatoCreate, 
    service: ContatoService = Depends(get_contato_service)
):
    """
    Cria um novo contato.
    """
    return service.create(contato)


@router.put("/{contato_id}", response_model=ContatoInDB)
def update_contato(
    contato_id: int, 
    contato: ContatoUpdate, 
    service: ContatoService = Depends(get_contato_service)
):
    """
    Atualiza um contato existente.
    """
    db_contato = service.update(contato_id, contato)
    if db_contato is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Contato com ID {contato_id} não encontrado"
        )
    return db_contato


@router.put("/{contato_id}/marcar-respondido", response_model=ContatoInDB)
def marcar_contato_como_respondido(
    contato_id: int, 
    service: ContatoService = Depends(get_contato_service)
):
    """
    Marca um contato como respondido.
    """
    db_contato = service.marcar_como_respondido(contato_id)
    if db_contato is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Contato com ID {contato_id} não encontrado"
        )
    return db_contato


@router.delete("/{contato_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_contato(
    contato_id: int, 
    service: ContatoService = Depends(get_contato_service)
):
    """
    Remove um contato.
    """
    success = service.delete(contato_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Contato com ID {contato_id} não encontrado"
        )
    return None
