import asyncpg
import logging
from typing import Any, Dict

class DatabaseConnection:
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.pool = None
        self.logger = logging.getLogger(__name__)

    async def connect(self) -> None:
        try:
            self.pool = await asyncpg.create_pool(self.database_url)
            self.logger.info("Database connection pool created successfully.")
        except Exception as e:
            self.logger.error(f"Error creating database connection pool: {e}")
            raise

    async def close(self) -> None:
        if self.pool:
            await self.pool.close()
            self.logger.info("Database connection pool closed.")

    async def execute(self, query: str, *args: Any) -> None:
        async with self.pool.acquire() as connection:
            async with connection.transaction():
                try:
                    await connection.execute(query, *args)
                    self.logger.info("Query executed successfully.")
                except Exception as e:
                    self.logger.error(f"Error executing query: {e}")
                    raise

    async def fetch(self, query: str, *args: Any) -> Any:
        async with self.pool.acquire() as connection:
            try:
                result = await connection.fetch(query, *args)
                self.logger.info("Query fetched successfully.")
                return result
            except Exception as e:
                self.logger.error(f"Error fetching {e}")
                raise

database_url = "postgresql://user:password@localhost:5432/global_analytics_dw"
db_connection = DatabaseConnection(database_url)