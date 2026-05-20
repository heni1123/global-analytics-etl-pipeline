import aiohttp
import asyncio
import logging
from typing import Dict, List, Any

class WorldCountriesInformationExtractor:
    def __init__(self, config: Dict) -> None:
        self.config = config
        self.base_url = config["url"]
        self.session = None
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

    async def extract(self) -> List[Dict[str, Any]]:
        try:
            countries_data = await self._fetch_page({})
            return countries_data
        except Exception as e:
            self.logger.error(f"Error during extraction: {e}")
            raise

    async def _fetch_page(self, params: Dict) -> List[Dict[str, Any]]:
        url = self.base_url
        response = await self._retry_with_backoff(self._make_request, url, params)
        return response

    async def _make_request(self, url: str, params: Dict) -> List[Dict[str, Any]]:
        async with self.session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=10, connect=30), headers={"User-Agent": "ETL-Agent/1.0"}) as response:
            if response.status == 200:
                return await response.json()
            elif response.status == 429:
                await self._handle_rate_limit(response)
            elif 500 <= response.status < 600:
                raise Exception(f"Server error: {response.status}")
            else:
                raise Exception(f"Unrecoverable error: {response.status}")

    async def _handle_rate_limit(self, response) -> None:
        retry_after = int(response.headers.get("Retry-After", 1))
        self.logger.warning(f"Rate limit hit, retrying after {retry_after} seconds.")
        await asyncio.sleep(retry_after)

    async def _retry_with_backoff(self, func, *args) -> Any:
        attempts = 0
        while attempts < 3:
            try:
                return await func(*args)
            except Exception as e:
                attempts += 1
                backoff_time = 2 ** attempts
                self.logger.warning(f"Attempt {attempts} failed: {e}. Retrying in {backoff_time} seconds.")
                await asyncio.sleep(backoff_time)
        raise Exception("Max retries exceeded")

    async def close(self) -> None:
        if self.session:
            await self.session.close()

    async def start(self) -> None:
        self.session = aiohttp.ClientSession()
        try:
            await self.extract()
        finally:
            await self.close()