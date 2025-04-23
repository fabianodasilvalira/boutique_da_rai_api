from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class ImagemBase(BaseModel):
    filename: str
    filepath: str
    original_filename: str
    content_type: str
    entidade_tipo: str
    entidade_id: Optional[int] = None


class ImagemCreate(ImagemBase):
    pass


class ImagemUpdate(BaseModel):
    entidade_tipo: Optional[str] = None
    entidade_id: Optional[int] = None


class ImagemInDB(ImagemBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
