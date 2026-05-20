import pytest
from unittest import mock

@pytest.fixture
def sample_records():
    """Provides a list of valid records matching the fact_crypto_markets schema."""
    return [
        {
            "crypto_id": "id_12345",
            "symbol": "example_symbol",
            "crypto_name": "Sample Name",
            "current_price": "100.00",
            "market_cap": "1000000",
            "market_cap_category": "large-cap",
            "total_volume": "50000",
            "volume_to_mcap_ratio": "0.05",
            "price_change_24h": "5.00",
            "price_change_pct_24h": "5.00",
            "country_code": "USA",
            "country_code_alpha2": "US",
            "country_name": "United States",
            "official_name": "United States of America",
            "capital_city": "Washington, D.C."
        },
        {
            "crypto_id": "id_67890",
            "symbol": "another_symbol",
            "crypto_name": "Another Name",
            "current_price": "200.00",
            "market_cap": "2000000",
            "market_cap_category": "mid-cap",
            "total_volume": "100000",
            "volume_to_mcap_ratio": "0.10",
            "price_change_24h": "10.00",
            "price_change_pct_24h": "5.00",
            "country_code": "USA",
            "country_code_alpha2": "US",
            "country_name": "United States",
            "official_name": "United States of America",
            "capital_city": "Washington, D.C."
        }
    ]

@pytest.fixture
def empty_records():
    """Provides an empty list of records."""
    return []

@pytest.fixture
def invalid_records():
    """Provides a list of records with missing/null required fields."""
    return [
        {"crypto_id": None, "symbol": "invalid_symbol"},
        {"crypto_id": "id_invalid", "symbol": None, "current_price": "invalid_price"},
        {}
    ]

@pytest.fixture
async def mock_db_connection():
    """Mocks asyncpg.Connection or sqlalchemy Engine connection."""
    with mock.patch('asyncpg.connect', create=True) as mock_connect:
        mock_conn = mock.AsyncMock()
        mock_conn.fetch.return_value = []
        mock_conn.execute.return_value = None
        mock_conn.fetchrow.return_value = None
        mock_conn.fetchval.return_value = None
        mock_connect.return_value = mock_conn
        yield mock_conn

@pytest.fixture
async def mock_http_session():
    """Mocks aiohttp.ClientSession."""
    with mock.patch('aiohttp.ClientSession', create=True) as mock_session:
        mock_session_instance = mock.AsyncMock()
        mock_session_instance.get.return_value.__aenter__.return_value = mock.AsyncMock(json=mock.AsyncMock(return_value={}))
        mock_session_instance.post.return_value.__aenter__.return_value = mock.AsyncMock(json=mock.AsyncMock(return_value={}))
        mock_session.return_value = mock_session_instance
        yield mock_session_instance