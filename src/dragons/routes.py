import uuid
from typing import List
from fastapi import APIRouter, Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from .schemas import DragonModel, DragonCreateModel, DragonUpdateModel
from src.abilities.schemas import AbilityModel
from src.distributions.schemas import DistributionModel
from src.images.schemas import ImageModel
from .service import DragonService
from src.errors import DragonNotFound

dragons_router = APIRouter()
dragons_service = DragonService()


@dragons_router.get("/", response_model=List[DragonModel], status_code=status.HTTP_200_OK)
async def get_all_dragons(
    session: AsyncSession = Depends(get_session)
) -> List[DragonModel]:
    return await dragons_service.get_all_dragons(session)


@dragons_router.get("/{dragon_uid}", response_model=DragonModel, status_code=status.HTTP_200_OK)
async def get_dragon(
    dragon_uid: uuid.UUID | str,
    session: AsyncSession = Depends(get_session)
) -> DragonModel:
    dragon = await dragons_service.get_dragon(dragon_uid, session)
    if not dragon:
        raise DragonNotFound()
    return dragon


@dragons_router.get("/{dragon_uid}/abilities", response_model=List[AbilityModel], status_code=status.HTTP_200_OK)
async def get_dragon_abilities(
    dragon_uid: uuid.UUID | str,
    session: AsyncSession = Depends(get_session)
) -> List[AbilityModel]:
    dragon = await dragons_service.get_dragon(dragon_uid, session)
    if not dragon:
        raise DragonNotFound()
    return await dragons_service.get_dragon_abilities(dragon, session)


@dragons_router.get("/{dragon_uid}/images", response_model=List[ImageModel], status_code=status.HTTP_200_OK)
async def get_images_by_dragon(
    dragon_uid: uuid.UUID | str,
    session: AsyncSession = Depends(get_session)
) -> List[ImageModel]:
    dragon = await dragons_service.get_dragon(dragon_uid, session)
    if not dragon:
        raise DragonNotFound()
    return await dragons_service.get_dragon_images(dragon, session)


@dragons_router.get("/{dragon_uid}/distributions", response_model=List[DistributionModel], status_code=status.HTTP_200_OK)
async def get_distributions_by_dragon(
    dragon_uid: uuid.UUID | str,
    session: AsyncSession = Depends(get_session)
) -> List[DistributionModel]:
    dragon = await dragons_service.get_dragon(dragon_uid, session)
    if not dragon:
        raise DragonNotFound()
    return await dragons_service.get_dragon_distributions(dragon, session)


@dragons_router.post("/", response_model=DragonModel, status_code=status.HTTP_201_CREATED)
async def create_dragon(
    dragon_data: DragonCreateModel,
    session: AsyncSession = Depends(get_session)
) -> DragonModel:
    return await dragons_service.create_dragon(dragon_data, session)


@dragons_router.post("/{dragon_uid}/abilities/{ability_uid}", status_code=status.HTTP_200_OK, response_model=DragonModel)
async def add_ability_to_dragon(
    dragon_uid: uuid.UUID | str,
    ability_uid: uuid.UUID | str,
    session: AsyncSession = Depends(get_session),
) -> DragonModel:
    dragon = await dragons_service.get_dragon(dragon_uid, session)
    if not dragon:
        raise DragonNotFound()
    return await dragons_service.add_ability_to_dragon(dragon, ability_uid, session)


@dragons_router.post("/{dragon_uid}/distributions/{distribution_uid}", status_code=status.HTTP_200_OK, response_model=DragonModel)
async def add_distribution_to_dragon(
    dragon_uid: uuid.UUID | str,
    distribution_uid: uuid.UUID | str,
    session: AsyncSession = Depends(get_session)
) -> DragonModel:
    dragon = await dragons_service.get_dragon(dragon_uid, session)
    if not dragon:
        raise DragonNotFound()
    return await dragons_service.add_distribution_to_dragon(
        dragon, distribution_uid, session
    )


@dragons_router.post("/{dragon_uid}/images/{image_uid}", status_code=status.HTTP_200_OK, response_model=DragonModel)
async def add_image_to_dragon(
    dragon_uid: uuid.UUID | str,
    image_uid: uuid.UUID | str,
    session: AsyncSession = Depends(get_session)
) -> DragonModel:
    dragon = await dragons_service.get_dragon(dragon_uid, session)
    if not dragon:
        raise DragonNotFound()
    return await dragons_service.add_image_to_dragon(dragon, image_uid, session)


@dragons_router.patch("/{dragon_uid}", response_model=DragonModel, status_code=status.HTTP_200_OK)
async def update_dragon(
    dragon_uid: uuid.UUID | str,
    dragon_data: DragonUpdateModel,
    session: AsyncSession = Depends(get_session)
) -> DragonModel:
    dragon = await dragons_service.get_dragon(dragon_uid, session)
    if not dragon:
        raise DragonNotFound()
    return await dragons_service.update_dragon(dragon, dragon_data, session)


@dragons_router.delete("/{dragon_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_dragon(
    dragon_uid: uuid.UUID | str,
    session: AsyncSession = Depends(get_session)
) -> None:
    deleted_dragon = await dragons_service.delete_dragon(dragon_uid, session)
    if not deleted_dragon:
        raise DragonNotFound()
    return None
