import logging
from typing import List, Dict, Any
import asyncpg
from db_connection import get_connection_pool

class DataValidation:
    def __init__(self):
        self.pool = get_connection_pool()
        logging.basicConfig(level=logging.INFO)

    async def validate_crypto_data(self) -> None:
        async with self.pool.acquire() as connection:
            try:
                query = """
                SELECT COUNT(*) FROM public.fact_crypto_markets
                WHERE crypto_id IS NULL OR snapshot_date IS NULL
                """
                result = await connection.fetchval(query)
                if result > 0:
                    logging.error("Validation failed: Found %s rows with NULL primary keys in fact_crypto_markets", result)
                else:
                    logging.info("Validation passed for fact_crypto_markets")

                query = """
                SELECT COUNT(*) FROM public.fact_crypto_markets
                WHERE market_cap_category IS NULL OR volatility_flag IS NULL
                """
                result = await connection.fetchval(query)
                if result > 0:
                    logging.error("Validation failed: Found %s rows with NULL values in fact_crypto_markets", result)
                else:
                    logging.info("Validation passed for fact_crypto_markets data integrity")

            except Exception as e:
                logging.error("Error during crypto data validation: %s", e)

    async def validate_countries_data(self) -> None:
        async with self.pool.acquire() as connection:
            try:
                query = """
                SELECT COUNT(*) FROM public.dim_countries
                WHERE country_code IS NULL
                """
                result = await connection.fetchval(query)
                if result > 0:
                    logging.error("Validation failed: Found %s rows with NULL primary keys in dim_countries", result)
                else:
                    logging.info("Validation passed for dim_countries")

            except Exception as e:
                logging.error("Error during countries data validation: %s", e)

    async def validate_universities_data(self) -> None:
        async with self.pool.acquire() as connection:
            try:
                query = """
                SELECT COUNT(*) FROM public.dim_universities
                WHERE university_id IS NULL
                """
                result = await connection.fetchval(query)
                if result > 0:
                    logging.error("Validation failed: Found %s rows with NULL primary keys in dim_universities", result)
                else:
                    logging.info("Validation passed for dim_universities")

            except Exception as e:
                logging.error("Error during universities data validation: %s", e)

    async def validate_exchange_rates_data(self) -> None:
        async with self.pool.acquire() as connection:
            try:
                query = """
                SELECT COUNT(*) FROM public.dim_exchange_rates
                WHERE currency IS NULL OR rate IS NULL
                """
                result = await connection.fetchval(query)
                if result > 0:
                    logging.error("Validation failed: Found %s rows with NULL values in dim_exchange_rates", result)
                else:
                    logging.info("Validation passed for dim_exchange_rates data integrity")

            except Exception as e:
                logging.error("Error during exchange rates data validation: %s", e)

    async def run_validations(self) -> None:
        await self.validate_crypto_data()
        await self.validate_countries_data()
        await self.validate_universities_data()
        await self.validate_exchange_rates_data()