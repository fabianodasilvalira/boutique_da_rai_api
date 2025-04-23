from sqlalchemy.orm import Session
from typing import List, Optional

from app.models.imagem import Imagem
from app.schemas.imagem_schema import ImagemCreate, ImagemUpdate


class ImagemRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get(self, imagem_id: int) -> Optional[Imagem]:
        return self.db.query(Imagem).filter(Imagem.id == imagem_id).first()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Imagem]:
        return self.db.query(Imagem).offset(skip).limit(limit).all()
    
    def get_by_entidade(self, tipo: str, entidade_id: int) -> List[Imagem]:
        return self.db.query(Imagem).filter(
            Imagem.entidade_tipo == tipo,
            Imagem.entidade_id == entidade_id
        ).all()
    
    def create(self, imagem: ImagemCreate) -> Imagem:
        db_imagem = Imagem(
            filename=imagem.filename,
            filepath=imagem.filepath,
            original_filename=imagem.original_filename,
            content_type=imagem.content_type,
            entidade_tipo=imagem.entidade_tipo,
            entidade_id=imagem.entidade_id
        )
        self.db.add(db_imagem)
        self.db.commit()
        self.db.refresh(db_imagem)
        return db_imagem
    
    def update(self, imagem_id: int, imagem: ImagemUpdate) -> Optional[Imagem]:
        db_imagem = self.get(imagem_id)
        if db_imagem is None:
            return None
        
        update_data = imagem.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_imagem, key, value)
        
        self.db.commit()
        self.db.refresh(db_imagem)
        return db_imagem
    
    def delete(self, imagem_id: int) -> bool:
        db_imagem = self.get(imagem_id)
        if db_imagem is None:
            return False
        
        self.db.delete(db_imagem)
        self.db.commit()
        return True
