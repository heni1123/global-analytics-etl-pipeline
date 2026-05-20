import aiohttp
import asyncio
import logging
from typing import List, Dict, Any

class DataExtractor:
    BASE_URL = "https://api.coingecko.com/api/v3/coins/markets"
    MAX_RETRIES = 3
    TIMEOUT = (10, 30)
    USER_AGENT = "ETL-Agent/1.0"

    def __init__(self) -> None:
        self.session: aiohttp.ClientSession = None
        logging.basicConfig(level=logging.INFO)

    async def extract(self) -> List[Dict[str, Any]]:
        if self.session is None:
            self.session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(*self.TIMEOUT))

        attempt = 0
        while attempt < self.MAX_RETRIES:
            try:
                async with self.session.get(self.BASE_URL, headers={"User-Agent": self.USER_AGENT}) as response:
                    if response.status == 200:
                        return await response.json()
                    elif response.status in {429, 500, 502, 503, 504}:
                        attempt += 1
                        wait_time = 2 ** attempt
                        logging.warning(f"Retrying in {wait_time} seconds due to status {response.status}. Attempt {attempt}.")
                        await asyncio.sleep(wait_time)
                    else:
                        response.raise_for_status()
            except aiohttp.ClientError as e:
                logging.error(f"Client error occurred: {e}")
                raise
            except Exception as e:
                logging.error(f"Unexpected error occurred: {e}")
                raise

        logging.error("Max retries exceeded.")
        raise Exception("Max retries exceeded.")

    async def close(self) -> None:
        if self.session:
            await self.session.close()