import uuid 
from datetime import datetime 
from typing import List, Optional
from pydantic import BaseModel
from src.dragons.schemas import DragonModel


class DragonClassModel(BaseModel):
    uid: uuid.UUID
    name: str
    description: str 
    icon: str
    created_at: datetime 
    updated_at: datetime 


class DragonClassCreateModel(BaseModel):
    name: str
    description: str 
    icon: str


class DragonClassUpdateModel(BaseModel):
    name: Optional[str] = None 
    description: Optional[str] = None
    icon: Optional[str] = None
