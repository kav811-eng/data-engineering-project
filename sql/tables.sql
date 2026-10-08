CREATE SCHEMA IF NOT EXISTS energy_market;

CREATE TABLE IF NOT EXISTS energy_market.consumption_hourly (
    timestamp TIMESTAMPTZ PRIMARY KEY,
    consumption DOUBLE PRECISION,
    date DATE,
    year INTEGER,
    month INTEGER,
    day INTEGER,
    hour INTEGER,
    day_of_week INTEGER,
    is_weekend BOOLEAN
);

CREATE TABLE IF NOT EXISTS energy_market.solar_hourly (
    timestamp TIMESTAMPTZ PRIMARY KEY,
    solar_generation DOUBLE PRECISION,
    date DATE,
    year INTEGER,
    month INTEGER,
    day INTEGER,
    hour INTEGER,
    day_of_week INTEGER,
    is_weekend BOOLEAN
);

CREATE TABLE IF NOT EXISTS energy_market.wind_offshore_hourly (
    timestamp TIMESTAMPTZ PRIMARY KEY,
    wind_offshore DOUBLE PRECISION,
    date DATE,
    year INTEGER,
    month INTEGER,
    day INTEGER,
    hour INTEGER,
    day_of_week INTEGER,
    is_weekend BOOLEAN
);

CREATE TABLE IF NOT EXISTS energy_market.wind_onshore_hourly (
    timestamp TIMESTAMPTZ PRIMARY KEY,
    wind_onshore DOUBLE PRECISION,
    date DATE,
    year INTEGER,
    month INTEGER,
    day INTEGER,
    hour INTEGER,
    day_of_week INTEGER,
    is_weekend BOOLEAN
);

CREATE TABLE IF NOT EXISTS energy_market.price_hourly (
    timestamp TIMESTAMPTZ PRIMARY KEY,
    price DOUBLE PRECISION,
    date DATE,
    year INTEGER,
    month INTEGER,
    day INTEGER,
    hour INTEGER,
    day_of_week INTEGER,
    is_weekend BOOLEAN
);

CREATE TABLE IF NOT EXISTS energy_market.residual_load_hourly (
    timestamp TIMESTAMPTZ PRIMARY KEY,
    residual_load DOUBLE PRECISION,
    date DATE,
    year INTEGER,
    month INTEGER,
    day INTEGER,
    hour INTEGER,
    day_of_week INTEGER,
    is_weekend BOOLEAN
);

-- Add total generation as a stored calculated column
ALTER TABLE energy_market.bi_energy_market
ADD COLUMN IF NOT EXISTS total_generation DOUBLE PRECISION
GENERATED ALWAYS AS (
    COALESCE(solar_generation, 0)
    + COALESCE(wind_onshore, 0)
    + COALESCE(wind_offshore, 0)
) STORED;


-- Add pipeline refresh timestamp
ALTER TABLE energy_market.bi_energy_market
ADD COLUMN IF NOT EXISTS last_refresh_at TIMESTAMPTZ;


- ============================================================
-- FINAL BI TABLE
-- One row per timestamp
-- ============================================================

DO $$
DECLARE
    object_type CHAR;
BEGIN
    SELECT c.relkind
    INTO object_type
    FROM pg_class c
    JOIN pg_namespace n
        ON n.oid = c.relnamespace
    WHERE n.nspname = 'energy_market'
      AND c.relname = 'bi_energy_market';

    IF object_type = 'v' THEN
        EXECUTE 'DROP VIEW energy_market.bi_energy_market CASCADE';
    END IF;
END $$;


CREATE TABLE IF NOT EXISTS energy_market.bi_energy_market (
    timestamp TIMESTAMPTZ PRIMARY KEY,
    date DATE,
    year INTEGER,
    month INTEGER,
    day INTEGER,
    hour INTEGER,
    day_of_week INTEGER,
    is_weekend BOOLEAN,

    consumption DOUBLE PRECISION,
    solar_generation DOUBLE PRECISION,
    wind_onshore DOUBLE PRECISION,
    wind_offshore DOUBLE PRECISION,
    price DOUBLE PRECISION,
    residual_load DOUBLE PRECISION,

    total_generation DOUBLE PRECISION
        GENERATED ALWAYS AS (
            COALESCE(solar_generation, 0)
            + COALESCE(wind_onshore, 0)
            + COALESCE(wind_offshore, 0)
        ) STORED,

    last_refresh_at TIMESTAMPTZ NOT NULL
);

-- ============================================================
-- INITIAL LOAD INTO BI TABLE
-- ============================================================

TRUNCATE TABLE energy_market.bi_energy_market;

INSERT INTO energy_market.bi_energy_market (
    timestamp,
    date,
    year,
    month,
    day,
    hour,
    day_of_week,
    is_weekend,
    consumption,
    solar_generation,
    wind_onshore,
    wind_offshore,
    price,
    residual_load,
    last_refresh_at
)
SELECT
    timestamp,
    date,
    year,
    month,
    day,
    hour,
    day_of_week,
    is_weekend,
    consumption,
    solar_generation,
    wind_onshore,
    wind_offshore,
    price,
    residual_load,
    CURRENT_TIMESTAMP
FROM energy_market.energy_market_hourly
ORDER BY timestamp;


