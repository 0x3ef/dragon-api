import uuid 
from datetime import datetime 
from typing import Optional 
from pydantic import BaseModel 


class ImageModel(BaseModel):
    uid: uuid.UUID
    dragon_uid: Optional[uuid.UUID]
    url: str
    created_at: datetime
    updated_at: datetime 


class ImageCreateModel(BaseModel):
    dragon_uid: Optional[uuid.UUID] 
    url: str
