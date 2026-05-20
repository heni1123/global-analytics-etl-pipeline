import aiohttp
import asyncio
import logging
from typing import Dict, List, Any

class CurrencyExchangeRatesExtractor:
    def __init__(self, config: Dict) -> None:
        self.config = config
        self.base_url = config["url"]
        self.session = None
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

    async def extract(self) -> List[Dict[str, Any]]:
        try:
            response = await self._retry_with_backoff(self._fetch_page, {})
            return [
                {
                    "base_code": response["base_code"],
                    "time_last_update_unix": response["time_last_update_unix"],
                    "time_last_update_utc": response["time_last_update_utc"],
                    "time_next_update_unix": response["time_next_update_unix"],
                    "rates": response["rates"],
                }
            ]
        except Exception as e:
            self.logger.error(f"Extraction failed: {e}")
            raise

    async def _fetch_page(self, params: Dict) -> Dict:
        async with self.session.get(self.base_url, params=params) as response:
            if response.status == 200:
                return await response.json()
            elif response.status == 429:
                await self._handle_rate_limit(response)
            elif response.status >= 500:
                self.logger.warning(f"Server error: {response.status}")
                raise Exception(f"Server error: {response.status}")
            else:
                self.logger.error(f"Unrecoverable error: {response.status}")
                raise Exception(f"Unrecoverable error: {response.status}")

    async def _handle_rate_limit(self, response) -> None:
        retry_after = int(response.headers.get("Retry-After", 1))
        self.logger.warning(f"Rate limit exceeded, retrying after {retry_after} seconds.")
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

    async def start(self) -> None:
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=10, connect=30),
            headers={"User-Agent": "ETL-Agent/1.0"}
        )