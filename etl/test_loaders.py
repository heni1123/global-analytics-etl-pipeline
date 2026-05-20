import asyncio
import pytest
from unittest.mock import AsyncMock, patch
from crypto_data_loader import CryptoDataLoader
from countries_data_loader import CountriesDataLoader
from universities_data_loader import UniversitiesDataLoader
from exchange_rates_loader import ExchangeRatesLoader
from db_connection import get_connection_pool

@pytest.fixture
async def connection_pool():
    pool = await get_connection_pool()
    yield pool
    await pool.close()

@pytest.mark.asyncio
async def test_crypto_data_loader(connection_pool):
    loader = CryptoDataLoader(connection_pool)
    mock_data = [
        {
            "id": "bitcoin",
            "symbol": "btc",
            "name": "Bitcoin",
            "current_price": 50000,
            "market_cap": 1000000000000,
            "price_change_percentage_24h": 6,
            "snapshot_date": "2023-10-01"
        }
    ]
    
    with patch('crypto_data_loader.CryptoDataLoader.fetch_data', return_value=mock_data):
        await loader.load_data()
        async with connection_pool.acquire() as conn:
            result = await conn.fetch("SELECT * FROM public.fact_crypto_markets WHERE snapshot_date = '2023-10-01'")
            assert len(result) == 1
            assert result[0]['market_cap_category'] == 'Large'
            assert result[0]['volatility_flag'] is True

@pytest.mark.asyncio
async def test_countries_data_loader(connection_pool):
    loader = CountriesDataLoader(connection_pool)
    mock_data = [
        {
            "name": "United States",
            "alpha2Code": "US",
            "alpha3Code": "USA",
            "population": 331000000,
            "area": 9833517,
            "region": "Americas",
            "subregion": "North America",
            "languages": [{"name": "English"}],
            "currencies": [{"code": "USD", "name": "United States Dollar"}],
            "flag": "https://restcountries.com/v3.1/flags/us.png"
        }
    ]
    
    with patch('countries_data_loader.CountriesDataLoader.fetch_data', return_value=mock_data):
        await loader.load_data()
        async with connection_pool.acquire() as conn:
            result = await conn.fetch("SELECT * FROM public.dim_countries WHERE country_code = 'US'")
            assert len(result) == 1
            assert result[0]['name'] == 'United States'

@pytest.mark.asyncio
async def test_universities_data_loader(connection_pool):
    loader = UniversitiesDataLoader(connection_pool)
    mock_data = [
        {
            "name": "Harvard University",
            "alpha_two_code": "US",
            "web_pages": ["http://www.harvard.edu"],
            "country": "United States",
            "university_id": "harvard"
        }
    ]
    
    with patch('universities_data_loader.UniversitiesDataLoader.fetch_data', return_value=mock_data):
        await loader.load_data()
        async with connection_pool.acquire() as conn:
            result = await conn.fetch("SELECT * FROM public.dim_universities WHERE university_id = 'harvard'")
            assert len(result) == 1
            assert result[0]['name'] == 'Harvard University'

@pytest.mark.asyncio
async def test_exchange_rates_loader(connection_pool):
    loader = ExchangeRatesLoader(connection_pool)
    mock_data = {
        "base": "USD",
        "rates": {
            "EUR": 0.85,
            "GBP": 0.75
        },
        "date": "2023-10-01"
    }
    
    with patch('exchange_rates_loader.ExchangeRatesLoader.fetch_data', return_value=mock_data):
        await loader.load_data()
        async with connection_pool.acquire() as conn:
            result = await conn.fetch("SELECT * FROM public.dim_exchange_rates WHERE base_currency = 'USD'")
            assert len(result) == 1
            assert result[0]['date'] == '2023-10-01'