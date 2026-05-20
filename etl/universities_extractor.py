import aiohttp
import asyncio
import logging
from typing import List, Dict, Any
from db_connection import get_connection_pool

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UniversitiesExtractor:
    def __init__(self):
        self.url = "http://universities.hipolabs.com/search"

    async def fetch_universities(self) -> List[Dict[str, Any]]:
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(self.url) as response:
                    response.raise_for_status()
                    data = await response.json()
                    logger.info("Successfully fetched university data.")
                    return data
            except aiohttp.ClientError as e:
                logger.error(f"Error fetching university {e}")
                return []

    async def extract(self) -> List[Dict[str, Any]]:
        universities_data = await self.fetch_universities()
        extracted_data = []
        for university in universities_data:
            extracted_data.append({
                "name": university.get("name"),
                "country": university.get("country"),
                "alpha_two_code": university.get("alpha_two_code"),
                "state_province": university.get("state-province", None)
            })
        logger.info(f"Extracted {len(extracted_data)} universities.")
        return extracted_data

async def main():
    extractor = UniversitiesExtractor()
    universities = await extractor.extract()
    # Here you would typically pass the data to the loader or further processing

if __name__ == "__main__":
    asyncio.run(main())