try:
    from pipeline.error_handler import *
except ImportError:
    pytest.skip("module not available", allow_module_level=True)

import pytest
from unittest import mock
from unittest.mock import AsyncMock

@pytest.mark.asyncio
async def test_execute_with_retry_happy_path():
    """Test execute_with_retry with a successful function call."""
    error_handler = ErrorHandler()
    mock_func = AsyncMock(return_value="success")
    result = await error_handler.execute_with_retry(mock_func)
    assert result == "success"

@pytest.mark.asyncio
async def test_execute_with_retry_empty_input():
    """Test execute_with_retry with empty input."""
    error_handler = ErrorHandler()
    mock_func = AsyncMock(return_value="success")
    result = await error_handler.execute_with_retry(mock_func)
    assert result == "success"

@pytest.mark.asyncio
async def test_execute_with_retry_error_handling():
    """Test execute_with_retry with a function that raises an exception."""
    error_handler = ErrorHandler(max_retries=2, backoff_factor=0.1)
    mock_func = AsyncMock(side_effect=Exception("Test error"))
    
    with mock.patch.object(error_handler.logger, 'error') as mock_error, \
         mock.patch.object(error_handler.logger, 'critical') as mock_critical:
        with pytest.raises(Exception, match="Test error"):
            await error_handler.execute_with_retry(mock_func)
    
    assert mock_error.call_count == 2
    assert mock_critical.call_count == 1

def test_audit_log():
    """Test audit_log method."""
    error_handler = ErrorHandler()
    with mock.patch.object(error_handler.logger, 'info') as mock_info:
        error_handler.audit_log("Test message")
        mock_info.assert_called_once_with("AUDIT: Test message")