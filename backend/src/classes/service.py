import uuid
from typing import List, Optional
from sqlmodel import desc, select
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.models import DragonClass
from .schemas import DragonClassCreateModel, DragonClassUpdateModel


class DragonClassService:
    async def get_all_classes(self, session: AsyncSession) -> List[DragonClass]:
        statement = select(DragonClass).order_by(desc(DragonClass.created_at))
        result = await session.exec(statement)
        return result.all()

    async def get_class(self, class_uid: uuid.UUID | str, session: AsyncSession) -> Optional[DragonClass]:
        statement = select(DragonClass).where(DragonClass.uid == class_uid)
        result = await session.exec(statement)
        return result.first()

    async def get_class_by_name(self, class_name: str, session: AsyncSession) -> Optional[DragonClass]:
        statement = select(DragonClass).where(DragonClass.name == class_name)
        result = await session.exec(statement)
        return result.first()

    async def create_class(self, class_data: DragonClassCreateModel, session: AsyncSession) -> DragonClass:
        dragon_class_data = class_data.model_dump()
        new_dragon_class = DragonClass(**dragon_class_data)
        session.add(new_dragon_class)
        await session.commit()
        return new_dragon_class 

    async def update_class(
        self, 
        class_uid: uuid.UUID | str, 
        class_update_data: DragonClassUpdateModel, 
        session: AsyncSession
    ) -> Optional[DragonClass]:
        class_to_update = await self.get_class(class_uid, session)
        if class_to_update is None: return None
        update_data_dict = class_update_data.model_dump(exclude_unset=True)
        for k, v in update_data_dict.items():
            setattr(class_to_update, k, v)
        await session.commit()
        return class_to_update 

    async def delete_class(self, class_uid: uuid.UUID | str, session: AsyncSession):
        class_to_delete = await self.get_class(class_uid, session)
        if class_to_delete is None: return None
        await session.delete(class_to_delete)
        await session.commit()
        return class_to_delete
