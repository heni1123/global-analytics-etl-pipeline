try:
    from pipeline.ingestion import *
except ImportError:
    pytest.skip("module not available", allow_module_level=True)

import pytest
from unittest import mock
from unittest.mock import AsyncMock

@pytest.mark.asyncio
async def test_fetch_data_happy_path(mock_http_session):
    """Test fetch_data with valid URL and response."""
    url = "https://api.coingecko.com/api/v3/coins/markets"
    mock_http_session.get.return_value.__aenter__.return_value.json = AsyncMock(return_value=[{"id": "bitcoin", "current_price": 50000}])
    ingestion = DataIngestion(run_id="12345")
    result = await ingestion.fetch_data(mock_http_session, url)
    assert result == [{"id": "bitcoin", "current_price": 50000}]

@pytest.mark.asyncio
async def test_fetch_data_empty_input(mock_http_session):
    """Test fetch_data with empty response."""
    url = "https://api.coingecko.com/api/v3/coins/markets"
    mock_http_session.get.return_value.__aenter__.return_value.json = AsyncMock(return_value=[])
    ingestion = DataIngestion(run_id="12345")
    result = await ingestion.fetch_data(mock_http_session, url)
    assert result == []

@pytest.mark.asyncio
async def test_fetch_data_error_handling(mock_http_session):
    """Test fetch_data with an error during fetch."""
    url = "https://api.coingecko.com/api/v3/coins/markets"
    mock_http_session.get.side_effect = Exception("Network error")
    ingestion = DataIngestion(run_id="12345")
    result = await ingestion.fetch_data(mock_http_session, url)
    assert result == []

@pytest.mark.asyncio
async def test_gather_data_happy_path(mock_http_session):
    """Test gather_data with valid responses from all URLs."""
    mock_http_session.get.return_value.__aenter__.return_value.json = AsyncMock(side_effect=[
        [{"id": "bitcoin", "current_price": 50000}],
        [{"name": "Country1"}],
        [{"name": "University1"}],
        [{"rate": 1.0}]
    ])
    ingestion = DataIngestion(run_id="12345")
    result = await ingestion.gather_data()
    assert len(result) == 4

@pytest.mark.asyncio
async def test_gather_data_empty_input(mock_http_session):
    """Test gather_data with empty responses from all URLs."""
    mock_http_session.get.return_value.__aenter__.return_value.json = AsyncMock(return_value=[])
    ingestion = DataIngestion(run_id="12345")
    result = await ingestion.gather_data()
    assert all(len(records) == 0 for records in result.values())

@pytest.mark.asyncio
async def test_gather_data_error_handling(mock_http_session):
    """Test gather_data with an error from one of the URLs."""
    mock_http_session.get.return_value.__aenter__.return_value.json = AsyncMock(side_effect=[
        [{"id": "bitcoin", "current_price": 50000}],
        Exception("Network error"),
        [{"name": "University1"}],
        [{"rate": 1.0}]
    ])
    ingestion = DataIngestion(run_id="12345")
    result = await ingestion.gather_data()
    assert len(result) == 4
    assert isinstance(result["source_countries_data"], list)

def test_run(mock_http_session):
    """Test run method to ensure it calls gather_data and process_data."""
    ingestion = DataIngestion(run_id="12345")
    ingestion.gather_data = AsyncMock(return_value={"source_crypto_prices": [], "source_countries_data": []})
    ingestion.process_data = mock.Mock()
    ingestion.run()
    ingestion.gather_data.assert_called_once()
    ingestion.process_data.assert_called_once()

def test_process_data_happy_path(sample_records):
    """Test process_data with valid data."""
    ingestion = DataIngestion(run_id="12345")
    with mock.patch('logging.Logger.info') as mock_info:
        ingestion.process_data(sample_records)
        assert mock_info.call_count > 0

def test_process_data_empty_input(empty_records):
    """Test process_data with empty data."""
    ingestion = DataIngestion(run_id="12345")
    with mock.patch('logging.Logger.info') as mock_info:
        ingestion.process_data(empty_records)
        assert mock_info.call_count == 0

def test_process_data_error_handling(invalid_records):
    """Test process_data with invalid data."""
    ingestion = DataIngestion(run_id="12345")
    with mock.patch('logging.Logger.info') as mock_info:
        ingestion.process_data(invalid_records)
        assert mock_info.call_count > 0