import asyncio
import logging
from typing import List, Dict, Any
from db_connection import get_connection_pool

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UniversitiesLoader:
    def __init__(self):
        self.pool = get_connection_pool()

    async def load_universities(self, universities: List[Dict[str, Any]]) -> None:
        async with self.pool.acquire() as connection:
            async with connection.transaction():
                for university in universities:
                    await self.upsert_university(connection, university)

    async def upsert_university(self, connection, university: Dict[str, Any]) -> None:
        try:
            query = """
            INSERT INTO public.dim_universities (university_id, name, country, alpha_two_code, web_pages, domains, state_province, "type", "year_founded", "student_count")
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
            ON CONFLICT (university_id) DO UPDATE SET
                name = EXCLUDED.name,
                country = EXCLUDED.country,
                alpha_two_code = EXCLUDED.alpha_two_code,
                web_pages = EXCLUDED.web_pages,
                domains = EXCLUDED.domains,
                state_province = EXCLUDED.state_province,
                "type" = EXCLUDED."type",
                "year_founded" = EXCLUDED."year_founded",
                "student_count" = EXCLUDED."student_count";
            """
            await connection.execute(query, 
                university['id'], 
                university['name'], 
                university['country'], 
                university['alpha_two_code'], 
                university['web_pages'], 
                university['domains'], 
                university.get('state-province', None), 
                university.get('type', None), 
                university.get('year_founded', None), 
                university.get('student_count', None)
            )
            logger.info(f"Upserted university: {university['name']}")
        except Exception as e:
            logger.error(f"Error upserting university {university['name']}: {e}")