import asyncio
import logging
import aiohttp
import pandas as pd
from typing import List, Dict, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataIngestion:
    def __init__(self, run_id: str) -> None:
        self.run_id = run_id
        self.api_urls = {
            "source_crypto_prices": "https://api.coingecko.com/api/v3/coins/markets",
            "source_countries_data": "https://restcountries.com/v3.1/all",
            "source_universities": "http://universities.hipolabs.com/search",
            "source_exchange_rates": "https://open.er-api.com/v6/latest/USD"
        }

    async def fetch_data(self, session: aiohttp.ClientSession, url: str) -> List[Dict[str, Any]]:
        try:
            async with session.get(url) as response:
                response.raise_for_status()
                data = await response.json()
                logger.info(f"Fetched data from {url}")
                return data
        except Exception as e:
            logger.error(f"Error fetching data from {url}: {e}")
            return []

    async def gather_data(self) -> Dict[str, List[Dict[str, Any]]]:
        async with aiohttp.ClientSession() as session:
            tasks = [self.fetch_data(session, url) for url in self.api_urls.values()]
            results = await asyncio.gather(*tasks)
            return dict(zip(self.api_urls.keys(), results))

    def run(self) -> None:
        logger.info("Starting data ingestion...")
        data = asyncio.run(self.gather_data())
        logger.info("Data ingestion completed.")
        self.process_data(data)

    def process_data(self, Dict[str, List[Dict[str, Any]]]) -> None:
        # Here you would implement data cleaning and normalization
        # For now, we will just log the data received
        logger.info("Processing data...")
        for source, records in data.items():
            logger.info(f"Source: {source}, Records: {len(records)}")
        # Further processing can be done here

if __name__ == "__main__":
    ingestion = DataIngestion(run_id="12345")
    ingestion.run()