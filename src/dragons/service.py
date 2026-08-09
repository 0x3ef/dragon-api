import uuid
from typing import List, Optional
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.models import Dragon, Ability, Distribution, Image
from .schemas import DragonCreateModel, DragonUpdateModel
from src.abilities.service import AbilitiesService
from src.distributions.service import DistributionsService
from src.errors import AbilityNotFound, DistributionNotFound


class DragonService:
    def __init__(self):
        self.abilities_service =AbilitiesService()
        self.distributions_service = DistributionsService()

    async def get_all_dragons(self, session: AsyncSession) -> List[Dragon]:
        statement = select(Dragon)
        result = await session.exec(statement)
        return result.all()

    async def get_dragon(self, dragon_uid: uuid.UUID | str, session: AsyncSession) -> Optional[Dragon]:
        statement = select(Dragon).where(Dragon.uid == dragon_uid)
        result = await session.exec(statement)
        return result.first()
    
    async def get_dragon_by_species(self, dragon_species: str, session: AsyncSession) -> Optional[Dragon]:
        statement = select(Dragon).where(Dragon.species == dragon_species)
        result = await session.exec(statement)
        return result.first()

    async def get_dragon_abilities(self, dragon: Dragon, session: AsyncSession) -> List[Ability]:
        statement = select(Ability).join(Ability.dragons).where(Dragon.uid == dragon.uid)
        result = await session.exec(statement)
        return result.all()

    async def get_dragon_distributions(self, dragon: Dragon, session: AsyncSession) -> List[Distribution]:
        statement = select(Distribution).join(Distribution.dragons).where(Dragon.uid == dragon.uid)
        result = await session.exec(statement)
        return result.all()

    async def get_dragon_images(self, dragon: Dragon, session: AsyncSession) -> List[Image]:
        statement = select(Image).join(Image.dragon).where(Dragon.uid == dragon.uid)
        result = await session.exec(statement)
        return result.all()

    async def create_dragon(self, dragon_data: DragonCreateModel, session: AsyncSession) -> Dragon:
        dragon_dict = dragon_data.model_dump(exclude={"abilities", "distributions"})
        new_dragon = Dragon(**dragon_dict)

        for ability_uid in dragon_data.abilities:
            ability = await self.abilities_service.get_ability_by_uid(ability_uid, session)
            if not ability: raise AbilityNotFound()
            new_dragon.abilities.append(ability)

        for distribution_uid in dragon_data.distributions:
            distribution = await self.distributions_service.get_distribution_by_uid(distribution_uid, session)
            if not distribution: raise DistributionNotFound()
            new_dragon.distributions.append(distribution)

        session.add(new_dragon)
        await session.commit()
        await session.refresh(new_dragon)
        return new_dragon

    async def create_dragon_with_relations(
        self,
        dragon_data: DragonCreateModel,
        abilities: List[Ability],
        distributions: List[Distribution],
        session: AsyncSession
    ) -> Dragon:
        new_dragon = Dragon(**dragon_data.model_dump(exclude={"abilities", "distributions"}))
        new_dragon.abilities = abilities
        new_dragon.distributions = distributions
        session.add(new_dragon)
        await session.commit()
        await session.refresh(new_dragon)
        return new_dragon

    async def add_ability_to_dragon(self, dragon: Dragon, ability_uid: uuid.UUID | str, session: AsyncSession) -> Dragon:
        ability = await self.abilities_service.get_ability_by_uid(ability_uid, session)
        if ability and ability not in dragon.abilities:
            dragon.abilities.append(ability)
            session.add(dragon)
            await session.commit()
            await session.refresh(dragon)
        return dragon

    async def add_distribution_to_dragon(self, dragon: Dragon, distribution_uid: uuid.UUID | str, session: AsyncSession) -> Dragon:
        distribution = await self.distributions_service.get_distribution_by_uid(distribution_uid, session)
        if distribution and distribution not in dragon.distributions:
            dragon.distributions.append(distribution)
            session.add(dragon)
            await session.commit()
            await session.refresh(dragon)
        return dragon

    async def update_dragon(self, dragon: Dragon, dragon_data: DragonUpdateModel, session: AsyncSession) -> Dragon:
        simple_fields = dragon_data.model_dump(
            exclude_unset=True,
            exclude={
                "ability_uids_add",
                "ability_uids_remove",
                "distribution_uids_add",
                "distribution_uids_remove",
                "features_add",
                "features_remove",
                "colors_add",
                "colors_remove",
                "diet_add",
                "diet_remove",
                "habitat_add",
                "habitat_remove",
            },
        )

        for k, v in simple_fields.items():
            setattr(dragon, k, v)

        if dragon_data.ability_uids_add:
            for ability_uid in dragon_data.ability_uids_add:
                ability = await self.abilities_service.get_ability_by_uid(ability_uid, session)
                if ability and ability not in dragon.abilities: dragon.abilities.append(ability)

        if dragon_data.ability_uids_remove:
            remove_set = set(dragon_data.ability_uids_remove)
            dragon.abilities = [ability for ability in dragon.abilities if ability.uid not in remove_set]

        if dragon_data.distribution_uids_add:
            for distribution_uid in dragon_data.distribution_uids_add:
                distribution = await self.distributions_service.get_distribution_by_uid(distribution_uid, session)
                if distribution and distribution not in dragon.distributions: dragon.distributions.append(distribution)

        if dragon_data.distribution_uids_remove:
            remove_set = set(dragon_data.distribution_uids_remove)
            dragon.distributions = [d for d in dragon.distributions if str(d.uid) not in remove_set]

        if dragon_data.features_add:
            dragon.features += dragon_data.features_add
        if dragon_data.features_remove:
            remove = set(dragon_data.features_remove)
            dragon.features = [f for f in dragon.features if f not in remove]

        if dragon_data.colors_add:
            dragon.colors += dragon_data.colors_add
        if dragon_data.colors_remove:
            remove = set(dragon_data.colors_remove)
            dragon.colors = [c for c in dragon.colors if c not in remove]

        if dragon_data.diet_add:
            dragon.diet += dragon_data.diet_add
        if dragon_data.diet_remove:
            remove = set(dragon_data.diet_remove)
            dragon.diet = [d for d in dragon.diet if d not in remove]

        if dragon_data.habitat_add:
            dragon.habitat += dragon_data.habitat_add
        if dragon_data.habitat_remove:
            remove = set(dragon_data.habitat_remove)
            dragon.habitat = [h for h in dragon.habitat if h not in remove]

        session.add(dragon)
        await session.commit()
        await session.refresh(dragon)
        return dragon

    async def delete_dragon(self, dragon_uid: uuid.UUID | str, session: AsyncSession) -> Optional[Dragon]:
        dragon = await self.get_dragon(dragon_uid, session)
        if not dragon: return None
        await session.delete(dragon)
        await session.commit()
        return dragon 
