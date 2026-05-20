import pytest
import requests
from unittest.mock import patch

class TestDataValidation:

    @pytest.fixture
    def sample_crypto_data(self):
        return {
            "id": "bitcoin",
            "symbol": "btc",
            "name": "Bitcoin",
            "current_price": 45000.00,
            "market_cap": 850000000000,
            "market_cap_category": "Large"
        }

    @pytest.fixture
    def sample_university_data(self):
        return {
            "domains": ["fho.edu.br"],
            "state-province": "São Paulo",
            "name": "Fundação Hermínio Ometto",
            "country": "Brazil",
            "web_pages": ["https://www.fho.edu.br/"],
            "alpha_two_code": "BR"
        }

    @pytest.fixture
    def sample_exchange_rate_data(self):
        return {
            "result": "success",
            "provider": "https://www.exchangerate-api.com",
            "documentation": "https://www.exchangerate-api.com/docs/free",
            "terms_of_use": "https://www.exchangerate-api.com/terms",
            "time_last_update_unix": 1779235351,
            "base_code": "USD",
            "rates": {
                "EUR": 0.85,
                "GBP": 0.75
            }
        }

    def test_crypto_data_validation(self, sample_crypto_data):
        assert isinstance(sample_crypto_data['id'], str)
        assert isinstance(sample_crypto_data['symbol'], str)
        assert isinstance(sample_crypto_data['name'], str)
        assert isinstance(sample_crypto_data['current_price'], (float, int))
        assert isinstance(sample_crypto_data['market_cap'], (float, int))
        assert sample_crypto_data['market_cap_category'] in ["Large", "Small"]

    def test_university_data_validation(self, sample_university_data):
        assert isinstance(sample_university_data['domains'], list)
        assert isinstance(sample_university_data['state-province'], str)
        assert isinstance(sample_university_data['name'], str)
        assert isinstance(sample_university_data['country'], str)
        assert isinstance(sample_university_data['web_pages'], list)
        assert isinstance(sample_university_data['alpha_two_code'], str)

    def test_exchange_rate_data_validation(self, sample_exchange_rate_data):
        assert sample_exchange_rate_data['result'] == "success"
        assert isinstance(sample_exchange_rate_data['provider'], str)
        assert isinstance(sample_exchange_rate_data['documentation'], str)
        assert isinstance(sample_exchange_rate_data['terms_of_use'], str)
        assert isinstance(sample_exchange_rate_data['time_last_update_unix'], int)
        assert isinstance(sample_exchange_rate_data['base_code'], str)
        assert isinstance(sample_exchange_rate_data['rates'], dict)

    @patch('requests.get')
    def test_crypto_api_response(self, mock_get, sample_crypto_data):
        mock_get.return_value.json.return_value = [sample_crypto_data]
        response = requests.get("https://api.coingecko.com/api/v3/coins/markets")
        data = response.json()
        assert len(data) > 0
        assert 'id' in data[0]
        assert 'current_price' in data[0]

    @patch('requests.get')
    def test_university_api_response(self, mock_get, sample_university_data):
        mock_get.return_value.json.return_value = [sample_university_data]
        response = requests.get("http://universities.hipolabs.com/search")
        data = response.json()
        assert len(data) > 0
        assert 'name' in data[0]
        assert 'country' in data[0]

    @patch('requests.get')
    def test_exchange_rate_api_response(self, mock_get, sample_exchange_rate_data):
        mock_get.return_value.json.return_value = sample_exchange_rate_data
        response = requests.get("https://open.er-api.com/v6/latest/USD")
        data = response.json()
        assert data['result'] == "success"
        assert 'rates' in data

    def test_market_cap_category_large(self, sample_crypto_data):
        sample_crypto_data['market_cap'] = 150000000000
        category = 'Large' if sample_crypto_data['market_cap'] > 100000000000 else 'Small'
        assert category == 'Large'

    def test_market_cap_category_small(self, sample_crypto_data):
        sample_crypto_data['market_cap'] = 50000000000
        category = 'Large' if sample_crypto_data['market_cap'] > 100000000000 else 'Small'
        assert category == 'Small'