CREATE SCHEMA IF NOT EXISTS energy_market;


-- ============================================================
-- HOURLY COMBINED MARKET VIEW
-- ============================================================

CREATE OR REPLACE VIEW energy_market.energy_market_hourly AS
SELECT
    c.timestamp,
    c.consumption,
    s.solar_generation,
    wo.wind_offshore,
    wi.wind_onshore,
    p.price,
    r.residual_load,
    c.date,
    c.year,
    c.month,
    c.day,
    c.hour,
    c.day_of_week,
    c.is_weekend
FROM energy_market.consumption_hourly c
LEFT JOIN energy_market.solar_hourly s
    ON c.timestamp = s.timestamp
LEFT JOIN energy_market.wind_offshore_hourly wo
    ON c.timestamp = wo.timestamp
LEFT JOIN energy_market.wind_onshore_hourly wi
    ON c.timestamp = wi.timestamp
LEFT JOIN energy_market.price_hourly p
    ON c.timestamp = p.timestamp
LEFT JOIN energy_market.residual_load_hourly r
    ON c.timestamp = r.timestamp;


-- ============================================================
-- DAILY CONSUMPTION
-- ============================================================

CREATE OR REPLACE VIEW energy_market.daily_consumption AS
SELECT
    date,
    SUM(consumption) AS total_consumption,
    AVG(consumption) AS average_hourly_consumption,
    MIN(consumption) AS minimum_hourly_consumption,
    MAX(consumption) AS maximum_hourly_consumption
FROM energy_market.consumption_hourly
GROUP BY date
ORDER BY date;


-- ============================================================
-- MONTHLY CONSUMPTION
-- ============================================================

CREATE OR REPLACE VIEW energy_market.monthly_consumption AS
SELECT
    year,
    month,
    SUM(consumption) AS total_consumption,
    AVG(consumption) AS average_hourly_consumption,
    MIN(consumption) AS minimum_hourly_consumption,
    MAX(consumption) AS maximum_hourly_consumption
FROM energy_market.consumption_hourly
GROUP BY year, month
ORDER BY year, month;


-- ============================================================
-- WEEKDAY CONSUMPTION
-- ============================================================

CREATE OR REPLACE VIEW energy_market.weekday_consumption AS
SELECT
    day_of_week,
    is_weekend,
    AVG(consumption) AS average_consumption,
    MIN(consumption) AS minimum_consumption,
    MAX(consumption) AS maximum_consumption
FROM energy_market.consumption_hourly
GROUP BY day_of_week, is_weekend
ORDER BY day_of_week;


-- ============================================================
-- RENEWABLE GENERATION VIEW
-- Three generation types:
-- solar
-- onshore
-- offshore
--
-- One row per timestamp per generation type
-- ============================================================

CREATE OR REPLACE VIEW energy_market.bi_generation AS

SELECT
    timestamp,
    date,
    year,
    month,
    day,
    hour,
    day_of_week,
    is_weekend,
    'solar' AS generation_type,
    solar_generation AS generation,
    last_refresh_at
FROM energy_market.bi_energy_market

UNION ALL

SELECT
    timestamp,
    date,
    year,
    month,
    day,
    hour,
    day_of_week,
    is_weekend,
    'onshore' AS generation_type,
    wind_onshore AS generation,
    last_refresh_at
FROM energy_market.bi_energy_market

UNION ALL

SELECT
    timestamp,
    date,
    year,
    month,
    day,
    hour,
    day_of_week,
    is_weekend,
    'offshore' AS generation_type,
    wind_offshore AS generation,
    last_refresh_at
FROM energy_market.bi_energy_market;

-- Create generation view
CREATE OR REPLACE VIEW energy_market.bi_generation AS

SELECT
    timestamp,
    date,
    year,
    month,
    day,
    hour,
    day_of_week,
    is_weekend,
    'solar' AS generation_type,
    solar_generation AS generation,
    last_refresh_at
FROM energy_market.bi_energy_market

UNION ALL

SELECT
    timestamp,
    date,
    year,
    month,
    day,
    hour,
    day_of_week,
    is_weekend,
    'onshore' AS generation_type,
    wind_onshore AS generation,
    last_refresh_at
FROM energy_market.bi_energy_market

UNION ALL

SELECT
    timestamp,
    date,
    year,
    month,
    day,
    hour,
    day_of_week,
    is_weekend,
    'offshore' AS generation_type,
    wind_offshore AS generation,
    last_refresh_at
FROM energy_market.bi_energy_market;