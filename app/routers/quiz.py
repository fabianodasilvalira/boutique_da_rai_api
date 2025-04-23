from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories.repositories import QuizPerguntaRepository, QuizOpcaoRepository, QuizResultadoRepository, QuizRegraRepository
from app.services.services import QuizPerguntaService, QuizOpcaoService, QuizResultadoService, QuizRegraService
from app.schemas.schemas import (
    QuizPerguntaCreate, QuizPerguntaUpdate, QuizPerguntaInDB, QuizPerguntaWithOpcoes,
    QuizOpcaoCreate, QuizOpcaoUpdate, QuizOpcaoInDB,
    QuizResultadoCreate, QuizResultadoUpdate, QuizResultadoInDB, QuizResultadoWithProduto,
    QuizRegraCreate, QuizRegraUpdate, QuizRegraInDB
)

router = APIRouter(
    prefix="/quiz",
    tags=["quiz"],
    responses={404: {"description": "Item não encontrado"}}
)


def get_pergunta_service(db: Session = Depends(get_db)):
    repository = QuizPerguntaRepository(db)
    return QuizPerguntaService(repository)


def get_opcao_service(db: Session = Depends(get_db)):
    repository = QuizOpcaoRepository(db)
    return QuizOpcaoService(repository)


def get_resultado_service(db: Session = Depends(get_db)):
    repository = QuizResultadoRepository(db)
    return QuizResultadoService(repository)


def get_regra_service(db: Session = Depends(get_db)):
    repository = QuizRegraRepository(db)
    return QuizRegraService(repository)


# Rotas para Perguntas
@router.get("/perguntas/", response_model=List[QuizPerguntaInDB])
def read_perguntas(
    skip: int = 0, 
    limit: int = 100, 
    service: QuizPerguntaService = Depends(get_pergunta_service)
):
    """
    Retorna todas as perguntas do quiz.
    """
    perguntas = service.get_all(skip=skip, limit=limit)
    return perguntas


@router.get("/perguntas/{pergunta_id}", response_model=QuizPerguntaInDB)
def read_pergunta(
    pergunta_id: int, 
    service: QuizPerguntaService = Depends(get_pergunta_service)
):
    """
    Retorna uma pergunta específica pelo ID.
    """
    pergunta = service.get(pergunta_id)
    if pergunta is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pergunta com ID {pergunta_id} não encontrada"
        )
    return pergunta


@router.post("/perguntas/", response_model=QuizPerguntaInDB, status_code=status.HTTP_201_CREATED)
def create_pergunta(
    pergunta: QuizPerguntaCreate, 
    service: QuizPerguntaService = Depends(get_pergunta_service)
):
    """
    Cria uma nova pergunta.
    """
    return service.create(pergunta)


@router.put("/perguntas/{pergunta_id}", response_model=QuizPerguntaInDB)
def update_pergunta(
    pergunta_id: int, 
    pergunta: QuizPerguntaUpdate, 
    service: QuizPerguntaService = Depends(get_pergunta_service)
):
    """
    Atualiza uma pergunta existente.
    """
    db_pergunta = service.update(pergunta_id, pergunta)
    if db_pergunta is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pergunta com ID {pergunta_id} não encontrada"
        )
    return db_pergunta


@router.delete("/perguntas/{pergunta_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_pergunta(
    pergunta_id: int, 
    service: QuizPerguntaService = Depends(get_pergunta_service)
):
    """
    Remove uma pergunta.
    """
    success = service.delete(pergunta_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pergunta com ID {pergunta_id} não encontrada"
        )
    return None


# Rotas para Opções
@router.get("/opcoes/", response_model=List[QuizOpcaoInDB])
def read_opcoes(
    skip: int = 0, 
    limit: int = 100, 
    service: QuizOpcaoService = Depends(get_opcao_service)
):
    """
    Retorna todas as opções.
    """
    opcoes = service.get_all(skip=skip, limit=limit)
    return opcoes


@router.get("/opcoes/pergunta/{pergunta_id}", response_model=List[QuizOpcaoInDB])
def read_opcoes_by_pergunta(
    pergunta_id: int, 
    service: QuizOpcaoService = Depends(get_opcao_service)
):
    """
    Retorna todas as opções de uma pergunta específica.
    """
    opcoes = service.get_by_pergunta(pergunta_id)
    return opcoes


@router.get("/opcoes/{opcao_id}", response_model=QuizOpcaoInDB)
def read_opcao(
    opcao_id: int, 
    service: QuizOpcaoService = Depends(get_opcao_service)
):
    """
    Retorna uma opção específica pelo ID.
    """
    opcao = service.get(opcao_id)
    if opcao is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Opção com ID {opcao_id} não encontrada"
        )
    return opcao


@router.post("/opcoes/", response_model=QuizOpcaoInDB, status_code=status.HTTP_201_CREATED)
def create_opcao(
    opcao: QuizOpcaoCreate, 
    service: QuizOpcaoService = Depends(get_opcao_service)
):
    """
    Cria uma nova opção.
    """
    return service.create(opcao)


