import uuid
from typing import List
from fastapi import APIRouter, Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from src.errors import DistributionNotFound
from .schemas import DistributionModel, DistributionCreateModel
from .service import DistributionsService

distributions_router = APIRouter()
distributions_service = DistributionsService()


@distributions_router.get("/", response_model=List[DistributionModel], status_code=status.HTTP_200_OK)
async def get_all_distributions(
    session: AsyncSession = Depends(get_session)
) -> List[DistributionModel]:
    return await distributions_service.get_all_distributions(session)


@distributions_router.get("/{distribution_uid}", response_model=DistributionModel, status_code=status.HTTP_200_OK)
async def get_distribution_by_uid(
    distribution_uid: uuid.UUID | str,
    session: AsyncSession = Depends(get_session)
) -> DistributionModel:
    distribution = await distributions_service.get_distribution_by_uid(distribution_uid, session)
    if distribution is not None:
        return distribution
    else:
        raise DistributionNotFound()


@distributions_router.post("/", response_model=DistributionModel, status_code=status.HTTP_201_CREATED)
async def create_distribution(
    distribution_data: DistributionCreateModel,
    session: AsyncSession = Depends(get_session)
) -> DistributionModel:
    return await distributions_service.create_distribution(distribution_data, session)


@distributions_router.delete("/{distribution_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_distribution(
    distribution_uid: uuid.UUID | str,
    session: AsyncSession = Depends(get_session)
) -> None:
    distribution_to_delete = await distributions_service.delete_distribution(distribution_uid, session)

    if not distribution_to_delete:
        raise DistributionNotFound()
    else:
        return None
