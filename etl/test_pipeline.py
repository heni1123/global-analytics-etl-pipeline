import unittest
from unittest.mock import patch, AsyncMock
from crypto_extractor import CryptoExtractor
from countries_extractor import CountriesExtractor
from universities_extractor import UniversitiesExtractor
from exchange_rates_extractor import ExchangeRatesExtractor
from crypto_loader import CryptoLoader
from countries_loader import CountriesLoader
from universities_loader import UniversitiesLoader
from exchange_rates_loader import ExchangeRatesLoader
from db_connection import get_connection_pool

class TestPipeline(unittest.TestCase):

    @patch('crypto_extractor.aiohttp.ClientSession.get', new_callable=AsyncMock)
    def test_crypto_extractor(self, mock_get):
        mock_get.return_value.__aenter__.return_value.json = AsyncMock(return_value=[
            {"id": "bitcoin", "symbol": "btc", "name": "Bitcoin", "current_price": 50000, "market_cap": 1000000000, "total_volume": 20000000, "high_24h": 51000, "low_24h": 49000, "price_change_24h": 500, "price_change_percentage_24h": 1.0}
        ])
        extractor = CryptoExtractor()
        data = extractor.extract()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['id'], 'bitcoin')

    @patch('countries_extractor.aiohttp.ClientSession.get', new_callable=AsyncMock)
    def test_countries_extractor(self, mock_get):
        mock_get.return_value.__aenter__.return_value.json = AsyncMock(return_value=[
            {"name": {"common": "United States"}, "alpha2Code": "US", "alpha3Code": "USA", "population": 331000000, "area": 9833517, "region": "Americas", "subregion": "North America", "languages": {"eng": "English"}, "currencies": {"USD": {"name": "United States Dollar", "symbol": "$"}}}
        ])
        extractor = CountriesExtractor()
        data = extractor.extract()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['alpha2Code'], 'US')

    @patch('universities_extractor.aiohttp.ClientSession.get', new_callable=AsyncMock)
    def test_universities_extractor(self, mock_get):
        mock_get.return_value.__aenter__.return_value.json = AsyncMock(return_value=[
            {"name": "Harvard University", "alpha_two_code": "US", "web_pages": ["http://www.harvard.edu"], "country": "United States"}
        ])
        extractor = UniversitiesExtractor()
        data = extractor.extract()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['name'], 'Harvard University')

    @patch('exchange_rates_extractor.aiohttp.ClientSession.get', new_callable=AsyncMock)
    def test_exchange_rates_extractor(self, mock_get):
        mock_get.return_value.__aenter__.return_value.json = AsyncMock(return_value={
            "rates": {"EUR": 0.85, "GBP": 0.75},
            "base": "USD",
            "date": "2023-10-01"
        })
        extractor = ExchangeRatesExtractor()
        data = extractor.extract()
        self.assertIn('EUR', data['rates'])
        self.assertEqual(data['rates']['EUR'], 0.85)

    @patch('db_connection.get_connection_pool', return_value=AsyncMock())
    @patch('crypto_loader.CryptoLoader.load_data', new_callable=AsyncMock)
    def test_crypto_loader(self, mock_load, mock_pool):
        loader = CryptoLoader()
        data = [{"id": "bitcoin", "symbol": "btc", "current_price": 50000, "market_cap": 1000000000, "total_volume": 20000000, "high_24h": 51000, "low_24h": 49000, "price_change_24h": 500, "price_change_percentage_24h": 1.0}]
        loader.load(data)
        mock_load.assert_called_once_with(data)

    @patch('db_connection.get_connection_pool', return_value=AsyncMock())
    @patch('countries_loader.CountriesLoader.load_data', new_callable=AsyncMock)
    def test_countries_loader(self, mock_load, mock_pool):
        loader = CountriesLoader()
        data = [{"name": "United States", "alpha2Code": "US", "population": 331000000}]
        loader.load(data)
        mock_load.assert_called_once_with(data)

    @patch('db_connection.get_connection_pool', return_value=AsyncMock())
    @patch('universities_loader.UniversitiesLoader.load_data', new_callable=AsyncMock)
    def test_universities_loader(self, mock_load, mock_pool):
        loader = UniversitiesLoader()
        data = [{"name": "Harvard University", "alpha_two_code": "US", "web_pages": ["http://www.harvard.edu"]}]
        loader.load(data)
        mock_load.assert_called_once_with(data)

    @patch('db_connection.get_connection_pool', return_value=AsyncMock())
    @patch('exchange_rates_loader.ExchangeRatesLoader.load_data', new_callable=AsyncMock)
    def test_exchange_rates_loader(self, mock_load, mock_pool):
        loader = ExchangeRatesLoader()
        data = {"rates": {"EUR": 0.85, "GBP": 0.75}, "base": "USD", "date": "2023-10-01"}
        loader.load(data)
        mock_load.assert_called_once_with(data)

if __name__ == '__main__':
    unittest.main()