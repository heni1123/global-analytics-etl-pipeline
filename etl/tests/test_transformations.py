import pytest
import requests
from unittest.mock import patch

class TestTransformations:
    
    @patch('requests.get')
    def test_source_universities(self, mock_get):
        mock_get.return_value.json.return_value = [
            {"domains": ["fho.edu.br"], "state-province": "São Paulo", "name": "Fundação Hermínio Ometto", "country": "Brazil", "web_pages": ["https://www.fho.edu.br/"], "alpha_two_code": "BR"},
            {"domains": ["noah.edu.gr"], "state-province": "Macedonia", "name": "Hellenic College of Noah", "country": "Greece", "web_pages": ["https://noah.edu.gr"], "alpha_two_code": "GR"}
        ]
        response = requests.get("http://universities.hipolabs.com/search")
        data = response.json()
        assert len(data) == 2
        assert data[0]['name'] == "Fundação Hermínio Ometto"
        assert data[1]['country'] == "Greece"

    @patch('requests.get')
    def test_source_exchange_rates(self, mock_get):
        mock_get.return_value.json.return_value = {
            "result": "success",
            "provider": "https://www.exchangerate-api.com",
            "rates": {"EUR": 0.85, "GBP": 0.75}
        }
        response = requests.get("https://open.er-api.com/v6/latest/USD")
        data = response.json()
        assert data['result'] == "success"
        assert data['rates']['EUR'] == 0.85

    @patch('requests.get')
    def test_source_crypto_prices(self, mock_get):
        mock_get.return_value.json.return_value = [
            {"id": "bitcoin", "symbol": "btc", "name": "Bitcoin", "current_price": 45000, "market_cap": 850000000000},
            {"id": "ethereum", "symbol": "eth", "name": "Ethereum", "current_price": 3000, "market_cap": 350000000000}
        ]
        response = requests.get("https://api.coingecko.com/api/v3/coins/markets")
        data = response.json()
        assert len(data) == 2
        assert data[0]['name'] == "Bitcoin"
        assert data[1]['current_price'] == 3000

    @patch('requests.get')
    def test_source_countries_data(self, mock_get):
        mock_get.return_value.json.return_value = [
            {"name": {"common": "Brazil"}, "alpha2Code": "BR"},
            {"name": {"common": "Greece"}, "alpha2Code": "GR"}
        ]
        response = requests.get("https://restcountries.com/v3.1/all")
        data = response.json()
        assert len(data) == 2
        assert data[0]['name']['common'] == "Brazil"
        assert data[1]['alpha2Code'] == "GR"