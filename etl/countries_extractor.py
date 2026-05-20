import aiohttp
import asyncio
import logging
from typing import List, Dict, Any
from db_connection import get_connection_pool

class CountriesExtractor:
    def __init__(self):
        self.api_url = "https://restcountries.com/v3.1/all"
        self.logger = logging.getLogger(__name__)

    async def fetch_countries_data(self) -> List[Dict[str, Any]]:
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(self.api_url) as response:
                    response.raise_for_status()
                    countries_data = await response.json()
                    return self.extract_relevant_fields(countries_data)
            except aiohttp.ClientError as e:
                self.logger.error(f"Error fetching countries {e}")
                return []

    def extract_relevant_fields(self, countries_List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        extracted_data = []
        for country in countries_data:
            extracted_data.append({
                "cca3": country.get("cca3"),
                "cca2": country.get("cca2"),
                "name": country.get("name", {}).get("common"),
                "region": country.get("region"),
                "subregion": country.get("subregion"),
                "population": country.get("population"),
            })
        return extracted_data

    async def run(self) -> List[Dict[str, Any]]:
        countries_data = await self.fetch_countries_data()
        return countries_data

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    extractor = CountriesExtractor()
    loop = asyncio.get_event_loop()
    countries = loop.run_until_complete(extractor.run())
    print(countries)