import asyncio
import logging
from typing import List, Dict
from db_connection import get_connection_pool

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ExchangeRatesLoader:
    def __init__(self):
        self.pool = get_connection_pool()

    async def load_exchange_rates(self, exchange_rates: List[Dict[str, float]]) -> None:
        async with self.pool.acquire() as connection:
            async with connection.transaction():
                try:
                    for rate in exchange_rates:
                        await self._upsert_exchange_rate(connection, rate)
                except Exception as e:
                    logger.error("Error loading exchange rates: %s", e)
                    raise

    async def _upsert_exchange_rate(self, connection, rate: Dict[str, float]) -> None:
        query = """
        INSERT INTO public.dim_exchange_rates (currency, rate, last_updated)
        VALUES ($1, $2, NOW())
        ON CONFLICT (currency) DO UPDATE SET rate = EXCLUDED.rate, last_updated = NOW();
        """
        await connection.execute(query, rate['currency'], rate['rate'])

    async def close(self) -> None:
        await self.pool.close()