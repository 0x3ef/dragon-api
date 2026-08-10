from typing import Optional
import asyncio
import logging
import httpx


logger = logging.getLogger(__name__)


class ScraperClient:
    def __init__(self, timeout: float = 10.0, delay: float = 1.0, max_retries: int = 5):
        self.delay = delay
        self.max_retries = max_retries
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
            "Accept": "text/html,application/xhtml+xml",
            "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
        }

        self.client = httpx.AsyncClient(headers=self.headers, timeout=timeout, follow_redirects=True)

    async def fetch(self, url: str) -> Optional[str]:
        if self.delay > 0:
            await asyncio.sleep(self.delay)

        for attempt in range(self.max_retries):
            try:
                logger.info("Fetching URL: %s (attempt %d/%d)", url, attempt + 1, self.max_retries)

                response = await self.client.get(url)
                response.raise_for_status()

                logger.info("Successfully fetched URL: %s", url)

                return response.text

            except httpx.HTTPStatusError as e:
                status = e.response.status_code

                logger.error("HTTP error %d while requesting URL: %s", status, url)

                if status in (400, 401, 403, 404):
                    break

            except httpx.RequestError as e:
                logger.warning("Request error while connecting to %s: %s", url, e)

            if attempt < self.max_retries - 1:
                wait_time = 2 ** attempt

                logger.info("Retrying request in %d seconds...", wait_time)

                await asyncio.sleep(wait_time)

        logger.error("Failed to fetch URL after %d attempts: %s", self.max_retries, url)

        return None

    async def close(self):
        await self.client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.close()