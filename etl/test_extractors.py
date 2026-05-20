import unittest
import asyncio
from unittest.mock import patch, AsyncMock
from crypto_prices_extractor import CryptoPricesExtractor
from countries_data_extractor import CountriesDataExtractor
from universities_extractor import UniversitiesExtractor
from exchange_rates_extractor import ExchangeRatesExtractor

class TestCryptoPricesExtractor(unittest.TestCase):
    @patch('crypto_prices_extractor.aiohttp.ClientSession.get', new_callable=AsyncMock)
    def test_extract_crypto_prices(self, mock_get):
        mock_get.return_value.__aenter__.return_value.json = AsyncMock(return_value=[
            {"id": "bitcoin", "symbol": "btc", "name": "Bitcoin", "current_price": 50000, "market_cap": 1000000000000, "price_change_percentage_24h": 2.5},
            {"id": "ethereum", "symbol": "eth", "name": "Ethereum", "current_price": 4000, "market_cap": 500000000000, "price_change_percentage_24h": 6.0}
        ])
        extractor = CryptoPricesExtractor()
        result = asyncio.run(extractor.extract())
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['market_cap_category'], 'Large')
        self.assertTrue(result[1]['volatility_flag'])

class TestCountriesDataExtractor(unittest.TestCase):
    @patch('countries_data_extractor.aiohttp.ClientSession.get', new_callable=AsyncMock)
    def test_extract_countries_data(self, mock_get):
        mock_get.return_value.__aenter__.return_value.json = AsyncMock(return_value=[
            {"name": {"common": "United States"}, "alpha2Code": "US", "alpha3Code": "USA", "population": 331000000},
            {"name": {"common": "Canada"}, "alpha2Code": "CA", "alpha3Code": "CAN", "population": 37700000}
        ])
        extractor = CountriesDataExtractor()
        result = asyncio.run(extractor.extract())
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['country_code'], 'US')

class TestUniversitiesExtractor(unittest.TestCase):
    @patch('universities_extractor.aiohttp.ClientSession.get', new_callable=AsyncMock)
    def test_extract_universities(self, mock_get):
        mock_get.return_value.__aenter__.return_value.json = AsyncMock(return_value=[
            {"name": "Harvard University", "alpha_two_code": "US", "web_pages": ["http://www.harvard.edu"], "country": "United States"},
            {"name": "University of Toronto", "alpha_two_code": "CA", "web_pages": ["http://www.utoronto.ca"], "country": "Canada"}
        ])
        extractor = UniversitiesExtractor()
        result = asyncio.run(extractor.extract())
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['university_id'], 'Harvard University')

class TestExchangeRatesExtractor(unittest.TestCase):
    @patch('exchange_rates_extractor.aiohttp.ClientSession.get', new_callable=AsyncMock)
    def test_extract_exchange_rates(self, mock_get):
        mock_get.return_value.__aenter__.return_value.json = AsyncMock(return_value={
            "base": "USD",
            "rates": {"EUR": 0.85, "GBP": 0.75}
        })
        extractor = ExchangeRatesExtractor()
        result = asyncio.run(extractor.extract())
        self.assertEqual(result['base'], 'USD')
        self.assertIn('EUR', result['rates'])

if __name__ == '__main__':
    unittest.main()