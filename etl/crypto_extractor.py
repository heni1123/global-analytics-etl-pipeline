import aiohttp
import asyncio
import logging
from typing import List, Dict, Any
from db_connection import get_connection_pool

class CryptoExtractor:
    def __init__(self):
        self.api_url = "https://api.coingecko.com/api/v3/coins/markets"
        self.logger = logging.getLogger(__name__)

    async def fetch_data(self) -> List[Dict[str, Any]]:
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(self.api_url) as response:
                    response.raise_for_status()
                    data = await response.json()
                    return self.extract_relevant_fields(data)
            except aiohttp.ClientError as e:
                self.logger.error(f"API request failed: {e}")
                return []
            except Exception as e:
                self.logger.error(f"An error occurred: {e}")
                return []

    def extract_relevant_fields(self, List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        extracted_data = []
        for item in data:
            extracted_data.append({
                "id": item.get("id"),
                "symbol": item.get("symbol"),
                "name": item.get("name"),
                "current_price": item.get("current_price"),
                "market_cap": item.get("market_cap"),
                "total_volume": item.get("total_volume"),
            })
        return extracted_data

    async def run(self) -> None:
        data = await self.fetch_data()
        if data:
            self.logger.info(f"Extracted {len(data)} cryptocurrency records.")
        else:
            self.logger.warning("No data extracted.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    extractor = CryptoExtractor()
    asyncio.run(extractor.run())