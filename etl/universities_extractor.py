import aiohttp
import asyncio
import logging
from typing import List, Dict, Any
from db_connection import get_connection_pool

class UniversitiesExtractor:
    def __init__(self):
        self.api_url = "http://universities.hipolabs.com/search"
        self.logger = logging.getLogger(__name__)

    async def fetch_universities(self) -> List[Dict[str, Any]]:
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(self.api_url) as response:
                    response.raise_for_status()
                    data = await response.json()
                    return self.extract_relevant_fields(data)
            except aiohttp.ClientError as e:
                self.logger.error(f"Error fetching universities {e}")
                return []

    def extract_relevant_fields(self, List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        universities = []
        for item in data:
            university = {
                "name": item.get("name"),
                "country": item.get("country"),
                "alpha_two_code": item.get("alpha_two_code"),
            }
            universities.append(university)
        return universities

    async def run(self) -> None:
        universities_data = await self.fetch_universities()
        if universities_data:
            self.logger.info(f"Fetched {len(universities_data)} universities.")
        else:
            self.logger.warning("No universities data fetched.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    extractor = UniversitiesExtractor()
    asyncio.run(extractor.run())