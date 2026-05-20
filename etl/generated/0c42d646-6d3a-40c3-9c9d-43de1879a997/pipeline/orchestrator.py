import asyncio
import logging
import aiohttp
import time
from typing import List, Dict, Any, Tuple

class PipelineOrchestrator:
    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self.metrics = {
            'extract': {'rows': 0, 'duration': 0, 'errors': 0},
            'transform': {'rows': 0, 'duration': 0, 'errors': 0},
            'load': {'rows': 0, 'duration': 0, 'errors': 0}
        }
        self.logger = self.setup_logging()

    def setup_logging(self) -> logging.Logger:
        logging.basicConfig(level=logging.INFO)
        return logging.getLogger(__name__)

    async def run(self) -> None:
        start_ts = time.time()
        try:
            records = await self._extract_phase()
            transformed_records = self._transform_phase(records)
            self._validate_phase(transformed_records)
            if not self.dry_run:
                await self._load_phase(transformed_records)
            status = 'success'
        except Exception as e:
            self.logger.error(f"Pipeline failed: {e}")
            status = 'failed'
        finally:
            end_ts = time.time()
            self.audit_pipeline_run(start_ts, end_ts, status)

    async def _extract_phase(self) -> List[Dict[str, Any]]:
        start_time = time.time()
        records = []
        sources = [
            "https://api.coingecko.com/api/v3/coins/markets",
            "https://restcountries.com/v3.1/all",
            "http://universities.hipolabs.com/search",
            "https://open.er-api.com/v6/latest/USD"
        ]
        async with aiohttp.ClientSession() as session:
            tasks = [self.fetch_data(session, url) for url in sources]
            results = await asyncio.gather(*tasks)
            for result in results:
                records.extend(result)
        self.metrics['extract']['duration'] = time.time() - start_time
        self.metrics['extract']['rows'] = len(records)
        return records

    async def fetch_data(self, session: aiohttp.ClientSession, url: str) -> List[Dict[str, Any]]:
        try:
            async with session.get(url) as response:
                response.raise_for_status()
                return await response.json()
        except Exception as e:
            self.logger.error(f"Error fetching data from {url}: {e}")
            self.metrics['extract']['errors'] += 1
            return []

    def _transform_phase(self, records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        start_time = time.time()
        transformed_records = []
        for record in records:
            if 'market_cap' in record:
                record['market_cap_category'] = 'Large' if record['market_cap'] > 100000000000 else 'Small'
            transformed_records.append(record)
        self.metrics['transform']['duration'] = time.time() - start_time
        self.metrics['transform']['rows'] = len(transformed_records)
        return transformed_records

    def _validate_phase(self, records: List[Dict[str, Any]]) -> None:
        if not records:
            raise ValueError("No records to validate")

    async def _load_phase(self, records: List[Dict[str, Any]]) -> None:
        start_time = time.time()
        if self.dry_run:
            self.logger.info("Dry run mode: skipping load phase.")
            return
        # Implement load strategies here
        # Example for upsert strategy
        try:
            await self.upsert_records(records)
        except Exception as e:
            self.logger.error(f"Error loading records: {e}")
            self.metrics['load']['errors'] += 1
        self.metrics['load']['duration'] = time.time() - start_time
        self.metrics['load']['rows'] = len(records)

    async def upsert_records(self, records: List[Dict[str, Any]]) -> None:
        # Implement the actual database upsert logic here
        pass

    def audit_pipeline_run(self, start_ts: float, end_ts: float, status: str) -> None:
        rows_extracted = self.metrics['extract']['rows']
        rows_loaded = self.metrics['load']['rows']
        self.logger.info(f"Pipeline run completed: start_ts={start_ts}, end_ts={end_ts}, status={status}, "
                         f"rows_extracted={rows_extracted}, rows_loaded={rows_loaded}")