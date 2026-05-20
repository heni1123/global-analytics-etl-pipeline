import asyncio
import logging
from typing import List, Dict, Any
from db_connection import get_connection_pool

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CryptoLoader:
    def __init__(self):
        self.pool = get_connection_pool()

    async def load_data(self, crypto_List[Dict[str, Any]], snapshot_date: str) -> None:
        async with self.pool.acquire() as connection:
            async with connection.transaction():
                for crypto in crypto_data:
                    await self.upsert_crypto_data(connection, crypto, snapshot_date)

    async def upsert_crypto_data(self, connection, crypto: Dict[str, Any], snapshot_date: str) -> None:
        try:
            query = """
            INSERT INTO public.fact_crypto_markets (crypto_id, name, symbol, current_price, market_cap, total_volume, 
            high_24h, low_24h, price_change_24h, snapshot_date)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
            ON CONFLICT (crypto_id, snapshot_date) DO UPDATE SET
            name = EXCLUDED.name,
            symbol = EXCLUDED.symbol,
            current_price = EXCLUDED.current_price,
            market_cap = EXCLUDED.market_cap,
            total_volume = EXCLUDED.total_volume,
            high_24h = EXCLUDED.high_24h,
            low_24h = EXCLUDED.low_24h,
            price_change_24h = EXCLUDED.price_change_24h;
            """
            await connection.execute(query, 
                crypto['id'], 
                crypto['name'], 
                crypto['symbol'], 
                crypto['current_price'], 
                crypto['market_cap'], 
                crypto['total_volume'], 
                crypto['high_24h'], 
                crypto['low_24h'], 
                crypto['price_change_24h'], 
                snapshot_date
            )
            logger.info(f"Upserted data for crypto_id: {crypto['id']} on {snapshot_date}")
        except Exception as e:
            logger.error(f"Error upserting data for crypto_id: {crypto['id']} - {str(e)}")