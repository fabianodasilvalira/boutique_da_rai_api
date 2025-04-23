from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session

from app.models.models import Categoria, Produto, QuizPergunta, QuizOpcao, QuizResultado, QuizRegra, Contato, Usuario


class BaseRepository:
    def __init__(self, db: Session):
        self.db = db


class CategoriaRepository(BaseRepository):
    def get(self, id: int) -> Optional[Categoria]:
        return self.db.query(Categoria).filter(Categoria.id == id).first()
    
    def get_by_slug(self, slug: str) -> Optional[Categoria]:
        return self.db.query(Categoria).filter(Categoria.slug == slug).first()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Categoria]:
        return self.db.query(Categoria).offset(skip).limit(limit).all()
    
    def create(self, categoria_data: Dict[str, Any]) -> Categoria:
        categoria = Categoria(**categoria_data)
        self.db.add(categoria)
        self.db.commit()
        self.db.refresh(categoria)
        return categoria
    
    def update(self, id: int, categoria_data: Dict[str, Any]) -> Optional[Categoria]:
        categoria = self.get(id)
        if not categoria:
            return None
        
        for key, value in categoria_data.items():
            setattr(categoria, key, value)
        
        self.db.commit()
        self.db.refresh(categoria)
        return categoria
    
    def delete(self, id: int) -> bool:
        categoria = self.get(id)
        if not categoria:
            return False
        
        self.db.delete(categoria)
        self.db.commit()
        return True


class ProdutoRepository(BaseRepository):
    def get(self, id: int) -> Optional[Produto]:
        return self.db.query(Produto).filter(Produto.id == id).first()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Produto]:
        return self.db.query(Produto).offset(skip).limit(limit).all()
    
    def get_by_categoria(self, categoria_id: int, skip: int = 0, limit: int = 100) -> List[Produto]:
        return self.db.query(Produto).filter(Produto.categoria_id == categoria_id).offset(skip).limit(limit).all()
    
    def get_destaques(self, skip: int = 0, limit: int = 100) -> List[Produto]:
        return self.db.query(Produto).filter(Produto.destaque == True).offset(skip).limit(limit).all()
    
    def create(self, produto_data: Dict[str, Any]) -> Produto:
        produto = Produto(**produto_data)
        self.db.add(produto)
        self.db.commit()
        self.db.refresh(produto)
        return produto
    
    def update(self, id: int, produto_data: Dict[str, Any]) -> Optional[Produto]:
        produto = self.get(id)
        if not produto:
            return None
        
        for key, value in produto_data.items():
            setattr(produto, key, value)
        
        self.db.commit()
        self.db.refresh(produto)
        return produto
    
    def delete(self, id: int) -> bool:
        produto = self.get(id)
        if not produto:
            return False
        
        self.db.delete(produto)
        self.db.commit()
        return True


class QuizPerguntaRepository(BaseRepository):
    def get(self, id: int) -> Optional[QuizPergunta]:
        return self.db.query(QuizPergunta).filter(QuizPergunta.id == id).first()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[QuizPergunta]:
        return self.db.query(QuizPergunta).order_by(QuizPergunta.ordem).offset(skip).limit(limit).all()
    
    def create(self, pergunta_data: Dict[str, Any]) -> QuizPergunta:
        pergunta = QuizPergunta(**pergunta_data)
        self.db.add(pergunta)
        self.db.commit()
        self.db.refresh(pergunta)
        return pergunta
    
    def update(self, id: int, pergunta_data: Dict[str, Any]) -> Optional[QuizPergunta]:
        pergunta = self.get(id)
        if not pergunta:
            return None
        
        for key, value in pergunta_data.items():
            setattr(pergunta, key, value)
        
        self.db.commit()
        self.db.refresh(pergunta)
        return pergunta
    
    def delete(self, id: int) -> bool:
        pergunta = self.get(id)
        if not pergunta:
            return False
        
        self.db.delete(pergunta)
        self.db.commit()
        return True


class QuizOpcaoRepository(BaseRepository):
    def get(self, id: int) -> Optional[QuizOpcao]:
        return self.db.query(QuizOpcao).filter(QuizOpcao.id == id).first()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[QuizOpcao]:
        return self.db.query(QuizOpcao).offset(skip).limit(limit).all()
    
    def get_by_pergunta(self, pergunta_id: int) -> List[QuizOpcao]:
        return self.db.query(QuizOpcao).filter(QuizOpcao.pergunta_id == pergunta_id).all()
    
    def create(self, opcao_data: Dict[str, Any]) -> QuizOpcao:
        opcao = QuizOpcao(**opcao_data)
        self.db.add(opcao)
        self.db.commit()
        self.db.refresh(opcao)
        return opcao
    
    def update(self, id: int, opcao_data: Dict[str, Any]) -> Optional[QuizOpcao]:
        opcao = self.get(id)
        if not opcao:
            return None
        
        for key, value in opcao_data.items():
            setattr(opcao, key, value)
        
        self.db.commit()
        self.db.refresh(opcao)
        return opcao
    
    def delete(self, id: int) -> bool:
        opcao = self.get(id)
        if not opcao:
            return False
        
        self.db.delete(opcao)
        self.db.commit()
        return True


