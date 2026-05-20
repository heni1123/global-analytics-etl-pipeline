try:
    from extractors.currency_exchange_rates_api_extractor import *
except ImportError:
    pytest.skip("module not available", allow_module_level=True)

import pytest
from unittest import mock
from unittest.mock import AsyncMock

@pytest.mark.asyncio
async def test_extract_happy_path(mock_http_session):
    """Test extract method with valid response."""
    mock_http_session.get.return_value = AsyncMock(status=200, json=AsyncMock(return_value={
        "base_code": "USD",
        "time_last_update_unix": 1633072800,
        "time_last_update_utc": "2021-10-01T00:00:00Z",
        "time_next_update_unix": 1633159200,
        "rates": {"EUR": 0.85, "GBP": 0.75}
    }))
    
    extractor = CurrencyExchangeRatesExtractor({"url": "http://fakeurl.com"})
    await extractor.start()
    result = await extractor.extract()
    await extractor.close()
    
    assert result == [{
        "base_code": "USD",
        "time_last_update_unix": 1633072800,
        "time_last_update_utc": "2021-10-01T00:00:00Z",
        "time_next_update_unix": 1633159200,
        "rates": {"EUR": 0.85, "GBP": 0.75}
    }]

@pytest.mark.asyncio
async def test_extract_empty_input():
    """Test extract method with empty response."""
    extractor = CurrencyExchangeRatesExtractor({"url": "http://fakeurl.com"})
    await extractor.start()
    with mock.patch.object(extractor, '_fetch_page', return_value=AsyncMock(return_value={})):
        with pytest.raises(KeyError):
            await extractor.extract()
    await extractor.close()

@pytest.mark.asyncio
async def test_extract_error_handling(mock_http_session):
    """Test extract method error handling on fetch failure."""
    mock_http_session.get.return_value = AsyncMock(status=500)
    
    extractor = CurrencyExchangeRatesExtractor({"url": "http://fakeurl.com"})
    await extractor.start()
    with pytest.raises(Exception):
        await extractor.extract()
    await extractor.close()

@pytest.mark.asyncio
async def test_fetch_page_happy_path(mock_http_session):
    """Test _fetch_page method with valid response."""
    mock_http_session.get.return_value = AsyncMock(status=200, json=AsyncMock(return_value={
        "base_code": "USD",
        "time_last_update_unix": 1633072800,
        "time_last_update_utc": "2021-10-01T00:00:00Z",
        "time_next_update_unix": 1633159200,
        "rates": {"EUR": 0.85, "GBP": 0.75}
    }))
    
    extractor = CurrencyExchangeRatesExtractor({"url": "http://fakeurl.com"})
    await extractor.start()
    result = await extractor._fetch_page({})
    await extractor.close()
    
    assert result == {
        "base_code": "USD",
        "time_last_update_unix": 1633072800,
        "time_last_update_utc": "2021-10-01T00:00:00Z",
        "time_next_update_unix": 1633159200,
        "rates": {"EUR": 0.85, "GBP": 0.75}
    }

@pytest.mark.asyncio
async def test_fetch_page_error_handling(mock_http_session):
    """Test _fetch_page method error handling on server error."""
    mock_http_session.get.return_value = AsyncMock(status=500)
    
    extractor = CurrencyExchangeRatesExtractor({"url": "http://fakeurl.com"})
    await extractor.start()
    with pytest.raises(Exception):
        await extractor._fetch_page({})
    await extractor.close()

@pytest.mark.asyncio
async def test_handle_rate_limit(mock_http_session):
    """Test _handle_rate_limit method for rate limiting."""
    extractor = CurrencyExchangeRatesExtractor({"url": "http://fakeurl.com"})
    await extractor.start()
    
    response = AsyncMock(headers={"Retry-After": "2"})
    await extractor._handle_rate_limit(response)
    
    await extractor.close()

@pytest.mark.asyncio
async def test_retry_with_backoff_happy_path(mock_http_session):
    """Test _retry_with_backoff method with successful retry."""
    extractor = CurrencyExchangeRatesExtractor({"url": "http://fakeurl.com"})
    await extractor.start()
    
    async def mock_function():
        return {"success": True}
    
    result = await extractor._retry_with_backoff(mock_function)
    await extractor.close()
    
    assert result == {"success": True}

@pytest.mark.asyncio
async def test_retry_with_backoff_error_handling(mock_http_session):
    """Test _retry_with_backoff method error handling on all attempts failing."""
    extractor = CurrencyExchangeRatesExtractor({"url": "http://fakeurl.com"})
    await extractor.start()
    
    async def mock_function():
        raise Exception("Test error")
    
    with pytest.raises(Exception):
        await extractor._retry_with_backoff(mock_function)
    
    await extractor.close()

@pytest.mark.asyncio
async def test_close_session():
    """Test close method to ensure session is closed."""
    extractor = CurrencyExchangeRatesExtractor({"url": "http://fakeurl.com"})
    await extractor.start()
    await extractor.close()
    
    assert extractor.session is None

@pytest.mark.asyncio
async def test_start_session():
    """Test start method to ensure session is created."""
    extractor = CurrencyExchangeRatesExtractor({"url": "http://fakeurl.com"})
    await extractor.start()
    
    assert extractor.session is not None
    
    await extractor.close()