import uuid
from typing import List, Optional
from sqlmodel import desc, select
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.models import Distribution
from .schemas import DistributionCreateModel


class DistributionsService:
    async def get_all_distributions(self, session: AsyncSession) -> List[Distribution]:
        statement = select(Distribution).order_by(desc(Distribution.created_at))
        result = await session.exec(statement)
        return list(result.all())

    async def get_distribution_by_uid(self, distribution_uid: uuid.UUID | str, session: AsyncSession) -> Optional[Distribution]:
        statement = select(Distribution).where(Distribution.uid == distribution_uid)
        result = await session.exec(statement)
        return result.first()

    async def get_distribution_by_name(self, distribution_name: str, session: AsyncSession) -> Optional[Distribution]:
        statement = select(Distribution).where(Distribution.name == distribution_name)
        result = await session.exec(statement)
        return result.first()

    async def create_distribution(self, distribution_data: DistributionCreateModel, session: AsyncSession) -> Distribution:
        new_distribution = Distribution(**distribution_data.model_dump())
        session.add(new_distribution)
        await session.commit()
        await session.refresh(new_distribution)
        return new_distribution

    async def delete_distribution(self, distribution_uid: uuid.UUID | str, session: AsyncSession) -> Optional[Distribution]:
        distribution_to_delete = await self.get_distribution_by_uid(distribution_uid, session)
        if distribution_to_delete is None: return None
        await session.delete(distribution_to_delete)
        await session.commit()
        return distribution_to_delete
