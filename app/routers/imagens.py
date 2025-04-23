from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import os
import shutil
from typing import Optional
from uuid import uuid4

from app.core.database import get_db
from app.core.config import settings
from app.repositories.repositories import ImagemRepository
from app.services.services import ImagemService
from app.schemas.schemas import ImagemCreate, ImagemInDB

router = APIRouter(
    prefix="/imagens",
    tags=["imagens"],
    responses={404: {"description": "Imagem não encontrada"}}
)

# Garantir que o diretório de uploads existe
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)


def get_imagem_service(db: Session = Depends(get_db)):
    repository = ImagemRepository(db)
    return ImagemService(repository)


@router.post("/upload", response_model=ImagemInDB, status_code=status.HTTP_201_CREATED)
async def upload_imagem(
    file: UploadFile = File(...),
    entidade_tipo: str = Form(...),  # "produto" ou "categoria"
    entidade_id: Optional[int] = Form(None),
    service: ImagemService = Depends(get_imagem_service)
):
    """
    Faz upload de uma imagem para produto ou categoria.
    
    - **file**: Arquivo de imagem
    - **entidade_tipo**: Tipo de entidade ("produto" ou "categoria")
    - **entidade_id**: ID da entidade (opcional, pode ser nulo para imagens temporárias)
    """
    # Validar tipo de arquivo
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Arquivo enviado não é uma imagem válida"
        )
    
    # Validar tipo de entidade
    if entidade_tipo not in ["produto", "categoria"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tipo de entidade inválido. Use 'produto' ou 'categoria'"
        )
    
    # Gerar nome único para o arquivo
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid4()}{file_extension}"
    file_path = os.path.join(settings.UPLOAD_DIR, unique_filename)
    
    # Salvar arquivo
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao salvar arquivo: {str(e)}"
        )
    finally:
        file.file.close()
    
    # Criar registro no banco de dados
    imagem_data = ImagemCreate(
        filename=unique_filename,
        filepath=file_path,
        original_filename=file.filename,
        content_type=file.content_type,
        entidade_tipo=entidade_tipo,
        entidade_id=entidade_id
    )
    
    return service.create(imagem_data)


@router.get("/{imagem_id}", response_class=FileResponse)
def get_imagem(
    imagem_id: int,
    service: ImagemService = Depends(get_imagem_service)
):
    """
    Retorna uma imagem pelo ID.
    """
    imagem = service.get(imagem_id)
    if imagem is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Imagem com ID {imagem_id} não encontrada"
        )
    
    if not os.path.exists(imagem.filepath):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Arquivo de imagem não encontrado no servidor"
        )
    
    return FileResponse(
        imagem.filepath, 
        media_type=imagem.content_type,
        filename=imagem.original_filename
    )


@router.get("/entidade/{tipo}/{id}", response_model=list[ImagemInDB])
def get_imagens_por_entidade(
    tipo: str,
    id: int,
    service: ImagemService = Depends(get_imagem_service)
):
    """
    Retorna todas as imagens associadas a uma entidade.
    
    - **tipo**: Tipo de entidade ("produto" ou "categoria")
    - **id**: ID da entidade
    """
    if tipo not in ["produto", "categoria"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tipo de entidade inválido. Use 'produto' ou 'categoria'"
        )
    
    return service.get_by_entidade(tipo, id)


@router.delete("/{imagem_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_imagem(
    imagem_id: int,
    service: ImagemService = Depends(get_imagem_service)
):
    """
    Remove uma imagem.
    """
    imagem = service.get(imagem_id)
    if imagem is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Imagem com ID {imagem_id} não encontrada"
        )
    
    # Remover arquivo físico
    try:
        if os.path.exists(imagem.filepath):
            os.remove(imagem.filepath)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao remover arquivo: {str(e)}"
        )
    
    # Remover registro do banco de dados
    success = service.delete(imagem_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao remover registro da imagem"
        )
    
    return None


@router.put("/{imagem_id}/associar/{tipo}/{entidade_id}", response_model=ImagemInDB)
def associar_imagem(
    imagem_id: int,
    tipo: str,
    entidade_id: int,
    service: ImagemService = Depends(get_imagem_service)
):
    """
    Associa uma imagem existente a uma entidade.
    
    - **imagem_id**: ID da imagem
    - **tipo**: Tipo de entidade ("produto" ou "categoria")
    - **entidade_id**: ID da entidade
    """
    if tipo not in ["produto", "categoria"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tipo de entidade inválido. Use 'produto' ou 'categoria'"
        )
    
    imagem = service.associar_entidade(imagem_id, tipo, entidade_id)
    if imagem is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Imagem com ID {imagem_id} não encontrada"
        )
    
    return imagem