@router.put("/opcoes/{opcao_id}", response_model=QuizOpcaoInDB)
def update_opcao(
    opcao_id: int, 
    opcao: QuizOpcaoUpdate, 
    service: QuizOpcaoService = Depends(get_opcao_service)
):
    """
    Atualiza uma opção existente.
    """
    db_opcao = service.update(opcao_id, opcao)
    if db_opcao is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Opção com ID {opcao_id} não encontrada"
        )
    return db_opcao


@router.delete("/opcoes/{opcao_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_opcao(
    opcao_id: int, 
    service: QuizOpcaoService = Depends(get_opcao_service)
):
    """
    Remove uma opção.
    """
    success = service.delete(opcao_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Opção com ID {opcao_id} não encontrada"
        )
    return None


# Rotas para Resultados
@router.get("/resultados/", response_model=List[QuizResultadoInDB])
def read_resultados(
    skip: int = 0, 
    limit: int = 100, 
    service: QuizResultadoService = Depends(get_resultado_service)
):
    """
    Retorna todos os resultados.
    """
    resultados = service.get_all(skip=skip, limit=limit)
    return resultados


@router.get("/resultados/{resultado_id}", response_model=QuizResultadoInDB)
def read_resultado(
    resultado_id: int, 
    service: QuizResultadoService = Depends(get_resultado_service)
):
    """
    Retorna um resultado específico pelo ID.
    """
    resultado = service.get(resultado_id)
    if resultado is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resultado com ID {resultado_id} não encontrado"
        )
    return resultado


@router.post("/resultados/", response_model=QuizResultadoInDB, status_code=status.HTTP_201_CREATED)
def create_resultado(
    resultado: QuizResultadoCreate, 
    service: QuizResultadoService = Depends(get_resultado_service)
):
    """
    Cria um novo resultado.
    """
    return service.create(resultado)


@router.put("/resultados/{resultado_id}", response_model=QuizResultadoInDB)
def update_resultado(
    resultado_id: int, 
    resultado: QuizResultadoUpdate, 
    service: QuizResultadoService = Depends(get_resultado_service)
):
    """
    Atualiza um resultado existente.
    """
    db_resultado = service.update(resultado_id, resultado)
    if db_resultado is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resultado com ID {resultado_id} não encontrado"
        )
    return db_resultado


@router.delete("/resultados/{resultado_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_resultado(
    resultado_id: int, 
    service: QuizResultadoService = Depends(get_resultado_service)
):
    """
    Remove um resultado.
    """
    success = service.delete(resultado_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resultado com ID {resultado_id} não encontrado"
        )
    return None


# Rotas para Regras
@router.get("/regras/", response_model=List[QuizRegraInDB])
def read_regras(
    skip: int = 0, 
    limit: int = 100, 
    service: QuizRegraService = Depends(get_regra_service)
):
    """
    Retorna todas as regras.
    """
    regras = service.get_all(skip=skip, limit=limit)
    return regras


@router.get("/regras/{regra_id}", response_model=QuizRegraInDB)
def read_regra(
    regra_id: int, 
    service: QuizRegraService = Depends(get_regra_service)
):
    """
    Retorna uma regra específica pelo ID.
    """
    regra = service.get(regra_id)
    if regra is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Regra com ID {regra_id} não encontrada"
        )
    return regra


@router.post("/regras/", response_model=QuizRegraInDB, status_code=status.HTTP_201_CREATED)
def create_regra(
    regra: QuizRegraCreate, 
    service: QuizRegraService = Depends(get_regra_service)
):
    """
    Cria uma nova regra.
    """
    return service.create(regra)


@router.put("/regras/{regra_id}", response_model=QuizRegraInDB)
def update_regra(
    regra_id: int, 
    regra: QuizRegraUpdate, 
    service: QuizRegraService = Depends(get_regra_service)
):
    """
    Atualiza uma regra existente.
    """
    db_regra = service.update(regra_id, regra)
    if db_regra is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Regra com ID {regra_id} não encontrada"
        )
    return db_regra


@router.delete("/regras/{regra_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_regra(
    regra_id: int, 
    service: QuizRegraService = Depends(get_regra_service)
):
    """
    Remove uma regra.
    """
    success = service.delete(regra_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Regra com ID {regra_id} não encontrada"
        )
    return None


# Rota para processar respostas do quiz
@router.post("/processar", response_model=dict)
def processar_quiz(
    respostas: Dict[str, str],
    regra_service: QuizRegraService = Depends(get_regra_service),
    resultado_service: QuizResultadoService = Depends(get_resultado_service)
):
    """
    Processa as respostas do quiz e retorna o resultado.
    """
    resultado_id = regra_service.processar_respostas(respostas)
    if resultado_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Não foi possível determinar um resultado para as respostas fornecidas"
        )
    
    resultado = resultado_service.get(resultado_id)
    if resultado is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resultado com ID {resultado_id} não encontrado"
        )
    
    return {
        "resultado_id": resultado.id,
        "nome": resultado.nome,
        "descricao": resultado.descricao,
        "recomendacao": resultado.recomendacao,
        "imagem_url": resultado.imagem_url,
        "produto_recomendado_id": resultado.produto_recomendado_id
    }
