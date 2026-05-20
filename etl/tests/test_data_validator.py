try:
    from validators.data_validator import *
except ImportError:
    pytest.skip("module not available", allow_module_level=True)

import pytest
from unittest import mock

@pytest.mark.asyncio
async def test_validate_batch_happy_path(sample_records):
    """Test validate_batch with valid records."""
    validator = DataValidator()
    result = await validator.validate_batch(sample_records)
    assert result.total == len(sample_records)
    assert result.valid == len(sample_records)
    assert result.invalid == 0
    assert result.failed_records == []

@pytest.mark.asyncio
async def test_validate_batch_empty_input(empty_records):
    """Test validate_batch with empty input."""
    validator = DataValidator()
    result = await validator.validate_batch(empty_records)
    assert result.total == 0
    assert result.valid == 0
    assert result.invalid == 0
    assert result.failed_records == []

@pytest.mark.asyncio
async def test_validate_batch_error_handling(invalid_records):
    """Test validate_batch with invalid records."""
    validator = DataValidator()
    result = await validator.validate_batch(invalid_records)
    assert result.total == len(invalid_records)
    assert result.valid == 0
    assert result.invalid == len(invalid_records)
    assert len(result.failed_records) == len(invalid_records)

def test_validate_record_happy_path(sample_records):
    """Test validate_record with valid record."""
    validator = DataValidator()
    result = validator.validate_record(sample_records[0])
    assert result.is_valid
    assert result.rule_id == ""
    assert result.message == ""

def test_validate_record_empty_input():
    """Test validate_record with empty input."""
    validator = DataValidator()
    result = validator.validate_record({})
    assert not result.is_valid
    assert result.rule_id == "NULL_FIELD"
    assert result.message == "crypto_id cannot be null"

def test_validate_record_error_handling(invalid_records):
    """Test validate_record with invalid record."""
    validator = DataValidator()
    for record in invalid_records:
        result = validator.validate_record(record)
        assert not result.is_valid
        assert result.rule_id == "NULL_FIELD"

def test_apply_rule_happy_path():
    """Test _apply_rule with valid market cap."""
    validator = DataValidator()
    record = {'market_cap': 150000000000}
    result = validator._apply_rule(record)
    assert result == 'Large'

def test_apply_rule_empty_input():
    """Test _apply_rule with no market cap."""
    validator = DataValidator()
    record = {}
    result = validator._apply_rule(record)
    assert result is None

def test_apply_rule_error_handling():
    """Test _apply_rule with invalid market cap."""
    validator = DataValidator()
    record = {'market_cap': 50000000}
    result = validator._apply_rule(record)
    assert result == 'Small'

def test_apply_rule_volatility_happy_path():
    """Test _apply_rule_volatility with valid price change."""
    validator = DataValidator()
    record = {'price_change_percentage_24h': 6}
    result = validator._apply_rule_volatility(record)
    assert result is True

def test_apply_rule_volatility_empty_input():
    """Test _apply_rule_volatility with no price change."""
    validator = DataValidator()
    record = {}
    result = validator._apply_rule_volatility(record)
    assert result is None

def test_apply_rule_volatility_error_handling():
    """Test _apply_rule_volatility with negative price change."""
    validator = DataValidator()
    record = {'price_change_percentage_24h': 3}
    result = validator._apply_rule_volatility(record)
    assert result is False

def test_apply_rule_population_density_happy_path():
    """Test _apply_rule_population_density with valid population and area."""
    validator = DataValidator()
    record = {'population': 1000, 'area': 100}
    result = validator._apply_rule_population_density(record)
    assert result == 10.0

def test_apply_rule_population_density_empty_input():
    """Test _apply_rule_population_density with missing fields."""
    validator = DataValidator()
    record = {'population': 1000}
    result = validator._apply_rule_population_density(record)
    assert result is None

def test_apply_rule_population_density_error_handling():
    """Test _apply_rule_population_density with zero area."""
    validator = DataValidator()
    record = {'population': 1000, 'area': 0}
    result = validator._apply_rule_population_density(record)
    assert result is None