import aiohttp
import asyncio
import logging
from typing import Dict, List, Any

class CryptocurrencyMarketDataExtractor:
    def __init__(self, config: Dict) -> None:
        self.config = config
        self.base_url = config["url"]
        self.session = None
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

    async def extract(self) -> List[Dict[str, Any]]:
        try:
            params = {}
            response = await self._retry_with_backoff(self._fetch_page, params)
            return response
        except Exception as e:
            self.logger.error(f"Extraction failed: {e}")
            raise

    async def _fetch_page(self, params: Dict) -> List[Dict[str, Any]]:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10, connect=30)) as session:
            self.session = session
            headers = {"User-Agent": "ETL-Agent/1.0"}
            async with session.get(self.base_url, params=params, headers=headers) as response:
                if response.status == 200:
                    return await response.json()
                elif response.status == 429:
                    await self._handle_rate_limit(response)
                elif response.status >= 500:
                    await self._retry_with_backoff(self._fetch_page, params)
                else:
                    self.logger.error(f"Unrecoverable error: {response.status}")
                    raise Exception(f"HTTP Error: {response.status}")

    async def _handle_rate_limit(self, response) -> None:
        retry_after = int(response.headers.get("Retry-After", 1))
        self.logger.warning(f"Rate limit exceeded. Retrying after {retry_after} seconds.")
        await asyncio.sleep(retry_after)

    async def _retry_with_backoff(self, func, *args) -> Any:
        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                return await func(*args)
            except Exception as e:
                if attempt < max_attempts - 1:
                    backoff_time = 2 ** attempt
                    self.logger.warning(f"Attempt {attempt + 1} failed: {e}. Retrying in {backoff_time} seconds.")
                    await asyncio.sleep(backoff_time)
                else:
                    self.logger.error(f"All attempts failed: {e}")
                    raise

    async def close(self) -> None:
        if self.session:
            await self.session.close()