class QuizResultadoRepository(BaseRepository):
    def get(self, id: int) -> Optional[QuizResultado]:
        return self.db.query(QuizResultado).filter(QuizResultado.id == id).first()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[QuizResultado]:
        return self.db.query(QuizResultado).offset(skip).limit(limit).all()
    
    def create(self, resultado_data: Dict[str, Any]) -> QuizResultado:
        resultado = QuizResultado(**resultado_data)
        self.db.add(resultado)
        self.db.commit()
        self.db.refresh(resultado)
        return resultado
    
    def update(self, id: int, resultado_data: Dict[str, Any]) -> Optional[QuizResultado]:
        resultado = self.get(id)
        if not resultado:
            return None
        
        for key, value in resultado_data.items():
            setattr(resultado, key, value)
        
        self.db.commit()
        self.db.refresh(resultado)
        return resultado
    
    def delete(self, id: int) -> bool:
        resultado = self.get(id)
        if not resultado:
            return False
        
        self.db.delete(resultado)
        self.db.commit()
        return True


class QuizRegraRepository(BaseRepository):
    def get(self, id: int) -> Optional[QuizRegra]:
        return self.db.query(QuizRegra).filter(QuizRegra.id == id).first()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[QuizRegra]:
        return self.db.query(QuizRegra).offset(skip).limit(limit).all()
    
    def get_by_resultado(self, resultado_id: int) -> List[QuizRegra]:
        return self.db.query(QuizRegra).filter(QuizRegra.resultado_id == resultado_id).all()
    
    def create(self, regra_data: Dict[str, Any]) -> QuizRegra:
        regra = QuizRegra(**regra_data)
        self.db.add(regra)
        self.db.commit()
        self.db.refresh(regra)
        return regra
    
    def update(self, id: int, regra_data: Dict[str, Any]) -> Optional[QuizRegra]:
        regra = self.get(id)
        if not regra:
            return None
        
        for key, value in regra_data.items():
            setattr(regra, key, value)
        
        self.db.commit()
        self.db.refresh(regra)
        return regra
    
    def delete(self, id: int) -> bool:
        regra = self.get(id)
        if not regra:
            return False
        
        self.db.delete(regra)
        self.db.commit()
        return True


class ContatoRepository(BaseRepository):
    def get(self, id: int) -> Optional[Contato]:
        return self.db.query(Contato).filter(Contato.id == id).first()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Contato]:
        return self.db.query(Contato).offset(skip).limit(limit).all()
    
    def get_nao_respondidos(self, skip: int = 0, limit: int = 100) -> List[Contato]:
        return self.db.query(Contato).filter(Contato.respondido == False).offset(skip).limit(limit).all()
    
    def create(self, contato_data: Dict[str, Any]) -> Contato:
        contato = Contato(**contato_data)
        self.db.add(contato)
        self.db.commit()
        self.db.refresh(contato)
        return contato
    
    def update(self, id: int, contato_data: Dict[str, Any]) -> Optional[Contato]:
        contato = self.get(id)
        if not contato:
            return None
        
        for key, value in contato_data.items():
            setattr(contato, key, value)
        
        self.db.commit()
        self.db.refresh(contato)
        return contato
    
    def delete(self, id: int) -> bool:
        contato = self.get(id)
        if not contato:
            return False
        
        self.db.delete(contato)
        self.db.commit()
        return True


class UsuarioRepository(BaseRepository):
    def get(self, id: int) -> Optional[Usuario]:
        return self.db.query(Usuario).filter(Usuario.id == id).first()
    
    def get_by_email(self, email: str) -> Optional[Usuario]:
        return self.db.query(Usuario).filter(Usuario.email == email).first()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Usuario]:
        return self.db.query(Usuario).offset(skip).limit(limit).all()
    
    def create(self, usuario_data: Dict[str, Any]) -> Usuario:
        usuario = Usuario(**usuario_data)
        self.db.add(usuario)
        self.db.commit()
        self.db.refresh(usuario)
        return usuario
    
    def update(self, id: int, usuario_data: Dict[str, Any]) -> Optional[Usuario]:
        usuario = self.get(id)
        if not usuario:
            return None
        
        for key, value in usuario_data.items():
            setattr(usuario, key, value)
        
        self.db.commit()
        self.db.refresh(usuario)
        return usuario
    
    def delete(self, id: int) -> bool:
        usuario = self.get(id)
        if not usuario:
            return False
        
        self.db.delete(usuario)
        self.db.commit()
        return True
