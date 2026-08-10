import uuid
from typing import List
from fastapi import APIRouter, Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from src.errors import AbilityNotFound
from .schemas import AbilityModel, AbilityCreateModel
from .service import AbilitiesService

abilities_router = APIRouter()
abilities_service = AbilitiesService()


@abilities_router.get("/", response_model=List[AbilityModel], status_code=status.HTTP_200_OK)
async def get_all_abilities(
    session: AsyncSession = Depends(get_session),
) -> List[AbilityModel]:
    return await abilities_service.get_all_abilities(session)


@abilities_router.get("/{ability_uid}", response_model=AbilityModel, status_code=status.HTTP_200_OK)
async def get_ability_by_uid(
    ability_uid: uuid.UUID | str,
    session: AsyncSession = Depends(get_session)
) -> AbilityModel:
    ability = await abilities_service.get_ability_by_uid(ability_uid, session)
    if ability is not None:
        return ability
    else:
        raise AbilityNotFound()


@abilities_router.post("/", response_model=AbilityModel, status_code=status.HTTP_201_CREATED)
async def create_ability(
    ability_data: AbilityCreateModel,
    session: AsyncSession = Depends(get_session)
) -> AbilityModel:
    return await abilities_service.create_ability(ability_data, session)


@abilities_router.delete("/{ability_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_ability(
    ability_uid: uuid.UUID | str,
    session: AsyncSession = Depends(get_session)
) -> None:
    ability_to_delete = await abilities_service.delete_ability(ability_uid, session)

    if not ability_to_delete:
        raise AbilityNotFound()
    else:
        return None
