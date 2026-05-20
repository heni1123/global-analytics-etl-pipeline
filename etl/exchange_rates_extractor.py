import aiohttp
import asyncio
import logging
from typing import Dict, Any, List
from db_connection import get_connection_pool

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ExchangeRatesExtractor:
    API_URL = "https://open.er-api.com/v6/latest/USD"

    async def fetch_exchange_rates(self) -> List[Dict[str, Any]]:
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(self.API_URL) as response:
                    response.raise_for_status()
                    data = await response.json()
                    return self.transform_data(data)
            except aiohttp.ClientError as e:
                logger.error(f"Error fetching exchange rates: {e}")
                return []

    def transform_data(self, Dict[str, Any]) -> List[Dict[str, Any]]:
        rates = data.get("rates", {})
        transformed_data = []
        for currency, rate in rates.items():
            transformed_data.append({
                "currency_code": currency,
                "exchange_rate": rate,
                "base_currency": "USD"
            })
        return transformed_data

async def main():
    extractor = ExchangeRatesExtractor()
    exchange_rates = await extractor.fetch_exchange_rates()
    logger.info(f"Extracted exchange rates: {exchange_rates}")

if __name__ == "__main__":
    asyncio.run(main())