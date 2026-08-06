import uuid
from typing import List
from fastapi import APIRouter, Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from src.errors import ClassNotFound, ClassAlreadyExists
from .schemas import DragonClassCreateModel, DragonClassModel, DragonClassUpdateModel
from .service import DragonClassService

dragon_class_router = APIRouter()
dragon_class_service = DragonClassService()


@dragon_class_router.get("/", response_model=List[DragonClassModel])
async def get_all_classes(
    session: AsyncSession = Depends(get_session),
) -> List[DragonClassModel]:
    return await dragon_class_service.get_all_classes(session)


@dragon_class_router.get("/{class_uid}", response_model=DragonClassModel)
async def get_class(
    class_uid: uuid.UUID,
    session: AsyncSession = Depends(get_session),
) -> DragonClassModel:
    dragon_class = await dragon_class_service.get_class(class_uid, session)

    if not dragon_class:
        raise ClassNotFound() 
    else:
        return dragon_class


@dragon_class_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=DragonClassModel,
)
async def create_a_class(
    class_data: DragonClassCreateModel,
    session: AsyncSession = Depends(get_session),
) -> DragonClassModel:
    dragon_class = await dragon_class_service.get_class_by_name(class_data.name, session)
    if not dragon_class:
        return await dragon_class_service.create_class(class_data, session)
    else: 
        raise ClassAlreadyExists()

@dragon_class_router.patch("/{class_uid}", response_model=DragonClassModel)
async def update_class(
    class_uid: uuid.UUID,
    class_update_data: DragonClassUpdateModel,
    session: AsyncSession = Depends(get_session),
) -> DragonClassModel:
    updated_dragon_class = await dragon_class_service.update_class(class_uid, class_update_data, session)

    if not updated_dragon_class:
        raise ClassNotFound() 
    else:
        return updated_dragon_class


@dragon_class_router.delete("/{class_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_class(
    class_uid: uuid.UUID,
    session: AsyncSession = Depends(get_session),
):
    dragon_class_to_delete = await dragon_class_service.delete_class(class_uid, session)

    if not dragon_class_to_delete:
        raise ClassNotFound() 
    else:
        return None
