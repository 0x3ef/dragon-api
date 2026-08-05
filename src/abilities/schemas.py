import uuid 
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel 


class AbilityModel(BaseModel):
    uid: uuid.UUID 
    name: str
    created_at: datetime 
    updated_at: datetime 
    dragons_uids: Optional[List[uuid.UUID]] = [] 


class AbilityCreateModel(BaseModel):
    name: str 


