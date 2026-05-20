import logging
from typing import List, Dict, Any, Optional, Tuple

class ValidationResult:
    def __init__(self, is_valid: bool, rule_id: str, column: str, message: str, severity: str):
        self.is_valid = is_valid
        self.rule_id = rule_id
        self.column = column
        self.message = message
        self.severity = severity

class ValidationResults:
    def __init__(self, total: int, valid: int, invalid: int, failed_records: List[Dict]):
        self.total = total
        self.valid = valid
        self.invalid = invalid
        self.failed_records = failed_records

class DataValidator:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)

    async def validate_batch(self, records: List[Dict[str, Any]]) -> ValidationResults:
        total = len(records)
        valid_count = 0
        invalid_count = 0
        failed_records = []

        for record in records:
            result = self.validate_record(record)
            if result.is_valid:
                valid_count += 1
            else:
                invalid_count += 1
                failed_records.append(record)
                if result.severity == 'critical':
                    logging.error(f"Critical violation in record {record}: {result.message}")

        return ValidationResults(total, valid_count, invalid_count, failed_records)

    def validate_record(self, record: Dict[str, Any]) -> ValidationResult:
        for field in ['crypto_id', 'symbol', 'crypto_name', 'current_price', 'market_cap', 'country_code', 
                      'country_code_alpha2', 'country_name', 'region', 'population', 'university_id', 
                      'university_name', 'country', 'primary_domain', 'primary_webpage']:
            if field not in record or record[field] is None:
                return ValidationResult(False, "NULL_FIELD", field, f"{field} cannot be null", 'critical')

        market_cap_category = self._apply_rule(record)
        if market_cap_category:
            record['market_cap_category'] = market_cap_category

        volatility_flag = self._apply_rule_volatility(record)
        record['volatility_flag'] = volatility_flag

        population_density = self._apply_rule_population_density(record)
        if population_density is not None:
            record['population_density'] = population_density

        return ValidationResult(True, "", "", "", "")

    def _apply_rule(self, record: Dict[str, Any]) -> Optional[str]:
        if 'market_cap' in record:
            if record['market_cap'] > 100000000000:
                return 'Large'
            else:
                return 'Small'
        return None

    def _apply_rule_volatility(self, record: Dict[str, Any]) -> Optional[bool]:
        if 'price_change_percentage_24h' in record:
            return abs(record['price_change_percentage_24h']) > 5
        return None

    def _apply_rule_population_density(self, record: Dict[str, Any]) -> Optional[float]:
        if 'population' in record and 'area' in record and record['area'] > 0:
            return record['population'] / record['area']
        return None