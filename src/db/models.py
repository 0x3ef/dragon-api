import uuid
from datetime import datetime
from typing import List, Optional
import sqlalchemy.dialects.postgresql as pg
from sqlmodel import Column, Field, Relationship, SQLModel


class DragonAbility(SQLModel, table=True):
    __tablename__ = "dragon_abilities"

    dragon_uid: Optional[uuid.UUID] = Field(
        default=None,
        foreign_key="dragons.uid",
        primary_key=True,
    )
    ability_uid: Optional[uuid.UUID] = Field(
        default=None,
        foreign_key="abilities.uid",
        primary_key=True,
    )


class DistributionDragon(SQLModel, table=True):
    __tablename__ = "distribution_dragons"

    dragon_uid: Optional[uuid.UUID] = Field(
        default=None,
        foreign_key="dragons.uid",
        primary_key=True,
    )
    distribution_uid: Optional[uuid.UUID] = Field(
        default=None,
        foreign_key="distributions.uid",
        primary_key=True,
    )


class Ability(SQLModel, table=True):
    __tablename__ = "abilities"

    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid7)
    )
    name: str

    dragons: List["Dragon"] = Relationship(
        back_populates="abilities",
        link_model=DragonAbility,
        sa_relationship_kwargs={"lazy": "selectin"},
    )


class Distribution(SQLModel, table=True):
    __tablename__ = "distributions"

    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid7)
    )
    name: str
    alternatenames: str
    created_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP, default=datetime.now)
    )
    updated_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP, default=datetime.now)
    )

    dragons: List["Dragon"] = Relationship(
        back_populates="distributions",
        link_model=DistributionDragon,
        sa_relationship_kwargs={"lazy": "selectin"},
    )


class Image(SQLModel, table=True):
    __tablename__ = "images"

    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid7)
    )
    dragon_uid: Optional[uuid.UUID] = Field(
        default=None,
        foreign_key="dragons.uid",
    )
    url: str
    created_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP, default=datetime.now)
    )
    updated_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP, default=datetime.now)
    )

    dragon: Optional["Dragon"] = Relationship(back_populates="images")


class DragonClass(SQLModel, table=True):
    __tablename__ = "classes"

    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid7)
    )
    name: str 
    description: str 
    icon: str

    created_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP, default=datetime.now)
    )
    
    updated_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP, default=datetime.now)
    )

    dragons: List["Dragon"] = Relationship(
        back_populates="dragon_class",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
    

class Dragon(SQLModel, table=True):
    __tablename__ = "dragons"

    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid7)
    )
    species: str
    firetype: str 

    features: List[str] = Field(default=[], sa_type=pg.ARRAY(pg.TEXT))
    colors: List[str] = Field(default=[], sa_type=pg.ARRAY(pg.TEXT))
    diet: List[str] = Field(default=[], sa_type=pg.ARRAY(pg.TEXT))
    habitat: List[str] = Field(default=[], sa_type=pg.ARRAY(pg.TEXT))
    
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

    class_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="classes.uid")
    
    created_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP, default=datetime.now)
    )
    updated_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP, default=datetime.now)
    )
    
    dragon_class: Optional[DragonClass] = Relationship(back_populates="dragons")

    abilities: List[Ability] = Relationship(
        back_populates="dragons",
        link_model=DragonAbility,
        sa_relationship_kwargs={"lazy": "selectin"},
    )

    distributions: List[Distribution] = Relationship(
        back_populates="dragons",
        link_model=DistributionDragon,
        sa_relationship_kwargs={"lazy": "selectin"},
    )

    images: List[Image] = Relationship(
        back_populates="dragon",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
