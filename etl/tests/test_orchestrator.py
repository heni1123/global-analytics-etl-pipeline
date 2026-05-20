try:
    from pipeline.orchestrator import *
except ImportError:
    pytest.skip("module not available", allow_module_level=True)

import pytest
from unittest import mock
from unittest.mock import AsyncMock

@pytest.mark.asyncio
async def test_run_happy_path(mock_http_session):
    """Test run method with normal valid input, expect success."""
    mock_http_session.get.side_effect = [
        AsyncMock(status=200, json=AsyncMock(return_value=[{"market_cap": 150000000000}])) for _ in range(4)
    ]
    orchestrator = PipelineOrchestrator(dry_run=False)
    await orchestrator.run()
    assert orchestrator.metrics['extract']['rows'] == 4
    assert orchestrator.metrics['load']['rows'] == 1

@pytest.mark.asyncio
async def test_run_empty_input():
    """Test run method with empty input, expect failure."""
    orchestrator = PipelineOrchestrator(dry_run=False)
    orchestrator._extract_phase = AsyncMock(return_value=[])
    with pytest.raises(ValueError, match="No records to validate"):
        await orchestrator.run()

@pytest.mark.asyncio
async def test_run_error_handling(mock_http_session):
    """Test run method error handling, expect failure."""
    mock_http_session.get.side_effect = AsyncMock(side_effect=Exception("Network error"))
    orchestrator = PipelineOrchestrator(dry_run=False)
    await orchestrator.run()
    assert orchestrator.metrics['extract']['errors'] == 1

@pytest.mark.asyncio
async def test_extract_phase_happy_path(mock_http_session):
    """Test _extract_phase method with normal valid input, expect success."""
    mock_http_session.get.side_effect = [
        AsyncMock(status=200, json=AsyncMock(return_value=[{"market_cap": 150000000000}])) for _ in range(4)
    ]
    orchestrator = PipelineOrchestrator()
    records = await orchestrator._extract_phase()
    assert len(records) == 4

@pytest.mark.asyncio
async def test_extract_phase_empty_input():
    """Test _extract_phase method with empty input, expect no records."""
    orchestrator = PipelineOrchestrator()
    orchestrator.fetch_data = AsyncMock(return_value=[])
    records = await orchestrator._extract_phase()
    assert len(records) == 0

@pytest.mark.asyncio
async def test_extract_phase_error_handling(mock_http_session):
    """Test _extract_phase method error handling, expect error count increment."""
    mock_http_session.get.side_effect = AsyncMock(side_effect=Exception("Network error"))
    orchestrator = PipelineOrchestrator()
    records = await orchestrator._extract_phase()
    assert orchestrator.metrics['extract']['errors'] == 1

def test_transform_phase_happy_path(sample_records):
    """Test _transform_phase method with normal valid input, expect transformed records."""
    orchestrator = PipelineOrchestrator()
    transformed_records = orchestrator._transform_phase(sample_records)
    assert all('market_cap_category' in record for record in transformed_records)

def test_transform_phase_empty_input():
    """Test _transform_phase method with empty input, expect empty output."""
    orchestrator = PipelineOrchestrator()
    transformed_records = orchestrator._transform_phase([])
    assert transformed_records == []

def test_transform_phase_error_handling(invalid_records):
    """Test _transform_phase method with invalid input, expect no transformation."""
    orchestrator = PipelineOrchestrator()
    transformed_records = orchestrator._transform_phase(invalid_records)
    assert len(transformed_records) == 0

def test_validate_phase_happy_path(sample_records):
    """Test _validate_phase method with valid records, expect no exception."""
    orchestrator = PipelineOrchestrator()
    orchestrator._validate_phase(sample_records)  # Should not raise

def test_validate_phase_empty_input():
    """Test _validate_phase method with empty input, expect ValueError."""
    orchestrator = PipelineOrchestrator()
    with pytest.raises(ValueError, match="No records to validate"):
        orchestrator._validate_phase([])

@pytest.mark.asyncio
async def test_load_phase_happy_path(mock_db_connection, sample_records):
    """Test _load_phase method with valid records, expect success."""
    orchestrator = PipelineOrchestrator(dry_run=False)
    orchestrator.upsert_records = AsyncMock()
    await orchestrator._load_phase(sample_records)
    assert orchestrator.metrics['load']['rows'] == len(sample_records)

@pytest.mark.asyncio
async def test_load_phase_dry_run():
    """Test _load_phase method in dry run mode, expect no load."""
    orchestrator = PipelineOrchestrator(dry_run=True)
    orchestrator.upsert_records = AsyncMock()
    await orchestrator._load_phase([])
    assert orchestrator.metrics['load']['rows'] == 0

@pytest.mark.asyncio
async def test_load_phase_error_handling(mock_db_connection, sample_records):
    """Test _load_phase method error handling, expect error count increment."""
    orchestrator = PipelineOrchestrator(dry_run=False)
    orchestrator.upsert_records = AsyncMock(side_effect=Exception("Load error"))
    await orchestrator._load_phase(sample_records)
    assert orchestrator.metrics['load']['errors'] == 1

@pytest.mark.asyncio
async def test_upsert_records_happy_path(mock_db_connection, sample_records):
    """Test upsert_records method with valid records, expect no exception."""
    orchestrator = PipelineOrchestrator()
    await orchestrator.upsert_records(sample_records)  # Should not raise

@pytest.mark.asyncio
async def test_upsert_records_error_handling(mock_db_connection, invalid_records):
    """Test upsert_records method with invalid records, expect exception."""
    orchestrator = PipelineOrchestrator()
    with pytest.raises(Exception):
        await orchestrator.upsert_records(invalid_records)

def test_audit_pipeline_run():
    """Test audit_pipeline_run method, expect logging of metrics."""
    orchestrator = PipelineOrchestrator()
    orchestrator.audit_pipeline_run(0, 1, 'success')
    assert orchestrator.metrics['extract']['rows'] == 0  # No records processed yet
    assert orchestrator.metrics['load']['rows'] == 0  # No records loaded yet