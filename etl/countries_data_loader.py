import asyncio
import logging
from typing import List, Dict, Any
from db_connection import get_connection_pool

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CountriesDataLoader:
    def __init__(self):
        self.pool = get_connection_pool()

    async def load_countries_data(self, countries: List[Dict[str, Any]]) -> None:
        async with self.pool.acquire() as connection:
            async with connection.transaction():
                for country in countries:
                    await self.upsert_country(connection, country)

    async def upsert_country(self, connection, country: Dict[str, Any]) -> None:
        country_code = country.get('cca2')
        country_name = country.get('name', {}).get('common')
        region = country.get('region')
        subregion = country.get('subregion')
        population = country.get('population')
        area = country.get('area')
        languages = ', '.join(country.get('languages', {}).values())
        currencies = ', '.join([currency['name'] for currency in country.get('currencies', {}).values()])

        query = """
        INSERT INTO public.dim_countries (country_code, country_name, region, subregion, population, area, languages, currencies)
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
        ON CONFLICT (country_code) DO UPDATE SET
            country_name = EXCLUDED.country_name,
            region = EXCLUDED.region,
            subregion = EXCLUDED.subregion,
            population = EXCLUDED.population,
            area = EXCLUDED.area,
            languages = EXCLUDED.languages,
            currencies = EXCLUDED.currencies;
        """
        try:
            await connection.execute(query, country_code, country_name, region, subregion, population, area, languages, currencies)
            logger.info(f"Upserted country: {country_name} ({country_code})")
        except Exception as e:
            logger.error(f"Error upserting country {country_name} ({country_code}): {e}")

    async def close(self) -> None:
        await self.pool.close()