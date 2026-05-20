# Global Data Analytics Pipeline

## Overview
The Global Data Analytics Pipeline is designed to aggregate and analyze data from various sources, including cryptocurrency prices, country information, university data, and exchange rates. This pipeline facilitates the transformation of raw data into structured formats suitable for analysis and reporting.

## Architecture
The architecture of the pipeline consists of multiple components that interact with various REST APIs to fetch data, transform it, and load it into a PostgreSQL database. The ETL process is designed to be efficient and scalable, allowing for on-demand execution.

## Data Sources
- **source_crypto_prices**: Cryptocurrency Market Data from [CoinGecko](https://api.coingecko.com/api/v3/coins/markets)
- **source_countries_data**: World Countries Information from [RestCountries](https://restcountries.com/v3.1/all)
- **source_universities**: World Universities Database from [Hipolabs](http://universities.hipolabs.com/search)
- **source_exchange_rates**: Currency Exchange Rates from [ExchangeRate API](https://open.er-api.com/v6/latest/USD)

## Target Tables
- **fact_crypto_markets**: Stores aggregated cryptocurrency market data.
- **dim_countries**: Contains information about countries.
- **dim_universities**: Holds data about universities worldwide.
- **fact_regional_crypto_stats**: Provides regional statistics on cryptocurrency markets.

## Installation
1. Clone the repository:
   ```
   git clone https://github.com/heni1123/global-analytics-etl-pipeline.git
   ```
2. Navigate to the project directory:
   ```
   cd global-analytics-etl-pipeline
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Configuration
1. Set up your environment variables:
   ```
   export GITHUB_TOKEN=your_github_token
   ```
2. Configure the database connection settings in the `config.py` file.

## Running
To execute the ETL pipeline, run the following command:
```
python main.py
```
This will trigger the on-demand data extraction, transformation, and loading process.

## Testing
To run the tests, use the following command:
```
pytest tests/
```
Ensure that all tests pass before deploying the pipeline to production.

## Troubleshooting
- **Common Issues**:
  - If the API fails to respond, check your internet connection and the API status.
  - Ensure that the database is running and accessible.
  - Review the logs for any error messages that can provide insight into the failure.

- **Log Files**: Check the `logs/` directory for detailed logs of the ETL process, which can help identify issues during execution.