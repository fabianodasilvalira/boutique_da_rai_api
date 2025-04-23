from typing import List, Optional

from app.repositories.imagem_repository import ImagemRepository
from app.schemas.imagem_schema import ImagemCreate, ImagemUpdate, ImagemInDB


class ImagemService:
    def __init__(self, repository: ImagemRepository):
        self.repository = repository
    
    def get(self, imagem_id: int) -> Optional[ImagemInDB]:
        imagem = self.repository.get(imagem_id)
        if imagem is None:
            return None
        return ImagemInDB.from_orm(imagem)
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[ImagemInDB]:
        imagens = self.repository.get_all(skip=skip, limit=limit)
        return [ImagemInDB.from_orm(imagem) for imagem in imagens]
    
    def get_by_entidade(self, tipo: str, entidade_id: int) -> List[ImagemInDB]:
        imagens = self.repository.get_by_entidade(tipo, entidade_id)
        return [ImagemInDB.from_orm(imagem) for imagem in imagens]
    
    def create(self, imagem: ImagemCreate) -> ImagemInDB:
        db_imagem = self.repository.create(imagem)
        return ImagemInDB.from_orm(db_imagem)
    
    def update(self, imagem_id: int, imagem: ImagemUpdate) -> Optional[ImagemInDB]:
        db_imagem = self.repository.update(imagem_id, imagem)
        if db_imagem is None:
            return None
        return ImagemInDB.from_orm(db_imagem)
    
    def delete(self, imagem_id: int) -> bool:
        return self.repository.delete(imagem_id)
    
    def associar_entidade(self, imagem_id: int, tipo: str, entidade_id: int) -> Optional[ImagemInDB]:
        update_data = ImagemUpdate(
            entidade_tipo=tipo,
            entidade_id=entidade_id
        )
        return self.update(imagem_id, update_data)
