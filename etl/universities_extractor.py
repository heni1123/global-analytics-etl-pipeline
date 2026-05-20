import aiohttp
import asyncio
import logging
from typing import List, Dict, Any
from db_connection import get_connection_pool

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UniversitiesExtractor:
    API_URL = "http://universities.hipolabs.com/search"

    async def fetch_universities(self) -> List[Dict[str, Any]]:
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(self.API_URL) as response:
                    response.raise_for_status()
                    data = await response.json()
                    return self.extract_fields(data)
            except aiohttp.ClientError as e:
                logger.error(f"Error fetching universities {e}")
                return []

    def extract_fields(self, List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        extracted_data = []
        for item in data:
            university_info = {
                "name": item.get("name"),
                "country": item.get("country"),
                "alpha_two_code": item.get("alpha_two_code"),
                "state_province": item.get("state-province")
            }
            extracted_data.append(university_info)
        return extracted_data

    async def run(self) -> None:
        universities = await self.fetch_universities()
        logger.info(f"Extracted {len(universities)} universities data.")
        # Further processing can be done here, such as loading to the database.