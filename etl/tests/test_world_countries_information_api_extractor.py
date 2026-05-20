try:
    from extractors.world_countries_information_api_extractor import *
except ImportError:
    pytest.skip("module not available", allow_module_level=True)

import pytest
from unittest import mock
from unittest.mock import AsyncMock

@pytest.mark.asyncio
async def test_extract_happy_path(mock_http_session):
    """Test extract method with valid input, expect success."""
    mock_http_session.get.return_value = AsyncMock(status=200, json=AsyncMock(return_value=[{"name": "Country1"}, {"name": "Country2"}]))
    extractor = WorldCountriesInformationExtractor({"url": "http://example.com"})
    result = await extractor.extract()
    assert result == [{"name": "Country1"}, {"name": "Country2"}]

@pytest.mark.asyncio
async def test_extract_empty_input():
    """Test extract method with empty input, expect success."""
    extractor = WorldCountriesInformationExtractor({"url": "http://example.com"})
    result = await extractor.extract()
    assert result == []

@pytest.mark.asyncio
async def test_extract_error_handling(mock_http_session):
    """Test extract method error handling on exception."""
    mock_http_session.get.side_effect = Exception("Network error")
    extractor = WorldCountriesInformationExtractor({"url": "http://example.com"})
    with pytest.raises(Exception, match="Network error"):
        await extractor.extract()

@pytest.mark.asyncio
async def test_fetch_page_happy_path(mock_http_session):
    """Test _fetch_page method with valid input, expect success."""
    mock_http_session.get.return_value = AsyncMock(status=200, json=AsyncMock(return_value=[{"name": "Country1"}]))
    extractor = WorldCountriesInformationExtractor({"url": "http://example.com"})
    result = await extractor._fetch_page({})
    assert result == [{"name": "Country1"}]

@pytest.mark.asyncio
async def test_fetch_page_empty_input():
    """Test _fetch_page method with empty input, expect success."""
    extractor = WorldCountriesInformationExtractor({"url": "http://example.com"})
    result = await extractor._fetch_page({})
    assert result == []

@pytest.mark.asyncio
async def test_fetch_page_error_handling(mock_http_session):
    """Test _fetch_page method error handling on exception."""
    mock_http_session.get.side_effect = Exception("Fetch error")
    extractor = WorldCountriesInformationExtractor({"url": "http://example.com"})
    with pytest.raises(Exception, match="Fetch error"):
        await extractor._fetch_page({})

@pytest.mark.asyncio
async def test_make_request_happy_path(mock_http_session):
    """Test _make_request method with valid input, expect success."""
    mock_http_session.get.return_value = AsyncMock(status=200, json=AsyncMock(return_value=[{"name": "Country1"}]))
    extractor = WorldCountriesInformationExtractor({"url": "http://example.com"})
    result = await extractor._make_request("http://example.com", {})
    assert result == [{"name": "Country1"}]

@pytest.mark.asyncio
async def test_make_request_rate_limit_handling(mock_http_session):
    """Test _make_request method handling rate limit response."""
    mock_http_session.get.return_value = AsyncMock(status=429, headers={"Retry-After": "1"})
    extractor = WorldCountriesInformationExtractor({"url": "http://example.com"})
    with pytest.raises(Exception, match="Max retries exceeded"):
        await extractor._make_request("http://example.com", {})

@pytest.mark.asyncio
async def test_make_request_server_error_handling(mock_http_session):
    """Test _make_request method handling server error response."""
    mock_http_session.get.return_value = AsyncMock(status=500)
    extractor = WorldCountriesInformationExtractor({"url": "http://example.com"})
    with pytest.raises(Exception, match="Server error: 500"):
        await extractor._make_request("http://example.com", {})

@pytest.mark.asyncio
async def test_handle_rate_limit_happy_path(mock_http_session):
    """Test _handle_rate_limit method with valid response."""
    extractor = WorldCountriesInformationExtractor({"url": "http://example.com"})
    response = AsyncMock(headers={"Retry-After": "1"})
    await extractor._handle_rate_limit(response)

@pytest.mark.asyncio
async def test_retry_with_backoff_happy_path(mock_http_session):
    """Test _retry_with_backoff method with successful retry."""
    async def successful_request():
        return [{"name": "Country1"}]

    extractor = WorldCountriesInformationExtractor({"url": "http://example.com"})
    result = await extractor._retry_with_backoff(successful_request)
    assert result == [{"name": "Country1"}]

@pytest.mark.asyncio
async def test_retry_with_backoff_error_handling(mock_http_session):
    """Test _retry_with_backoff method handling retries on failure."""
    async def failing_request():
        raise Exception("Request failed")

    extractor = WorldCountriesInformationExtractor({"url": "http://example.com"})
    with pytest.raises(Exception, match="Max retries exceeded"):
        await extractor._retry_with_backoff(failing_request)

@pytest.mark.asyncio
async def test_close_happy_path():
    """Test close method to ensure session is closed."""
    extractor = WorldCountriesInformationExtractor({"url": "http://example.com"})
    extractor.session = AsyncMock()
    await extractor.close()
    extractor.session.close.assert_called_once()

@pytest.mark.asyncio
async def test_start_happy_path(mock_http_session):
    """Test start method to ensure extraction is initiated."""
    mock_http_session.get.return_value = AsyncMock(status=200, json=AsyncMock(return_value=[{"name": "Country1"}]))
    extractor = WorldCountriesInformationExtractor({"url": "http://example.com"})
    await extractor.start()  # Should not raise an exception

@pytest.mark.asyncio
async def test_start_error_handling(mock_http_session):
    """Test start method error handling on extraction failure."""
    mock_http_session.get.side_effect = Exception("Network error")
    extractor = WorldCountriesInformationExtractor({"url": "http://example.com"})
    with pytest.raises(Exception, match="Network error"):
        await extractor.start()