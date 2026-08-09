import uuid 
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel 


class DistributionModel(BaseModel):
    uid: uuid.UUID
    name: str
    alternatenames: str
    created_at: datetime
    updated_at: datetime
    dragons_uids: Optional[List[uuid.UUID]] = Field(default_factory=list)


class DistributionCreateModel(BaseModel):
    name: str 
    alternatenames: str 
