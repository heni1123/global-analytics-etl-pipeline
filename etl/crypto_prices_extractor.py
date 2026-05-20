import aiohttp
import asyncio
import logging
from typing import List, Dict, Any
from db_connection import get_connection_pool

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CryptoPricesExtractor:
    API_URL = "https://api.coingecko.com/api/v3/coins/markets"
    
    async def fetch_data(self) -> List[Dict[str, Any]]:
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(self.API_URL, params={"vs_currency": "usd"}) as response:
                    response.raise_for_status()
                    data = await response.json()
                    return self.extract_fields(data)
            except aiohttp.ClientError as e:
                logger.error(f"API request failed: {e}")
                return []
            except Exception as e:
                logger.error(f"An error occurred: {e}")
                return []

    def extract_fields(self, List[Dict[str, Any]]) -> List[Dict[str, Any]]:
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

async def main():
    extractor = CryptoPricesExtractor()
    data = await extractor.fetch_data()
    logger.info(f"Extracted {data}")

if __name__ == "__main__":
    asyncio.run(main())