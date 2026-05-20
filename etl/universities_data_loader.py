import asyncio
import logging
from typing import List, Dict, Any
from db_connection import get_connection_pool

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UniversitiesDataLoader:
    def __init__(self):
        self.pool = get_connection_pool()

    async def load_universities_data(self, universities: List[Dict[str, Any]]) -> None:
        async with self.pool.acquire() as connection:
            async with connection.transaction():
                for university in universities:
                    await self.upsert_university(connection, university)

    async def upsert_university(self, connection, university: Dict[str, Any]) -> None:
        try:
            query = """
            INSERT INTO public.dim_universities (university_id, name, country, alpha_two_code, web_pages, domains, state_province, "type")
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
            ON CONFLICT (university_id) DO UPDATE SET
                name = EXCLUDED.name,
                country = EXCLUDED.country,
                alpha_two_code = EXCLUDED.alpha_two_code,
                web_pages = EXCLUDED.web_pages,
                domains = EXCLUDED.domains,
                state_province = EXCLUDED.state_province,
                "type" = EXCLUDED.type;
            """
            await connection.execute(query, university['id'], university['name'], university['country'], 
                                      university['alpha_two_code'], university['web_pages'], 
                                      university['domains'], university.get('state-province'), 
                                      university.get('type'))
            logger.info(f"Upserted university: {university['name']}")
        except Exception as e:
            logger.error(f"Error upserting university {university['name']}: {e}")

    async def run(self) -> None:
        universities = await self.extract_universities_data()
        await self.load_universities_data(universities)

    async def extract_universities_data(self) -> List[Dict[str, Any]]:
        url = "http://universities.hipolabs.com/search"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    response.raise_for_status()
                    data = await response.json()
                    logger.info("Successfully extracted universities data")
                    return data
        except Exception as e:
            logger.error(f"Error extracting universities {e}")
            return []

if __name__ == "__main__":
    loader = UniversitiesDataLoader()
    asyncio.run(loader.run())