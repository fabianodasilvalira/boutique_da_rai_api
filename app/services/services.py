from typing import List, Optional, Dict, Any
from datetime import datetime
from passlib.context import CryptContext

from app.repositories.repositories import (
    CategoriaRepository, ProdutoRepository, QuizPerguntaRepository,
    QuizOpcaoRepository, QuizResultadoRepository, QuizRegraRepository,
    ContatoRepository, UsuarioRepository
)
from app.schemas.schemas import (
    CategoriaCreate, CategoriaUpdate, ProdutoCreate, ProdutoUpdate,
    QuizPerguntaCreate, QuizPerguntaUpdate, QuizOpcaoCreate, QuizOpcaoUpdate,
    QuizResultadoCreate, QuizResultadoUpdate, QuizRegraCreate, QuizRegraUpdate,
    ContatoCreate, ContatoUpdate, UsuarioCreate, UsuarioUpdate
)

# Configuração para hash de senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class BaseService:
    pass


class CategoriaService(BaseService):
    def __init__(self, repository: CategoriaRepository):
        self.repository = repository
    
    def get(self, id: int):
        return self.repository.get(id)
    
    def get_by_slug(self, slug: str):
        return self.repository.get_by_slug(slug)
    
    def get_all(self, skip: int = 0, limit: int = 100):
        return self.repository.get_all(skip, limit)
    
    def create(self, categoria: CategoriaCreate):
        categoria_data = categoria.model_dump()
        return self.repository.create(categoria_data)
    
    def update(self, id: int, categoria: CategoriaUpdate):
        categoria_data = {k: v for k, v in categoria.model_dump().items() if v is not None}
        return self.repository.update(id, categoria_data)
    
    def delete(self, id: int):
        return self.repository.delete(id)


class ProdutoService(BaseService):
    def __init__(self, repository: ProdutoRepository):
        self.repository = repository
    
    def get(self, id: int):
        return self.repository.get(id)
    
    def get_all(self, skip: int = 0, limit: int = 100):
        return self.repository.get_all(skip, limit)
    
    def get_by_categoria(self, categoria_id: int, skip: int = 0, limit: int = 100):
        return self.repository.get_by_categoria(categoria_id, skip, limit)
    
    def get_destaques(self, skip: int = 0, limit: int = 100):
        return self.repository.get_destaques(skip, limit)
    
    def create(self, produto: ProdutoCreate):
        produto_data = produto.model_dump()
        return self.repository.create(produto_data)
    
    def update(self, id: int, produto: ProdutoUpdate):
        produto_data = {k: v for k, v in produto.model_dump().items() if v is not None}
        return self.repository.update(id, produto_data)
    
    def delete(self, id: int):
        return self.repository.delete(id)


class QuizPerguntaService(BaseService):
    def __init__(self, repository: QuizPerguntaRepository):
        self.repository = repository
    
    def get(self, id: int):
        return self.repository.get(id)
    
    def get_all(self, skip: int = 0, limit: int = 100):
        return self.repository.get_all(skip, limit)
    
    def create(self, pergunta: QuizPerguntaCreate):
        pergunta_data = pergunta.model_dump()
        return self.repository.create(pergunta_data)
    
    def update(self, id: int, pergunta: QuizPerguntaUpdate):
        pergunta_data = {k: v for k, v in pergunta.model_dump().items() if v is not None}
        return self.repository.update(id, pergunta_data)
    
    def delete(self, id: int):
        return self.repository.delete(id)


class QuizOpcaoService(BaseService):
    def __init__(self, repository: QuizOpcaoRepository):
        self.repository = repository
    
    def get(self, id: int):
        return self.repository.get(id)
    
    def get_all(self, skip: int = 0, limit: int = 100):
        return self.repository.get_all(skip, limit)
    
    def get_by_pergunta(self, pergunta_id: int):
        return self.repository.get_by_pergunta(pergunta_id)
    
    def create(self, opcao: QuizOpcaoCreate):
        opcao_data = opcao.model_dump()
        return self.repository.create(opcao_data)
    
    def update(self, id: int, opcao: QuizOpcaoUpdate):
        opcao_data = {k: v for k, v in opcao.model_dump().items() if v is not None}
        return self.repository.update(id, opcao_data)
    
    def delete(self, id: int):
        return self.repository.delete(id)


