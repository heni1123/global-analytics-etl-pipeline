import aiohttp
import asyncio
import logging
from typing import Dict, Any, List
from db_connection import get_connection_pool

class ExchangeRatesExtractor:
    def __init__(self):
        self.url = "https://open.er-api.com/v6/latest/USD"
        self.pool = get_connection_pool()

    async def fetch_exchange_rates(self) -> List[Dict[str, Any]]:
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(self.url) as response:
                    response.raise_for_status()
                    data = await response.json()
                    return self.parse_response(data)
            except aiohttp.ClientError as e:
                logging.error(f"Error fetching exchange rates: {e}")
                return []

    def parse_response(self, Dict[str, Any]) -> List[Dict[str, Any]]:
        rates = data.get("rates", {})
        exchange_rates = []
        for currency, rate in rates.items():
            exchange_rates.append({
                "currency_code": currency,
                "exchange_rate": rate,
                "snapshot_date": data.get("date")
            })
        return exchange_rates

    async def run(self) -> None:
        exchange_rates = await self.fetch_exchange_rates()
        if exchange_rates:
            await self.load_exchange_rates(exchange_rates)

    async def load_exchange_rates(self, exchange_rates: List[Dict[str, Any]]) -> None:
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

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    extractor = ExchangeRatesExtractor()
    asyncio.run(extractor.run())