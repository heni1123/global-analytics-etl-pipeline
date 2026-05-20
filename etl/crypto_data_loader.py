import asyncio
import logging
from typing import List, Dict, Any
from db_connection import get_connection_pool

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CryptoDataLoader:
    def __init__(self):
        self.pool = get_connection_pool()

    async def transform_and_load(self, crypto_List[Dict[str, Any]]) -> None:
        transformed_data = self.apply_business_rules(crypto_data)
        await self.load_data(transformed_data)

    def apply_business_rules(self, crypto_List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        for row in crypto_data:
            row['market_cap_category'] = self.categorize_market_cap(row['market_cap'])
            row['volatility_flag'] = self.flag_volatility(row['price_change_percentage_24h'])
        return crypto_data

    @staticmethod
    def categorize_market_cap(market_cap: float) -> str:
        if market_cap > 100000000000:
            return 'Large'
        elif market_cap > 10000000000:
            return 'Medium'
        else:
            return 'Small'

    @staticmethod
    def flag_volatility(price_change_pct: float) -> bool:
        return abs(price_change_pct) > 5

    async def load_data(self, transformed_List[Dict[str, Any]]) -> None:
        async with self.pool.acquire() as connection:
            async with connection.transaction():
                for row in transformed_data:
                    await self.upsert_crypto_market_data(connection, row)

    async def upsert_crypto_market_data(self, connection, row: Dict[str, Any]) -> None:
        query = """
        INSERT INTO public.fact_crypto_markets (crypto_id, name, symbol, market_cap, price, price_change_percentage_24h, market_cap_category, volatility_flag, snapshot_date)
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8, CURRENT_DATE)
        ON CONFLICT (crypto_id, snapshot_date) DO UPDATE SET
            name = EXCLUDED.name,
            symbol = EXCLUDED.symbol,
            market_cap = EXCLUDED.market_cap,
            price = EXCLUDED.price,
            price_change_percentage_24h = EXCLUDED.price_change_percentage_24h,
            market_cap_category = EXCLUDED.market_cap_category,
            volatility_flag = EXCLUDED.volatility_flag;
        """
        try:
            await connection.execute(query, row['id'], row['name'], row['symbol'], row['market_cap'], row['current_price'], row['price_change_percentage_24h'], row['market_cap_category'], row['volatility_flag'])
            logger.info(f"Upserted data for crypto_id: {row['id']}")
        except Exception as e:
            logger.error(f"Error upserting data for crypto_id: {row['id']}, error: {e}")