import aiohttp
import asyncio
import logging
from typing import Dict, Any

class ExchangeRatesExtractor:
    def __init__(self, url: str):
        self.url = url
        self.logger = logging.getLogger(__name__)

    async def fetch_exchange_rates(self) -> Dict[str, Any]:
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(self.url) as response:
                    response.raise_for_status()
                    data = await response.json()
                    self.logger.info("Successfully fetched exchange rates data.")
                    return data
            except aiohttp.ClientError as e:
                self.logger.error(f"Error fetching exchange rates: {e}")
                raise

    async def extract(self) -> Dict[str, Any]:
        return await self.fetch_exchange_rates()

# Example usage:
# extractor = ExchangeRatesExtractor("https://open.er-api.com/v6/latest/USD")
# exchange_rates = asyncio.run(extractor.extract())