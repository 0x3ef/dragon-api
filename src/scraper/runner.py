import argparse
import asyncio
import logging

from tqdm import tqdm
from pydantic import ValidationError

from src.abilities.schemas import AbilityCreateModel
from src.abilities.service import AbilitiesService
from src.classes.schemas import DragonClassCreateModel
from src.classes.service import DragonClassService
from src.distributions.schemas import DistributionCreateModel
from src.distributions.service import DistributionsService
from src.dragons.schemas import DragonCreateModel
from src.dragons.service import DragonService
from src.images.schemas import ImageCreateModel
from src.images.service import ImagesService
from src.db.main import async_session

from .client import ScraperClient
from .parsers import ParserService


logger = logging.getLogger(__name__)


dragon_class_service = DragonClassService()
dragon_service = DragonService()
abilities_service = AbilitiesService()
distributions_service = DistributionsService()
images_service = ImagesService()
parser_service = ParserService()


async def run_scraper(url: str):

    logger.info("Starting scraper")

    async with ScraperClient(delay=1.5) as client:

        async with async_session() as session:

            # -------------------------------------------------
            # Fetch dragon classes
            # -------------------------------------------------

            logger.info("Fetching dragon classes")

            html = await client.fetch(url)

            if not html:
                logger.error("Failed to fetch dragon classes page")
                return

            classes_dragons = parser_service.extract_classes_with_dragons_urls(html)

            total_classes = len(classes_dragons)

            total_dragons = sum(len(dragon_class["dragons"]) for dragon_class in classes_dragons)

            logger.info("Classes found: %d",total_classes)

            logger.info("Dragons found: %d", total_dragons)

            # -------------------------------------------------
            # Process dragons
            # -------------------------------------------------

            with tqdm(total=total_dragons, desc="Scraping dragons", unit="dragon") as progress:

                for dragon_class_data in classes_dragons:

                    # -----------------------------------------
                    # Dragon class
                    # -----------------------------------------

                    existing_class = await dragon_class_service.get_class_by_name(dragon_class_data["name"], session)

                    if existing_class:
                        dragon_class = existing_class

                    else:
                        try:
                            class_data = DragonClassCreateModel(
                                name=dragon_class_data["name"],
                                description=dragon_class_data["description"],
                                icon=dragon_class_data["icon"],
                            )

                            dragon_class = await dragon_class_service.create_class(class_data, session)

                        except ValidationError as exc:
                            logger.warning("Skipping class '%s' due to invalid data: %s", dragon_class_data["name"], exc)

                            continue

                    # -----------------------------------------
                    # Dragons
                    # -----------------------------------------

                    for dragon in dragon_class_data["dragons"]:

                        try:
                            html = await client.fetch(dragon["url"])

                            if not html:
                                logger.warning("Skipping dragon '%s': page could not be fetched", dragon["name"])

                                continue

                            dragon_data = parser_service.extract_dragons_data(html)

                            if not dragon_data:
                                logger.warning("Skipping dragon '%s': no data was extracted", dragon["name"])

                                continue

                            # ---------------------------------
                            # Abilities
                            # ---------------------------------

                            abilities = []

                            for ability_data in dragon_data["abilities"]:

                                existing_ability = await abilities_service.get_ability_by_name(ability_data["name"], session)

                                if existing_ability:
                                    ability = existing_ability

                                else:
                                    new_ability_data = AbilityCreateModel(name=ability_data["name"])
                                    ability = await abilities_service.create_ability(new_ability_data, session)

                                abilities.append(ability)

                            # ---------------------------------
                            # Distributions
                            # ---------------------------------

                            distributions = []

                            for distribution_data in dragon_data["distributions"]:

                                existing_distribution = await distributions_service.get_distribution_by_name(distribution_data["name"], session)

                                if existing_distribution:
                                    distribution = existing_distribution

                                else:
                                    new_distribution_data = DistributionCreateModel(name=distribution_data["name"], alternatenames=distribution_data["alternatenames"])
                                    distribution = await distributions_service.create_distribution(new_distribution_data, session)

                                distributions.append(distribution)

                            # ---------------------------------
                            # Dragon
                            # ---------------------------------

                            existing_dragon = await dragon_service.get_dragon_by_species(dragon_data["species"], session)

                            if existing_dragon:
                                new_dragon = existing_dragon

                            else:
                                new_dragon_dict = {key: value for key, value in dragon_data.items() if key not in {"abilities", "distributions", "images"}}
                                new_dragon_dict["class_uid"] = dragon_class.uid

                                new_dragon_data = DragonCreateModel(**new_dragon_dict)

                                new_dragon = await dragon_service.create_dragon_with_relations(new_dragon_data, abilities, distributions, session)

                            # ---------------------------------
                            # Images
                            # ---------------------------------

                            for image_url in dragon_data["images"]:

                                if not image_url:
                                    continue

                                existing_image = await images_service.get_image_by_url(image_url, session)

                                if not existing_image:

                                    new_image_data = ImageCreateModel(dragon_uid=new_dragon.uid, url=image_url)

                                    await images_service.create_a_image(new_image_data, session)

                            logger.info("Successfully processed dragon: %s", dragon_data["species"])

                        except ValidationError as exc:
                            logger.warning("Skipping dragon '%s' due to invalid data: %s", dragon["name"], exc)

                        except Exception:
                            logger.exception("Unexpected error while processing dragon '%s'", dragon["name"])

                        finally:
                            progress.update(1)

            logger.info("Scraper finished successfully")


def main():
    parser = argparse.ArgumentParser(description="Scrape dragon data from a source URL")
    parser.add_argument("url", help="URL containing the dragon classes")
    args = parser.parse_args()
    asyncio.run(run_scraper(args.url))


if __name__ == "__main__":
    main()