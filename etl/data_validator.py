import logging
from typing import List
import asyncpg
from db_connection import get_connection_pool

class DataValidator:
    def __init__(self):
        self.pool = get_connection_pool()

    async def validate_crypto_data(self) -> None:
        async with self.pool.acquire() as connection:
            try:
                result = await connection.fetch("SELECT crypto_id, snapshot_date FROM public.fact_crypto_markets")
                for row in result:
                    if row['crypto_id'] is None or row['snapshot_date'] is None:
                        logging.error(f"Validation failed for crypto {row}")
                        raise ValueError("Primary key fields cannot be null in fact_crypto_markets")
            except Exception as e:
                logging.exception("Error validating cryptocurrency %s", e)
                raise

    async def validate_country_data(self) -> None:
        async with self.pool.acquire() as connection:
            try:
                result = await connection.fetch("SELECT country_code FROM public.dim_countries")
                for row in result:
                    if row['country_code'] is None:
                        logging.error(f"Validation failed for country {row}")
                        raise ValueError("Primary key field cannot be null in dim_countries")
            except Exception as e:
                logging.exception("Error validating country %s", e)
                raise

    async def validate_university_data(self) -> None:
        async with self.pool.acquire() as connection:
            try:
                result = await connection.fetch("SELECT university_id FROM public.dim_universities")
                for row in result:
                    if row['university_id'] is None:
                        logging.error(f"Validation failed for university {row}")
                        raise ValueError("Primary key field cannot be null in dim_universities")
            except Exception as e:
                logging.exception("Error validating university %s", e)
                raise

    async def validate_exchange_rates_data(self) -> None:
        async with self.pool.acquire() as connection:
            try:
                result = await connection.fetch("SELECT * FROM public.dim_exchange_rates")
                if not result:
                    logging.error("Validation failed: dim_exchange_rates table is empty")
                    raise ValueError("dim_exchange_rates table cannot be empty")
            except Exception as e:
                logging.exception("Error validating exchange rates %s", e)
                raise

    async def run_validations(self) -> None:
        await self.validate_crypto_data()
        await self.validate_country_data()
        await self.validate_university_data()
        await self.validate_exchange_rates_data()