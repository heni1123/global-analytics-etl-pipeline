try:
    from extractors.cryptocurrency_market_data_api_extractor import *
except ImportError:
    pytest.skip("module not available", allow_module_level=True)

import pytest
from unittest import mock
from unittest.mock import AsyncMock

@pytest.mark.asyncio
async def test_extract_happy_path(mock_http_session, sample_records):
    """Test extract method with valid input, expect success."""
    mock_http_session.get.return_value = AsyncMock(status=200, json=AsyncMock(return_value=sample_records))
    extractor = CryptocurrencyMarketDataExtractor({"url": "http://fakeurl.com"})
    result = await extractor.extract()
    assert result == sample_records

@pytest.mark.asyncio
async def test_extract_empty_input(mock_http_session):
    """Test extract method with empty input, expect success."""
    mock_http_session.get.return_value = AsyncMock(status=200, json=AsyncMock(return_value=[]))
    extractor = CryptocurrencyMarketDataExtractor({"url": "http://fakeurl.com"})
    result = await extractor.extract()
    assert result == []

@pytest.mark.asyncio
async def test_extract_error_handling(mock_http_session):
    """Test extract method error handling with an exception."""
    mock_http_session.get.side_effect = Exception("Network error")
    extractor = CryptocurrencyMarketDataExtractor({"url": "http://fakeurl.com"})
    with pytest.raises(Exception, match="Extraction failed: Network error"):
        await extractor.extract()

@pytest.mark.asyncio
async def test_fetch_page_happy_path(mock_http_session, sample_records):
    """Test _fetch_page method with valid input, expect success."""
    mock_http_session.get.return_value = AsyncMock(status=200, json=AsyncMock(return_value=sample_records))
    extractor = CryptocurrencyMarketDataExtractor({"url": "http://fakeurl.com"})
    result = await extractor._fetch_page({})
    assert result == sample_records

@pytest.mark.asyncio
async def test_fetch_page_empty_input(mock_http_session):
    """Test _fetch_page method with empty input, expect success."""
    mock_http_session.get.return_value = AsyncMock(status=200, json=AsyncMock(return_value=[]))
    extractor = CryptocurrencyMarketDataExtractor({"url": "http://fakeurl.com"})
    result = await extractor._fetch_page({})
    assert result == []

@pytest.mark.asyncio
async def test_fetch_page_error_handling(mock_http_session):
    """Test _fetch_page method error handling with a 500 status code."""
    mock_http_session.get.return_value = AsyncMock(status=500)
    extractor = CryptocurrencyMarketDataExtractor({"url": "http://fakeurl.com"})
    with pytest.raises(Exception, match="HTTP Error: 500"):
        await extractor._fetch_page({})

@pytest.mark.asyncio
async def test_handle_rate_limit(mock_http_session):
    """Test _handle_rate_limit method with a rate limit response."""
    extractor = CryptocurrencyMarketDataExtractor({"url": "http://fakeurl.com"})
    mock_response = AsyncMock(headers={"Retry-After": "1"})
    with mock.patch('asyncio.sleep', return_value=None) as mock_sleep:
        await extractor._handle_rate_limit(mock_response)
        mock_sleep.assert_called_once_with(1)

@pytest.mark.asyncio
async def test_retry_with_backoff_happy_path(mock_http_session, sample_records):
    """Test _retry_with_backoff method with successful retry."""
    extractor = CryptocurrencyMarketDataExtractor({"url": "http://fakeurl.com"})
    mock_http_session.get.side_effect = [Exception("Network error"), AsyncMock(status=200, json=AsyncMock(return_value=sample_records))]
    result = await extractor._retry_with_backoff(extractor._fetch_page, {})
    assert result == sample_records

@pytest.mark.asyncio
async def test_retry_with_backoff_error_handling(mock_http_session):
    """Test _retry_with_backoff method error handling after retries."""
    extractor = CryptocurrencyMarketDataExtractor({"url": "http://fakeurl.com"})
    mock_http_session.get.side_effect = Exception("Network error")
    with pytest.raises(Exception, match="All attempts failed: Network error"):
        await extractor._retry_with_backoff(extractor._fetch_page, {})

@pytest.mark.asyncio
async def test_close_happy_path(mock_http_session):
    """Test close method to ensure session is closed."""
    extractor = CryptocurrencyMarketDataExtractor({"url": "http://fakeurl.com"})
    extractor.session = mock_http_session
    await extractor.close()
    mock_http_session.close.assert_called_once()