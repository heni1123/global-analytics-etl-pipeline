import asyncio
import logging
import aiohttp
from typing import Dict, Any
from db_connection import get_connection_pool

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ExchangeRatesLoader:
    def __init__(self):
        self.pool = get_connection_pool()

    async def load_exchange_rates(self) -> None:
        exchange_rates_data = await self.extract_exchange_rates()
        await self.transform_and_load(exchange_rates_data)

    async def extract_exchange_rates(self) -> Dict[str, Any]:
        url = "https://open.er-api.com/v6/latest/USD"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    logger.error(f"Failed to fetch exchange rates: {response.status}")
                    raise Exception("API request failed")
                data = await response.json()
                logger.info("Successfully fetched exchange rates data")
                return data

    async def transform_and_load(self, Dict[str, Any]) -> None:
        async with self.pool.acquire() as connection:
            async with connection.transaction():
                rates = data.get("rates", {})
                for currency, rate in rates.items():
                    await self.insert_exchange_rate(connection, currency, rate)

    async def insert_exchange_rate(self, connection, currency: str, rate: float) -> None:
        query = """
        INSERT INTO public.dim_exchange_rates (currency_code, exchange_rate, snapshot_date)
        VALUES ($1, $2, NOW())
        ON CONFLICT (currency_code) DO UPDATE SET exchange_rate = EXCLUDED.exchange_rate, snapshot_date = NOW();
        """
        try:
            await connection.execute(query, currency, rate)
            logger.info(f"Inserted/Updated exchange rate for {currency}: {rate}")
        except Exception as e:
            logger.error(f"Error inserting exchange rate for {currency}: {e}")
            raise

if __name__ == "__main__":
    loader = ExchangeRatesLoader()
    asyncio.run(loader.load_exchange_rates())