import asyncio
import logging
import aiohttp
from typing import List, Dict, Any
from db_connection import get_connection_pool

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ExchangeRatesLoader:
    def __init__(self):
        self.pool = get_connection_pool()

    async def load_exchange_rates(self) -> None:
        exchange_rates_data = await self.extract_exchange_rates()
        await self.insert_exchange_rates(exchange_rates_data)

    async def extract_exchange_rates(self) -> List[Dict[str, Any]]:
        url = "https://open.er-api.com/v6/latest/USD"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    logger.error(f"Failed to fetch exchange rates: {response.status}")
                    raise Exception("API request failed")
                data = await response.json()
                return self.transform_exchange_rates(data)

    def transform_exchange_rates(self, Dict[str, Any]) -> List[Dict[str, Any]]:
        rates = data.get("rates", {})
        transformed_data = []
        for currency, rate in rates.items():
            transformed_data.append({
                "currency_code": currency,
                "exchange_rate": rate,
                "snapshot_date": data.get("date")
            })
        return transformed_data

    async def insert_exchange_rates(self, exchange_rates: List[Dict[str, Any]]) -> None:
        async with self.pool.acquire() as connection:
            async with connection.transaction():
                for rate in exchange_rates:
                    await connection.execute("""
                        INSERT INTO public.dim_exchange_rates (currency_code, exchange_rate, snapshot_date)
                        VALUES ($1, $2, $3)
                        ON CONFLICT (currency_code) DO UPDATE SET
                        exchange_rate = EXCLUDED.exchange_rate,
                        snapshot_date = EXCLUDED.snapshot_date
                    """, rate['currency_code'], rate['exchange_rate'], rate['snapshot_date'])
        logger.info("Exchange rates data loaded successfully.")

if __name__ == "__main__":
    loader = ExchangeRatesLoader()
    asyncio.run(loader.load_exchange_rates())