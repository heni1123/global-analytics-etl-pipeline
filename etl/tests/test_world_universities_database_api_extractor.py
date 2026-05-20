try:
    from extractors.world_universities_database_api_extractor import *
except ImportError:
    pytest.skip("module not available", allow_module_level=True)

import pytest
from unittest import mock
from unittest.mock import AsyncMock

@pytest.mark.asyncio
async def test_extract_happy_path(mock_http_session):
    """Test extract method with valid input, expect success."""
    mock_http_session.get.return_value = AsyncMock(status=200, json=AsyncMock(return_value=[{"name": "University A"}]))
    extractor = WorldUniversitiesDatabaseExtractor({"url": "http://example.com"})
    result = await extractor.extract()
    assert result == [{"name": "University A"}]

@pytest.mark.asyncio
async def test_extract_empty_input():
    """Test extract method with empty input, expect success."""
    extractor = WorldUniversitiesDatabaseExtractor({"url": "http://example.com"})
    with mock.patch.object(extractor, '_fetch_page', return_value=AsyncMock(return_value=[])):
        result = await extractor.extract()
        assert result == []

@pytest.mark.asyncio
async def test_extract_error_handling(mock_http_session):
    """Test extract method error handling with exception."""
    mock_http_session.get.side_effect = Exception("Network error")
    extractor = WorldUniversitiesDatabaseExtractor({"url": "http://example.com"})
    with pytest.raises(Exception, match="Network error"):
        await extractor.extract()

@pytest.mark.asyncio
async def test_fetch_page_happy_path(mock_http_session):
    """Test _fetch_page method with valid parameters, expect success."""
    mock_http_session.get.return_value = AsyncMock(status=200, json=AsyncMock(return_value=[{"name": "University B"}]))
    extractor = WorldUniversitiesDatabaseExtractor({"url": "http://example.com"})
    result = await extractor._fetch_page({})
    assert result == [{"name": "University B"}]

@pytest.mark.asyncio
async def test_fetch_page_empty_input():
    """Test _fetch_page method with empty parameters, expect success."""
    extractor = WorldUniversitiesDatabaseExtractor({"url": "http://example.com"})
    with mock.patch.object(extractor, '_retry_with_backoff', return_value=AsyncMock(status=200, json=AsyncMock(return_value=[]))):
        result = await extractor._fetch_page({})
        assert result == []

@pytest.mark.asyncio
async def test_fetch_page_error_handling(mock_http_session):
    """Test _fetch_page method error handling with HTTP error."""
    mock_http_session.get.return_value = AsyncMock(status=500)
    extractor = WorldUniversitiesDatabaseExtractor({"url": "http://example.com"})
    with pytest.raises(Exception, match="HTTP Error: 500"):
        await extractor._fetch_page({})

@pytest.mark.asyncio
async def test_handle_rate_limit(mock_http_session):
    """Test _handle_rate_limit method, expect sleep on rate limit."""
    extractor = WorldUniversitiesDatabaseExtractor({"url": "http://example.com"})
    with mock.patch('asyncio.sleep', return_value=None) as mock_sleep:
        await extractor._handle_rate_limit(AsyncMock())
        mock_sleep.assert_called_once_with(5)

@pytest.mark.asyncio
async def test_retry_with_backoff_happy_path(mock_http_session):
    """Test _retry_with_backoff method with successful retry."""
    mock_http_session.get.side_effect = [AsyncMock(status=500), AsyncMock(status=200, json=AsyncMock(return_value=[{"name": "University C"}]))]
    extractor = WorldUniversitiesDatabaseExtractor({"url": "http://example.com"})
    result = await extractor._retry_with_backoff(mock_http_session.get, "http://example.com")
    assert result.status == 200

@pytest.mark.asyncio
async def test_retry_with_backoff_max_retries(mock_http_session):
    """Test _retry_with_backoff method exceeding max retries."""
    mock_http_session.get.side_effect = Exception("Network error")
    extractor = WorldUniversitiesDatabaseExtractor({"url": "http://example.com"})
    with pytest.raises(Exception, match="Max retries exceeded."):
        await extractor._retry_with_backoff(mock_http_session.get, "http://example.com")

@pytest.mark.asyncio
async def test_close_happy_path():
    """Test close method to ensure session is closed."""
    extractor = WorldUniversitiesDatabaseExtractor({"url": "http://example.com"})
    extractor.session = AsyncMock()
    await extractor.close()
    extractor.session.close.assert_awaited_once()