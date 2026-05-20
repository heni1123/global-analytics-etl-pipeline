import aiohttp
import asyncio
import logging
from typing import List, Dict, Any
from db_connection import get_connection_pool

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CountriesDataExtractor:
    API_URL = "https://restcountries.com/v3.1/all"

    async def fetch_countries_data(self) -> List[Dict[str, Any]]:
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(self.API_URL) as response:
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

async def main():
    extractor = CountriesDataExtractor()
    countries_data = await extractor.fetch_countries_data()
    logger.info(f"Extracted countries {countries_data}")

if __name__ == "__main__":
    asyncio.run(main())