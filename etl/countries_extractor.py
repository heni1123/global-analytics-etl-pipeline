import aiohttp
import asyncio
import logging
from typing import List, Dict, Any
from db_connection import get_connection_pool

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CountriesExtractor:
    def __init__(self):
        self.api_url = "https://restcountries.com/v3.1/all"

    async def fetch_countries_data(self) -> List[Dict[str, Any]]:
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(self.api_url) as response:
                    response.raise_for_status()
                    data = await response.json()
                    return self.extract_fields(data)
            except aiohttp.ClientError as e:
                logger.error(f"Error fetching countries {e}")
                return []

    def extract_fields(self, List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        countries = []
        for country in data:
            country_info = {
                "cca3": country.get("cca3"),
                "cca2": country.get("cca2"),
                "name": country.get("name", {}).get("common"),
                "region": country.get("region"),
                "subregion": country.get("subregion"),
                "population": country.get("population"),
            }
            countries.append(country_info)
        return countries

    async def run(self) -> None:
        countries_data = await self.fetch_countries_data()
        logger.info(f"Extracted {len(countries_data)} countries data.")
        # Here you would typically pass the data to the loader or further processing

if __name__ == "__main__":
    extractor = CountriesExtractor()
    asyncio.run(extractor.run())