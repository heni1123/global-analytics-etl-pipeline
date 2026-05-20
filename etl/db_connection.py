import asyncpg
import logging
from typing import Any, Dict

class DatabaseConnection:
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.pool = None

    async def setup(self) -> None:
        try:
            self.pool = await asyncpg.create_pool(self.database_url)
            logging.info("Database connection pool created successfully.")
        except Exception as e:
            logging.error(f"Error creating database connection pool: {e}")
            raise

    async def close(self) -> None:
        if self.pool:
            await self.pool.close()
            logging.info("Database connection pool closed.")

    async def fetch(self, query: str, *args: Any) -> Any:
        async with self.pool.acquire() as connection:
            try:
                result = await connection.fetch(query, *args)
                return result
            except Exception as e:
                logging.error(f"Error executing fetch query: {query} | Error: {e}")
                raise

    async def execute(self, query: str, *args: Any) -> None:
        async with self.pool.acquire() as connection:
            try:
                await connection.execute(query, *args)
            except Exception as e:
                logging.error(f"Error executing query: {query} | Error: {e}")
                raise

database_connection = DatabaseConnection("postgresql://user:password@localhost/global_analytics_dw")