import uuid 
from datetime import datetime 
from typing import List, Optional 
from pydantic import BaseModel, Field 
from src.abilities.schemas import AbilityModel 
from src.distributions.schemas import DistributionModel 
from src.images.schemas import ImageModel
from src.classes.schemas import DragonClassModel


class DragonModel(BaseModel):
    uid: uuid.UUID
    species: str
    firetype: str
    features: List[str] 
    colors: List[str] 
    diet: List[str] 
    habitat: List[str]
    size: str
    weight: int
    wingspan: int 
    trainable: bool
    attack: int 
    speed: int 
    armor: int 
    firepower: int 
    shotlimit: int 
    venom: int
    jawstrength: int
    created_at: datetime
    updated_at: datetime
    dragon_class: Optional[DragonClassModel] = None
    abilities: List[AbilityModel] = Field(default_factory=list)
    distributions: List[DistributionModel] = Field(default_factory=list)
    images: List[ImageModel] = Field(default_factory=list)


class DragonCreateModel(BaseModel):
    species: str
    firetype: str
    features: List[str] 
    colors: List[str] 
    diet: List[str] 
    habitat: List[str]
    size: str
    weight: int
    wingspan: int 
    trainable: bool
    attack: int 
    speed: int 
    armor: int 
    firepower: int 
    shotlimit: int 
    venom: int
    jawstrength: int
    class_uid: Optional[uuid.UUID] = None
    abilities: List[uuid.UUID] = Field(default_factory=list)
    distributions: List[uuid.UUID] = Field(default_factory=list)


class DragonUpdateModel(BaseModel):
    species: Optional[str] = None
    firetype: Optional[str] = None
    features_add: Optional[List[str]] = None
    features_remove: Optional[List[str]] = None
    colors_add: Optional[List[str]] = None
    colors_remove: Optional[List[str]] = None
    diet_add: Optional[List[str]] = None
    diet_remove: Optional[List[str]] = None 
    habitat_add: Optional[List[str]] = None
    habitat_remove: Optional[List[str]] = None
    size: Optional[str] = None
    weight: Optional[int] = None
    wingspan: Optional[int] = None
    trainable: Optional[bool] = None
    attack: Optional[int] = None
    speed: Optional[int] = None
    armor: Optional[int] = None
    firepower: Optional[int] = None
    shotlimit: Optional[int] = None
    venom: Optional[int] = None
    jawstrength: Optional[int] = None
    class_uid: Optional[uuid.UUID] = None
    ability_uids_add: List[uuid.UUID] = Field(default_factory=list)
    ability_uids_remove: List[uuid.UUID] = Field(default_factory=list)
    distribution_uids_add: List[uuid.UUID] = Field(default_factory=list)
    distribution_uids_remove: List[uuid.UUID] = Field(default_factory=list)


class DragonClassDragonsModel(DragonClassModel):
    dragons: List[DragonModel] = Field(default_factory=list)
