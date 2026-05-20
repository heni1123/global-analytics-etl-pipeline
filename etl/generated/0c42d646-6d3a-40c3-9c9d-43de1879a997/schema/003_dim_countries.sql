CREATE SCHEMA IF NOT EXISTS public;

CREATE TABLE IF NOT EXISTS public.fact_crypto_markets (
    crypto_id VARCHAR(50) NOT NULL,
    symbol VARCHAR(20) NOT NULL,
    crypto_name VARCHAR(255) NOT NULL,
    current_price DECIMAL(20,8) NOT NULL,
    market_cap BIGINT NOT NULL,
    market_cap_category VARCHAR(20),
    total_volume BIGINT,
    volume_to_mcap_ratio DECIMAL(10,4),
    price_change_24h DECIMAL(20,8),
    price_change_pct_24h DECIMAL(10,4),
    snapshot_date TIMESTAMP NOT NULL,
    PRIMARY KEY (crypto_id, snapshot_date)
);

CREATE TABLE IF NOT EXISTS public.dim_countries (
    country_code VARCHAR(3) NOT NULL,
    country_code_alpha2 VARCHAR(2) NOT NULL,
    country_name VARCHAR(255) NOT NULL,
    official_name VARCHAR(500),
    capital_city VARCHAR(255),
    region VARCHAR(100) NOT NULL,
    subregion VARCHAR(100),
    population BIGINT NOT NULL,
    population_category VARCHAR(20),
    area_km2 DECIMAL(15,2),
    PRIMARY KEY (country_code)
);

CREATE TABLE IF NOT EXISTS public.dim_universities (
    university_id SERIAL NOT NULL,
    university_name VARCHAR(500) NOT NULL,
    country VARCHAR(255) NOT NULL,
    country_code VARCHAR(2) NOT NULL,
    state_province VARCHAR(255),
    has_state BOOLEAN,
    primary_domain VARCHAR(255) NOT NULL,
    primary_webpage VARCHAR(500) NOT NULL,
    all_domains JSONB,
    all_webpages JSONB,
    PRIMARY KEY (university_id)
);

CREATE TABLE IF NOT EXISTS public.fact_regional_crypto_stats (
    region VARCHAR(100) NOT NULL,
    market_cap_category VARCHAR(20) NOT NULL,
    calculation_date TIMESTAMP NOT NULL,
    PRIMARY KEY (region, market_cap_category, calculation_date)
);

CREATE TABLE IF NOT EXISTS public.dim_exchange_rates (
    result VARCHAR(20) NOT NULL,
    provider VARCHAR(255) NOT NULL,
    documentation VARCHAR(255) NOT NULL,
    terms_of_use VARCHAR(255) NOT NULL,
    time_last_update_unix BIGINT NOT NULL,
    time_last_update_utc TIMESTAMP NOT NULL,
    time_next_update_unix BIGINT NOT NULL,
    time_next_update_utc TIMESTAMP NOT NULL,
    time_eol_unix BIGINT,
    base_code VARCHAR(10) NOT NULL,
    rates JSONB,
    PRIMARY KEY (base_code)
);