class QuizResultadoService(BaseService):
    def __init__(self, repository: QuizResultadoRepository):
        self.repository = repository
    
    def get(self, id: int):
        return self.repository.get(id)
    
    def get_all(self, skip: int = 0, limit: int = 100):
        return self.repository.get_all(skip, limit)
    
    def create(self, resultado: QuizResultadoCreate):
        resultado_data = resultado.model_dump()
        return self.repository.create(resultado_data)
    
    def update(self, id: int, resultado: QuizResultadoUpdate):
        resultado_data = {k: v for k, v in resultado.model_dump().items() if v is not None}
        return self.repository.update(id, resultado_data)
    
    def delete(self, id: int):
        return self.repository.delete(id)


class QuizRegraService(BaseService):
    def __init__(self, repository: QuizRegraRepository):
        self.repository = repository
    
    def get(self, id: int):
        return self.repository.get(id)
    
    def get_all(self, skip: int = 0, limit: int = 100):
        return self.repository.get_all(skip, limit)
    
    def get_by_resultado(self, resultado_id: int):
        return self.repository.get_by_resultado(resultado_id)
    
    def create(self, regra: QuizRegraCreate):
        regra_data = regra.model_dump()
        return self.repository.create(regra_data)
    
    def update(self, id: int, regra: QuizRegraUpdate):
        regra_data = {k: v for k, v in regra.model_dump().items() if v is not None}
        return self.repository.update(id, regra_data)
    
    def delete(self, id: int):
        return self.repository.delete(id)
    
    def processar_respostas(self, respostas: Dict[str, str]):
        """
        Processa as respostas do quiz e retorna o resultado mais adequado
        """
        # Buscar todas as regras
        regras = self.repository.get_all()
        
        # Implementação simplificada - em um caso real seria mais complexo
        # Aqui estamos apenas verificando se as respostas correspondem exatamente a uma regra
        for regra in regras:
            combinacao = regra.combinacao_respostas
            match = True
            
            for pergunta_id, resposta in combinacao.items():
                if pergunta_id not in respostas or respostas[pergunta_id] != resposta:
                    match = False
                    break
            
            if match:
                return regra.resultado_id
        
        # Se não encontrar correspondência exata, retorna o primeiro resultado (fallback)
        if regras:
            return regras[0].resultado_id
        
        return None


class ContatoService(BaseService):
    def __init__(self, repository: ContatoRepository):
        self.repository = repository
    
    def get(self, id: int):
        return self.repository.get(id)
    
    def get_all(self, skip: int = 0, limit: int = 100):
        return self.repository.get_all(skip, limit)
    
    def get_nao_respondidos(self, skip: int = 0, limit: int = 100):
        return self.repository.get_nao_respondidos(skip, limit)
    
    def create(self, contato: ContatoCreate):
        contato_data = contato.model_dump()
        return self.repository.create(contato_data)
    
    def update(self, id: int, contato: ContatoUpdate):
        contato_data = {k: v for k, v in contato.model_dump().items() if v is not None}
        return self.repository.update(id, contato_data)
    
    def marcar_como_respondido(self, id: int):
        return self.repository.update(id, {"respondido": True})
    
    def delete(self, id: int):
        return self.repository.delete(id)


class UsuarioService(BaseService):
    def __init__(self, repository: UsuarioRepository):
        self.repository = repository
    
    def get(self, id: int):
        return self.repository.get(id)
    
    def get_by_email(self, email: str):
        return self.repository.get_by_email(email)
    
    def get_all(self, skip: int = 0, limit: int = 100):
        return self.repository.get_all(skip, limit)
    
    def create(self, usuario: UsuarioCreate):
        usuario_data = usuario.model_dump()
        # Hash da senha antes de salvar
        senha_hash = self._get_password_hash(usuario_data.pop("senha"))
        usuario_data["senha_hash"] = senha_hash
        
        return self.repository.create(usuario_data)
    
    def update(self, id: int, usuario: UsuarioUpdate):
        usuario_data = {k: v for k, v in usuario.model_dump().items() if v is not None}
        
        # Se a senha foi fornecida, hash antes de salvar
        if "senha" in usuario_data:
            senha_hash = self._get_password_hash(usuario_data.pop("senha"))
            usuario_data["senha_hash"] = senha_hash
        
        return self.repository.update(id, usuario_data)
    
    def delete(self, id: int):
        return self.repository.delete(id)
    
    def authenticate(self, email: str, senha: str):
        usuario = self.repository.get_by_email(email)
        if not usuario:
            return False
        
        if not self._verify_password(senha, usuario.senha_hash):
            return False
        
        # Atualizar último acesso
        self.repository.update(usuario.id, {"ultimo_acesso": datetime.utcnow()})
        
        return usuario
    
    def _get_password_hash(self, password: str):
        return pwd_context.hash(password)
    
    def _verify_password(self, plain_password: str, hashed_password: str):
        return pwd_context.verify(plain_password, hashed_password)
