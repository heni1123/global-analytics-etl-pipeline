import aiohttp
import asyncio
import logging
from typing import Dict, List, Any

class WorldUniversitiesDatabaseExtractor:
    def __init__(self, config: Dict) -> None:
        self.config = config
        self.base_url = config["url"]
        self.session = None
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

    async def extract(self) -> List[Dict[str, Any]]:
        try:
            self.session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=10, connect=30),
                headers={"User-Agent": "ETL-Agent/1.0"}
            )
            universities = await self._fetch_page({})
            return universities
        except Exception as e:
            self.logger.error(f"Error during extraction: {e}")
            raise

    async def _fetch_page(self, params: Dict) -> List[Dict[str, Any]]:
        response = await self._retry_with_backoff(self.session.get, self.base_url, params=params)
        if response.status == 200:
            data = await response.json()
            return data
        elif response.status == 429:
            await self._handle_rate_limit(response)
        elif 500 <= response.status < 600:
            await self._retry_with_backoff(self.session.get, self.base_url, params=params)
        else:
            self.logger.error(f"Unrecoverable error: {response.status}")
            raise Exception(f"HTTP Error: {response.status}")

    async def _handle_rate_limit(self, response) -> None:
        self.logger.warning("Rate limit exceeded, handling backoff.")
        await asyncio.sleep(5)  # Simple backoff strategy

    async def _retry_with_backoff(self, func, *args) -> Any:
        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                response = await func(*args)
                return response
            except Exception as e:
                self.logger.warning(f"Attempt {attempt + 1} failed: {e}")
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
        self.logger.error("Max retries exceeded.")
        raise Exception("Max retries exceeded.")

    async def close(self) -> None:
        if self.session:
            await self.session.close()