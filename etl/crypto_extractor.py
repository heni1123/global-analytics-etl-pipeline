import aiohttp
import asyncio
import logging
from typing import List, Dict, Any

class CryptoExtractor:
    API_URL = "https://api.coingecko.com/api/v3/coins/markets"
    
    def __init__(self) -> None:
        self.logger = self.setup_logging()

    def setup_logging(self) -> logging.Logger:
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)
        return logger

    async def fetch_data(self) -> List[Dict[str, Any]]:
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(self.API_URL) as response:
                    response.raise_for_status()
                    data = await response.json()
                    return self.extract_relevant_fields(data)
            except aiohttp.ClientError as e:
                self.logger.error(f"HTTP error occurred: {e}")
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

    async def run(self) -> List[Dict[str, Any]]:
        return await self.fetch_data()

if __name__ == "__main__":
    extractor = CryptoExtractor()
    loop = asyncio.get_event_loop()
    crypto_data = loop.run_until_complete(extractor.run())
    print(crypto_data)