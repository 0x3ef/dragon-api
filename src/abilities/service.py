import uuid
from typing import List, Optional
from sqlmodel import desc, select
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.models import Ability
from .schemas import AbilityCreateModel


class AbilitiesService:
    async def get_all_abilities(self, session: AsyncSession) -> List[Ability]:
        statement = select(Ability).order_by(desc(Ability.created_at))
        result = await session.exec(statement)
        return list(result.all())

    async def get_ability_by_uid(self, ability_uid: uuid.UUID | str, session: AsyncSession) -> Optional[Ability]:
        statement = select(Ability).where(Ability.uid == ability_uid)
        result = await session.exec(statement)
        return result.first()

    async def get_ability_by_name(self, name_ability: str, session: AsyncSession) -> Optional[Ability]:
        statement = select(Ability).where(Ability.name == name_ability)
        result = await session.exec(statement)
        return result.first()

    async def create_ability(self, ability_data: AbilityCreateModel, session: AsyncSession) -> Ability:
        new_ability = Ability(**ability_data.model_dump())
        session.add(new_ability)
        await session.commit()
        await session.refresh(new_ability)
        return new_ability

    async def delete_ability(self, ability_uid: uuid.UUID | str, session: AsyncSession) -> Optional[Ability]:
        ability_to_delete = await self.get_ability_by_uid(ability_uid, session)
        if ability_to_delete is None: return None
        await session.delete(ability_to_delete)
        await session.commit()
        return ability_to_delete
