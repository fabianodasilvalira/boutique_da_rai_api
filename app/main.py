from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import engine, Base, get_db
from app.routers import categorias, produtos, quiz, contatos, usuarios, imagens
from app.models.models import Categoria, Produto, QuizPergunta, QuizOpcao, QuizResultado, QuizRegra, Contato, Usuario
from app.models.imagem import Imagem

# Criar tabelas no banco de dados
Base.metadata.create_all(bind=engine)

# Garantir que o diretório de uploads existe
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especificar origens permitidas
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Servir arquivos estáticos (uploads)
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

# Incluir routers
app.include_router(categorias.router, prefix=settings.API_V1_STR)
app.include_router(produtos.router, prefix=settings.API_V1_STR)
app.include_router(quiz.router, prefix=settings.API_V1_STR)
app.include_router(contatos.router, prefix=settings.API_V1_STR)
app.include_router(usuarios.router, prefix=settings.API_V1_STR)
app.include_router(imagens.router, prefix=settings.API_V1_STR)


@app.get("/")
def read_root():
    return {
        "message": "Bem-vindo à API de Perfumes",
        "version": "1.0.0",
        "docs": f"/docs"
    }


@app.get("/health")
def health_check():
    return {"status": "ok"}


# Endpoint para inicializar dados de exemplo (apenas para desenvolvimento)
@app.post("/init-db")
def init_db(db: Session = Depends(get_db)):
    # Verificar se já existem dados
    if db.query(Categoria).count() > 0:
        return {"message": "Banco de dados já inicializado"}
    
    # Criar categorias
    categorias_data = [
        {"nome": "Perfumes Masculinos", "descricao": "Fragrâncias marcantes e sofisticadas para homens modernos", "imagem_url": "/images/perfume_1.webp", "slug": "perfumes-masculinos"},
        {"nome": "Perfumes Femininos", "descricao": "Aromas delicados e envolventes para mulheres de atitude", "imagem_url": "/images/perfume_2.webp", "slug": "perfumes-femininos"},
        {"nome": "Perfumes Unissex", "descricao": "Fragrâncias versáteis para todos os estilos e personalidades", "imagem_url": "/images/perfume_3.webp", "slug": "perfumes-unissex"},
        {"nome": "Perfumes Infantis", "descricao": "Aromas suaves e divertidos para os pequenos", "imagem_url": "/images/perfume_1.webp", "slug": "perfumes-infantis"},
        {"nome": "Cosméticos", "descricao": "Produtos de beleza e cuidados pessoais de alta qualidade", "imagem_url": "/images/perfume_2.webp", "slug": "cosmeticos"},
        {"nome": "Bijuterias", "descricao": "Acessórios elegantes para complementar seu estilo", "imagem_url": "/images/perfume_3.webp", "slug": "bijuterias"}
    ]
    
    db_categorias = {}
    for cat_data in categorias_data:
        categoria = Categoria(**cat_data)
        db.add(categoria)
        db.commit()
        db.refresh(categoria)
        db_categorias[categoria.slug] = categoria
    
    # Criar produtos
    produtos_data = [
        {"nome": "Elegance Pour Homme", "descricao": "Fragrância amadeirada com notas de sândalo e bergamota", "preco": 189.90, "imagem_url": "/images/perfume_1.webp", "categoria_id": db_categorias["perfumes-masculinos"].id, "destaque": True, "estoque": 50},
        {"nome": "Blue Ocean", "descricao": "Aroma fresco e aquático para o dia a dia", "preco": 159.90, "imagem_url": "/images/perfume_2.webp", "categoria_id": db_categorias["perfumes-masculinos"].id, "destaque": False, "estoque": 30},
        {"nome": "Black Intense", "descricao": "Perfume intenso com notas de couro e especiarias", "preco": 219.90, "imagem_url": "/images/perfume_3.webp", "categoria_id": db_categorias["perfumes-masculinos"].id, "destaque": False, "estoque": 25},
        
        {"nome": "Floral Essence", "descricao": "Fragrância floral com notas de jasmim e rosa", "preco": 179.90, "imagem_url": "/images/perfume_2.webp", "categoria_id": db_categorias["perfumes-femininos"].id, "destaque": True, "estoque": 40},
        {"nome": "Sweet Vanilla", "descricao": "Aroma doce e envolvente com notas de baunilha", "preco": 169.90, "imagem_url": "/images/perfume_1.webp", "categoria_id": db_categorias["perfumes-femininos"].id, "destaque": False, "estoque": 35},
        {"nome": "Midnight Rose", "descricao": "Perfume sofisticado com notas de rosa e âmbar", "preco": 199.90, "imagem_url": "/images/perfume_3.webp", "categoria_id": db_categorias["perfumes-femininos"].id, "destaque": True, "estoque": 20},
        
        {"nome": "Fresh Citrus", "descricao": "Fragrância cítrica refrescante para qualquer ocasião", "preco": 149.90, "imagem_url": "/images/perfume_3.webp", "categoria_id": db_categorias["perfumes-unissex"].id, "destaque": True, "estoque": 45},
        {"nome": "Urban Style", "descricao": "Aroma moderno com notas de lavanda e cedro", "preco": 179.90, "imagem_url": "/images/perfume_1.webp", "categoria_id": db_categorias["perfumes-unissex"].id, "destaque": False, "estoque": 30},
        {"nome": "Pure White", "descricao": "Perfume clean com notas de algodão e almíscar", "preco": 159.90, "imagem_url": "/images/perfume_2.webp", "categoria_id": db_categorias["perfumes-unissex"].id, "destaque": False, "estoque": 25}
    ]
    
    for prod_data in produtos_data:
        produto = Produto(**prod_data)
        db.add(produto)
    
    # Criar perguntas do quiz
    perguntas_data = [
        {"pergunta": "Qual é o seu dia a dia?", "ordem": 1},
        {"pergunta": "Qual intensidade de fragrância você prefere?", "ordem": 2},
        {"pergunta": "Para qual ocasião você está buscando um perfume?", "ordem": 3},
        {"pergunta": "Qual tipo de fragrância mais lhe agrada?", "ordem": 4},
        {"pergunta": "Quais sensações e sentimentos você quer despertar?", "ordem": 5}
    ]
    
    db_perguntas = {}
    for i, perg_data in enumerate(perguntas_data):
        pergunta = QuizPergunta(**perg_data)
        db.add(pergunta)
        db.commit()
        db.refresh(pergunta)
        db_perguntas[i+1] = pergunta
    
    # Criar opções do quiz
    opcoes_data = [
        # Pergunta 1
        {"pergunta_id": db_perguntas[1].id, "texto": "Trabalho em escritório", "valor_id": "trabalho"},
        {"pergunta_id": db_perguntas[1].id, "texto": "Fico mais em casa", "valor_id": "casa"},
        {"pergunta_id": db_perguntas[1].id, "texto": "Atividades ao ar livre", "valor_id": "ar_livre"},
        {"pergunta_id": db_perguntas[1].id, "texto": "Bastante variado", "valor_id": "variado"},
        
        # Pergunta 2
        {"pergunta_id": db_perguntas[2].id, "texto": "Suave", "valor_id": "suave"},
        {"pergunta_id": db_perguntas[2].id, "texto": "Moderada", "valor_id": "moderada"},
        {"pergunta_id": db_perguntas[2].id, "texto": "Intensa", "valor_id": "intensa"},
        
        # Pergunta 3
        {"pergunta_id": db_perguntas[3].id, "texto": "Dia a dia", "valor_id": "dia_a_dia"},
        {"pergunta_id": db_perguntas[3].id, "texto": "Trabalho", "valor_id": "trabalho"},
        {"pergunta_id": db_perguntas[3].id, "texto": "Encontro romântico", "valor_id": "encontro"},
        {"pergunta_id": db_perguntas[3].id, "texto": "Ocasião especial", "valor_id": "ocasiao_especial"},
        
        # Pergunta 4
        {"pergunta_id": db_perguntas[4].id, "texto": "Floral", "valor_id": "floral", "imagem_url": "/images/floral.webp"},
        {"pergunta_id": db_perguntas[4].id, "texto": "Frutal", "valor_id": "frutal", "imagem_url": "/images/frutal.webp"},
        {"pergunta_id": db_perguntas[4].id, "texto": "Oriental", "valor_id": "oriental", "imagem_url": "/images/oriental.jpeg"},
        {"pergunta_id": db_perguntas[4].id, "texto": "Amadeirado", "valor_id": "amadeirado", "imagem_url": "/images/amadeirado.jpeg"},
        
        # Pergunta 5
        {"pergunta_id": db_perguntas[5].id, "texto": "Frescor e liberdade", "valor_id": "frescor"},
        {"pergunta_id": db_perguntas[5].id, "texto": "Sensualidade e mistério", "valor_id": "sensualidade"},
        {"pergunta_id": db_perguntas[5].id, "texto": "Elegância e sofisticação", "valor_id": "elegancia"},
        {"pergunta_id": db_perguntas[5].id, "texto": "Conforto e aconchego", "valor_id": "conforto"}
    ]
    
    for opcao_data in opcoes_data:
        opcao = QuizOpcao(**opcao_data)
        db.add(opcao)
    
    # Criar resultados do quiz
    resultados_data = [
        {"nome": "Floral Delicado", "descricao": "Um perfume floral suave com notas de jasmim e rosa, ideal para o dia a dia e ambientes de trabalho.", "recomendacao": "Ideal para mulheres que preferem fragrâncias sutis e elegantes para o cotidiano.", "imagem_url": "/images/perfume_1.webp"},
        {"nome": "Floral Intenso", "descricao": "Uma fragrância floral marcante com notas de gardênia e ylang-ylang. Perfeita para ocasiões especiais e encontros românticos.", "recomendacao": "Perfeito para mulheres que desejam marcar presença com uma fragrância memorável.", "imagem_url": "/images/perfume_2.webp"},
        {"nome": "Frutal Refrescante", "descricao": "Um perfume frutal leve com notas cítricas de laranja e maçã verde. Ideal para o dia a dia e atividades ao ar livre.", "recomendacao": "Excelente para mulheres dinâmicas que buscam frescor durante todo o dia.", "imagem_url": "/images/perfume_3.webp"},
        {"nome": "Oriental Misterioso", "descricao": "Uma fragrância oriental intensa com notas de baunilha e âmbar. Perfeita para noites especiais e encontros românticos.", "recomendacao": "Ideal para mulheres que desejam transmitir sensualidade e mistério.", "imagem_url": "/images/woman_perfume_1.webp"},
        {"nome": "Amadeirado Sofisticado", "descricao": "Um perfume amadeirado com notas de sândalo e cedro. Equilibrado e versátil, adequado para diversas ocasiões.", "recomendacao": "Perfeito para mulheres que apreciam fragrâncias sofisticadas e atemporais.", "imagem_url": "/images/woman_perfume_2.webp"}
    ]
    
    db_resultados = {}
    for i, res_data in enumerate(resultados_data):
        resultado = QuizResultado(**res_data)
        db.add(resultado)
        db.commit()
        db.refresh(resultado)
        db_resultados[i+1] = resultado
    
    # Criar regras do quiz
    regras_data = [
        {"combinacao_respostas": {"4": "floral", "2": "suave"}, "resultado_id": db_resultados[1].id},
        {"combinacao_respostas": {"4": "floral", "2": "intensa"}, "resultado_id": db_resultados[2].id},
        {"combinacao_respostas": {"4": "frutal"}, "resultado_id": db_resultados[3].id},
        {"combinacao_respostas": {"4": "oriental"}, "resultado_id": db_resultados[4].id},
        {"combinacao_respostas": {"4": "amadeirado"}, "resultado_id": db_resultados[5].id}
    ]
    
    for regra_data in regras_data:
        regra = QuizRegra(**regra_data)
        db.add(regra)
    
    # Criar usuário admin
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    admin_data = {
        "nome": "Administrador",
        "email": "admin@perfumes.com.br",
        "senha_hash": pwd_context.hash("admin123"),
        "ativo": True
    }
    
    admin = Usuario(**admin_data)
    db.add(admin)
    
    db.commit()
    
    return {"message": "Banco de dados inicializado com sucesso"}
