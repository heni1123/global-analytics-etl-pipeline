import logging
import asyncio
import aiohttp
from typing import Any, Dict, Optional

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
LOG_LEVEL = logging.INFO

logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
logger = logging.getLogger(__name__)

async def fetch_with_retries(url: str, retries: int = 3, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
    for attempt in range(retries):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    response.raise_for_status()
                    data = await response.json()
                    logger.info(f"Successfully fetched data from {url}")
                    return data
        except aiohttp.ClientError as e:
            logger.error(f"Attempt {attempt + 1} failed to fetch data from {url}: {e}")
            if attempt == retries - 1:
                logger.critical(f"All attempts to fetch data from {url} failed.")
                return None

def log_database_operation(operation: str, success: bool, details: Optional[str] = None) -> None:
    if success:
        logger.info(f"Database operation '{operation}' completed successfully.")
    else:
        logger.error(f"Database operation '{operation}' failed. Details: {details}")

async def execute_db_operation(query: str, params: Optional[Dict[str, Any]] = None) -> None:
    try:
        # Assuming a function `get_db_connection` exists to get a connection from the pool
        async with get_db_connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, params)
                logger.info(f"Executed query: {query} with params: {params}")
    except Exception as e:
        logger.error(f"Database operation failed: {e}")
        log_database_operation("execute_db_operation", False, str(e))
        raise

def setup_logging() -> None:
    logger.info("Logging setup complete.")