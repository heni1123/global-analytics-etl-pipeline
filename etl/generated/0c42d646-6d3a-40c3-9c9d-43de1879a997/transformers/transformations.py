import logging
from typing import List, Dict, Any
import asyncio

class DataTransformer:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    async def transform_batch(self, records: List[Dict]) -> List[Dict]:
        transformed_records = []
        for record in records:
            try:
                transformed_record = self._apply_all(record)
                transformed_records.append(transformed_record)
            except ValueError as e:
                self.logger.error(f"ValueError for record {record}: {e}")
        return transformed_records

    def _apply_all(self, record: Dict) -> Dict:
        return {
            "crypto_id": record.get("id"),
            "symbol": record.get("symbol"),
            "crypto_name": record.get("name"),
            "current_price": record.get("current_price"),
            "market_cap": record.get("market_cap"),
            "market_cap_category": self._market_cap_category(record),
            "total_volume": record.get("total_volume"),
            "volume_to_mcap_ratio": self._volume_to_mcap_ratio(record),
            "price_change_24h": record.get("price_change_24h"),
            "price_change_pct_24h": record.get("price_change_percentage_24h"),
            "country_code": record.get("country_code"),
            "country_code_alpha2": record.get("country_code_alpha2"),
            "country_name": self._country_name(record),
            "official_name": self._official_name(record),
            "capital_city": self._capital_city(record),
            "region": record.get("region"),
            "subregion": record.get("subregion"),
            "population": record.get("population"),
            "population_category": record.get("population_category"),
            "area_km2": record.get("area_km2"),
            "university_id": record.get("university_id"),
            "university_name": record.get("university_name"),
            "country": record.get("country"),
            "state_province": record.get("state_province"),
            "has_state": self._has_state(record),
            "primary_domain": self._primary_domain(record),
            "primary_webpage": self._primary_webpage(record),
            "all_domains": record.get("all_domains"),
            "all_webpages": record.get("all_webpages"),
        }

    def _market_cap_category(self, record: Dict) -> Any:
        market_cap = record.get("market_cap")
        if market_cap is None:
            return None
        return 'Large' if market_cap > 100000000000 else 'Small'

    def _volatility_flag(self, record: Dict) -> Any:
        price_change_pct_24h = record.get("price_change_percentage_24h")
        if price_change_pct_24h is None:
            return None
        return abs(price_change_pct_24h) > 5

    def _volume_to_mcap_ratio(self, record: Dict) -> Any:
        total_volume = record.get("total_volume")
        market_cap = record.get("market_cap")
        if market_cap is None or market_cap == 0:
            return None
        return round(total_volume / market_cap, 4)

    def _country_name(self, record: Dict) -> Any:
        return record.get("country_name")

    def _official_name(self, record: Dict) -> Any:
        return record.get("official_name")

    def _capital_city(self, record: Dict) -> Any:
        return record.get("capital_city")

    def _population_density(self, record: Dict) -> Any:
        population = record.get("population")
        area = record.get("area_km2")
        if area is None or area == 0:
            return None
        return round(population / area, 2)

    def _primary_domain(self, record: Dict) -> Any:
        domains = record.get("domains")
        if domains:
            return domains[0]
        return None

    def _primary_webpage(self, record: Dict) -> Any:
        web_pages = record.get("web_pages")
        if web_pages:
            return web_pages[0]
        return None

    def _has_state(self, record: Dict) -> Any:
        state_province = record.get("state_province")
        return state_province is not None and state_province != ''