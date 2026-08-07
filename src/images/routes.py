import uuid
from typing import List
from fastapi import APIRouter, Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from .schemas import ImageModel, ImageCreateModel
from .service import ImagesService
from src.errors import ImageNotFound

images_router = APIRouter()
images_service = ImagesService()


@images_router.get("/", response_model=List[ImageModel], status_code=status.HTTP_200_OK)
async def get_all_images(
    session: AsyncSession = Depends(get_session),
) -> List[ImageModel]:
    return await images_service.get_all_images(session)


@images_router.get("/{image_uid}", response_model=ImageModel, status_code=status.HTTP_200_OK)
async def get_image_by_uid(
    image_uid: uuid.UUID | str,
    session: AsyncSession = Depends(get_session)
) -> ImageModel:
    image = await images_service.get_image_by_uid(image_uid, session)
    if image is not None:
        return image
    else:
        raise ImageNotFound()


@images_router.post("/", response_model=ImageModel, status_code=status.HTTP_201_CREATED)
async def create_a_image(
    image_data: ImageCreateModel,
    session: AsyncSession = Depends(get_session)
) -> ImageModel:
    return await images_service.create_a_image(image_data, session)


@images_router.delete("/{image_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_image(
    image_uid: uuid.UUID | str,
    session: AsyncSession = Depends(get_session)
) -> None:
    image_to_delete = await images_service.delete_image(image_uid, session)

    if not image_to_delete:
        raise ImageNotFound()
    else:
        return None
