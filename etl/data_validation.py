import logging
from typing import List, Dict, Any
from db_connection import get_connection

class DataValidation:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    async def validate_crypto_data(self, List[Dict[str, Any]]) -> bool:
        if not data:
            self.logger.error("No cryptocurrency data to validate.")
            return False
        
        for record in data:
            if 'id' not in record or 'current_price' not in record or 'market_cap' not in record:
                self.logger.error(f"Invalid cryptocurrency record: {record}")
                return False
            if not isinstance(record['id'], str) or not isinstance(record['current_price'], (int, float)) or not isinstance(record['market_cap'], (int, float)):
                self.logger.error(f"Invalid data types in cryptocurrency record: {record}")
                return False
        
        self.logger.info("Cryptocurrency data validation passed.")
        return True

    async def validate_countries_data(self, List[Dict[str, Any]]) -> bool:
        if not data:
            self.logger.error("No countries data to validate.")
            return False
        
        for record in data:
            if 'cca2' not in record or 'name' not in record or 'population' not in record:
                self.logger.error(f"Invalid country record: {record}")
                return False
            if not isinstance(record['cca2'], str) or not isinstance(record['name'], dict) or not isinstance(record['population'], int):
                self.logger.error(f"Invalid data types in country record: {record}")
                return False
        
        self.logger.info("Countries data validation passed.")
        return True

    async def validate_universities_data(self, List[Dict[str, Any]]) -> bool:
        if not data:
            self.logger.error("No universities data to validate.")
            return False
        
        for record in data:
            if 'id' not in record or 'name' not in record or 'country' not in record:
                self.logger.error(f"Invalid university record: {record}")
                return False
            if not isinstance(record['id'], str) or not isinstance(record['name'], str) or not isinstance(record['country'], str):
                self.logger.error(f"Invalid data types in university record: {record}")
                return False
        
        self.logger.info("Universities data validation passed.")
        return True

    async def validate_exchange_rates_data(self, Dict[str, Any]) -> bool:
        if not data or 'rates' not in data:
            self.logger.error("No exchange rates data to validate.")
            return False
        
        for currency, rate in data['rates'].items():
            if not isinstance(currency, str) or not isinstance(rate, (int, float)):
                self.logger.error(f"Invalid exchange rate record: {currency}: {rate}")
                return False
        
        self.logger.info("Exchange rates data validation passed.")
        return True

    async def validate_all_data(self, crypto_List[Dict[str, Any]], countries_List[Dict[str, Any]], universities_List[Dict[str, Any]], exchange_rates_Dict[str, Any]) -> bool:
        crypto_valid = await self.validate_crypto_data(crypto_data)
        countries_valid = await self.validate_countries_data(countries_data)
        universities_valid = await self.validate_universities_data(universities_data)
        exchange_rates_valid = await self.validate_exchange_rates_data(exchange_rates_data)

        return crypto_valid and countries_valid and universities_valid and exchange_rates_valid