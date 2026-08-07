import uuid
from typing import List, Optional
from sqlmodel import desc, select
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.models import Image
from .schemas import ImageCreateModel


class ImagesService:
    async def get_all_images(self, session: AsyncSession) -> List[Image]:
        statement = select(Image).order_by(desc(Image.created_at))
        result = await session.exec(statement)
        return list(result.all())

    async def get_image_by_uid(
        self, image_uid: uuid.UUID | str, session: AsyncSession
    ) -> Optional[Image]:
        statement = select(Image).where(Image.uid == image_uid)
        result = await session.exec(statement)
        return result.first()

    async def create_a_image(
        self, image_data: ImageCreateModel, session: AsyncSession
    ) -> Image:
        new_image = Image(**image_data.model_dump())
        session.add(new_image)
        await session.commit()
        await session.refresh(new_image)
        return new_image

    async def delete_image(
        self, image_uid: uuid.UUID | str, session: AsyncSession
    ) -> Optional[Image]:
        image_to_delete = await self.get_image_by_uid(image_uid, session)
        if image_to_delete is None:
            return None
        await session.delete(image_to_delete)
        await session.commit()
        return image_to_delete
