# Germany Energy Analytics

### Electricity Prices, Demand & Renewable Generation Analytics

An end-to-end data analytics and engineering project analyzing Germany's electricity market using public data from [SMARD](https://www.smard.de/home/marktdaten).

The project builds a reproducible data pipeline that ingests electricity-market data, cleans and validates the datasets, stores the analytical data in PostgreSQL, synchronizes a BI dataset to Aiven PostgreSQL, and presents the results through an interactive Looker Studio dashboard.

---

## Project Overview

Germany's electricity market is increasingly influenced by renewable energy generation, electricity demand, and the amount of electricity that must be supplied by conventional or other sources.

This project investigates the relationship between:

* Electricity demand
* Solar generation
* Onshore wind generation
* Offshore wind generation
* Residual load
* Day-ahead electricity prices

The project combines data engineering, SQL analytics, cloud database deployment, and business intelligence into one end-to-end workflow.

---

## Business Question

> **How do renewable generation, electricity demand, and residual load influence electricity prices in Germany?**

The analysis focuses on identifying patterns between renewable electricity availability, system demand, residual load, and electricity prices across different time periods.

---

## Objectives

The project was designed to:

1. Ingest public German electricity-market data from SMARD.
2. Build a repeatable Python data pipeline.
3. Clean and transform the raw datasets.
4. Validate data quality before analysis.
5. Store structured hourly data in PostgreSQL.
6. Create analytical SQL models for BI reporting.
7. Synchronize the BI dataset to Aiven PostgreSQL.
8. Build an interactive Looker Studio dashboard.
9. Analyze electricity prices, demand, renewable generation, and residual load.
10. Create a foundation for future predictive analytics and machine-learning extensions.

---

## Architecture

```text
                         SMARD
                           │
                           ▼
                 Python API Ingestion
                           │
                           ▼
                    Data Cleaning
                           │
                           ▼
                     Validation
                           │
                           ▼
                 Local PostgreSQL
                           │
                           ▼
                  SQL Analytical Models
                           │
                           ▼
                  Aiven PostgreSQL
                           │
                           ▼
                    Looker Studio
                           │
                           ▼
                 Interactive Dashboard
```

### Data Flow

```text
SMARD Public Data
       ↓
Python ingestion scripts
       ↓
Raw Parquet files
       ↓
Cleaning / transformation
       ↓
Processed Parquet files
       ↓
PostgreSQL
       ↓
BI analytical dataset
       ↓
Aiven PostgreSQL
       ↓
Looker Studio
```

---

## Data Source

The primary data source is **SMARD**, the German Federal Network Agency's electricity-market data platform.

SMARD provides publicly available electricity-market information including generation, consumption, residual load, and electricity prices.

### Source

* SMARD Market Data: https://www.smard.de/home/marktdaten
* SMARD Download Center: https://www.smard.de/home/downloadcenter

The project uses the SMARD API/data download functionality to retrieve the required datasets programmatically.

---

## Datasets

The project currently works with the following hourly datasets:

| Dataset         | Description                                             | Main Metric |
| --------------- | ------------------------------------------------------- | ----------- |
| Consumption     | Electricity consumption                                 | MWh         |
| Solar           | Solar electricity generation                            | MWh         |
| Wind Onshore    | Onshore wind generation                                 | MWh         |
| Wind Offshore   | Offshore wind generation                                | MWh         |
| Day-Ahead Price | Electricity market price                                | €/MWh       |
| Residual Load   | Electricity demand remaining after renewable generation | MWh         |

### SMARD Filter IDs

| Dataset         | SMARD Filter ID |
| --------------- | --------------: |
| Consumption     |             410 |
| Wind Offshore   |            1225 |
| Wind Onshore    |            4067 |
| Solar           |            4068 |
| Day-Ahead Price |            4169 |
| Residual Load   |            4359 |

---

## Data Units

The project preserves the units provided by SMARD:

* Generation: MWh per reporting interval
* Consumption: MWh per reporting interval
* Residual load: MWh per reporting interval
* Electricity price: €/MWh

Negative electricity prices are retained because they are legitimate observations in the electricity market and are analytically important.

---

## Technology Stack

### Data Engineering

* Python
* Pandas
* Requests
* PyArrow
* PostgreSQL
* Psycopg
* Python dotenv

### Cloud / Database

* PostgreSQL
* Aiven PostgreSQL
* DBeaver
* Postgres.app

### Business Intelligence

* Looker Studio

### Development

* Visual Studio Code
* Git
* GitHub

---

## Project Structure

```text
data-engineering-project/
│
├── README.md
├── .gitignore
├── requirements.txt
├── .env
│
├── data/
│   ├── raw/
│   └── processed/
│
├── src/
│   ├── ingestion/
│   │   ├── smard_consumption.py
│   │   ├── smard_solar.py
│   │   ├── smard_wind_offshore.py
│   │   ├── smard_wind_onshore.py
│   │   ├── smard_price.py
│   │   ├── smard_residual_load.py
│   │   ├── load_consumption.py
│   │   ├── load_solar.py
│   │   ├── load_wind_offshore.py
│   │   ├── load_wind_onshore.py
│   │   ├── load_price.py
│   │   ├── load_residual_load.py
│   │   ├── validate_all_data.py
│   │   └── sync_to_aiven.py
│   │
│   ├── transformation/
│   │   ├── clean_consumption.py
│   │   ├── clean_solar.py
│   │   ├── clean_wind_offshore.py
│   │   ├── clean_wind_onshore.py
│   │   ├── clean_price.py
│   │   └── clean_residual_load.py
│   │
│   └── run_pipeline.py
│
├── sql/
│   ├── tables.sql
│   └── views.sql
│
├── notebooks/
│
├── looker/
│   └── README.md
│
└── tests/
```

> Note: `.env`, raw data, processed data, and other local configuration files are excluded from version control through `.gitignore`.

---

# Data Pipeline

The pipeline follows a structured ingestion, transformation, loading, and validation workflow.

## 1. Data Ingestion

Python scripts retrieve the required datasets from SMARD.

Example ingestion modules include:

```text
smard_consumption.py
smard_solar.py
smard_wind_offshore.py
smard_wind_onshore.py
smard_price.py
smard_residual_load.py
```

The downloaded datasets are stored locally as raw files.

---

## 2. Data Transformation

The raw datasets are cleaned and standardized using Python/Pandas.

Transformation scripts include:

```text
clean_consumption.py
clean_solar.py
clean_wind_offshore.py
clean_wind_onshore.py
clean_price.py
clean_residual_load.py
```

The cleaned datasets are stored as Parquet files in:

```text
data/processed/
```

---

## 3. PostgreSQL Loading

The processed Parquet datasets are loaded into PostgreSQL.

The database schema is:

```text
energy_market
```

The main hourly tables are:

```text
energy_market.consumption_hourly
energy_market.solar_hourly
energy_market.wind_offshore_hourly
energy_market.wind_onshore_hourly
energy_market.price_hourly
energy_market.residual_load_hourly
```

Each dataset uses the timestamp as the primary time dimension.

---

## 4. Analytical Data Model

The individual datasets are combined into an hourly analytical view:

```text
energy_market.energy_market_hourly
```

The view combines:

* Consumption
* Solar generation
* Onshore wind generation
* Offshore wind generation
* Electricity price
* Residual load
* Calendar dimensions

This provides a unified analytical layer for downstream analysis.

---

# BI Data Model

A dedicated BI table is used to provide a stable dataset for dashboarding:

```text
energy_market.bi_energy_market
```

The BI table contains:

```text
timestamp
date
year
month
day
hour
day_of_week
is_weekend
consumption
solar_generation
wind_onshore
wind_offshore
price
residual_load
total_generation
last_refresh_at
```

### Total Renewable Generation

The BI table calculates:

```text
total_generation =
    solar_generation
    + wind_onshore
    + wind_offshore
```

This is implemented as a PostgreSQL generated column so that the calculation remains consistent within the database layer.

---

## Generation Breakdown View

A separate analytical view is used for renewable-generation composition:

```text
energy_market.bi_generation
```

It transforms the generation columns into a long-format structure:

```text
timestamp
generation_type
generation
```

with generation categories:

```text
solar
onshore
offshore
```

This structure is used for generation-mix visualizations in Looker Studio.

---

# Data Validation

Data quality checks are included as part of the pipeline.

The validation script is:

```text
src/ingestion/validate_all_data.py
```

The validation process checks each main dataset for:

* Row count
* Minimum timestamp
* Maximum timestamp
* Null timestamps
* Duplicate timestamps

The pipeline therefore includes validation before the data is used for analysis.

Example validation output:

```text
Rows: ...
Start: ...
End: ...
Null timestamps: 0
Duplicate timestamps: 0
```

---

# Cloud Database

Aiven PostgreSQL is used as the cloud-hosted BI data layer.

The architecture intentionally separates:

### Local PostgreSQL

Used as the primary engineering and development database.

### Aiven PostgreSQL

Used as the cloud copy consumed by Looker Studio.

The synchronization process is handled by:

```text
src/ingestion/sync_to_aiven.py
```

The script:

1. Reads the local BI dataset.
2. Creates a pipeline refresh timestamp.
3. Clears the existing Aiven BI table.
4. Loads the refreshed dataset.
5. Records the refresh timestamp.

Database credentials are stored in environment variables and are not committed to GitHub.

---

# Looker Studio Dashboard

The project includes an interactive Looker Studio dashboard called:

## Germany Energy Analytics

### Dashboard subtitle

**Electricity Prices, Demand & Renewable Generation Analytics**

The dashboard is designed to provide both high-level KPIs and detailed market analysis.

### Dashboard components

The dashboard includes analysis of:

* Average electricity price
* Electricity price over time
* Renewable generation
* Electricity consumption
* Residual load
* Price vs. residual load
* Average price by hour
* Renewable generation mix
* Data freshness

### Dashboard pages

#### 1. Date Range Analysis

Designed for flexible analysis over selected date ranges.

#### 2. Year & Month Analysis

Designed for comparing market behavior across selected years and months.

### Interactive Controls

The dashboard includes time-based filtering such as:

* Date range
* Year
* Month

These controls allow users to explore the electricity market across different time periods.

---

## Dashboard Screenshots

Dashboard screenshots are stored in:

```text
looker/
```

Planned screenshots include:

```text
looker/
├── README.md
├── date_range_analysis.png
└── year_month_analysis.png
```

---

# Key Analytical Questions

The dashboard and analytical model are designed to answer questions such as:

### Electricity Prices

* How do electricity prices change over time?
* Which hours tend to have higher or lower average prices?
* How frequently do negative prices occur?

### Renewable Generation

* How much electricity is generated by solar and wind?
* How does the generation mix change over time?
* Which renewable source contributes the most generation?

### Demand

* How does electricity consumption vary by hour?
* How does demand change across different periods?

### Residual Load

* How does residual load change over time?
* What relationship exists between residual load and electricity prices?

### Market Relationships

* Does lower residual load correspond with lower electricity prices?
* How does renewable generation relate to electricity prices?
* Are there identifiable hourly or seasonal patterns?

---

# Reproducibility

The project is designed so that the pipeline can be executed from the project root.

Activate the virtual environment:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure the required environment variables in:

```text
.env
```

The `.env` file is intentionally excluded from Git.

Then run the complete pipeline:

```bash
python src/run_pipeline.py
```

The pipeline performs:

```text
SMARD ingestion
      ↓
Data cleaning
      ↓
PostgreSQL loading
      ↓
Data validation
      ↓
BI dataset refresh
      ↓
Aiven synchronization
```

---

# Environment Variables

Local and cloud database configuration is stored outside the source code.

Example structure:

```text
# Local PostgreSQL
DB_NAME=...
DB_USER=...
DB_HOST=...
DB_PORT=...

# Aiven PostgreSQL
AIVEN_DB=...
AIVEN_USER=...
AIVEN_PASSWORD=...
AIVEN_HOST=...
AIVEN_PORT=...
```

Actual credentials are never stored in the repository.

---

# SQL Layer

The SQL layer contains the database definitions and analytical views.

### `sql/tables.sql`

Contains PostgreSQL table definitions for the project's data model.

### `sql/views.sql`

Contains analytical views used to combine and reshape the data for analysis and BI reporting.

The SQL layer separates analytical modeling from the Python ingestion process.

---

# Data Engineering Practices

This project demonstrates several practical data engineering and analytics practices:

* API/public-data ingestion
* Modular Python pipeline design
* Data cleaning and transformation
* Parquet-based intermediate storage
* PostgreSQL relational modeling
* SQL analytical views
* Database-generated calculations
* Data validation
* Environment-based configuration
* Cloud PostgreSQL deployment
* BI data modeling
* Interactive dashboard development
* Reproducible pipeline execution
* Git/GitHub version control

---

# Future Improvements

The current version focuses on building a reliable analytical foundation.

Potential future versions include:

### Machine Learning

* Predict negative electricity-price events
* Forecast electricity prices
* Predict high-price periods
* Model renewable-generation effects on prices

### Data Quality

* Automated checks for missing hourly intervals
* Range validation for generation and consumption
* Automated detection of unusual observations
* Pipeline-level data-quality reporting

### Analytics

* Seasonal analysis
* Renewable penetration metrics
* Negative-price event analysis
* Price volatility analysis
* Renewable generation vs. price relationships
* More advanced residual-load analysis

### Automation

* Automated scheduled data ingestion
* Automated cloud synchronization
* Dashboard refresh automation
* Monitoring and alerting for pipeline failures

### AI Analytics

A future version may add evidence-grounded AI capabilities that explain market patterns using the project's validated analytical data rather than unsupported assumptions.

---

# Current Project Scope

The current version is focused on:

```text
Historical electricity-market analytics
+
Data engineering pipeline
+
PostgreSQL analytical modeling
+
Cloud BI data layer
+
Looker Studio dashboard
```

Predictive machine learning and AI features are planned future extensions and are not represented as completed features in the current version.

---

# Project Status

**Version:** v1.0

**Status:** Completed analytical foundation

### Completed

* [x] SMARD data ingestion
* [x] Data cleaning
* [x] Parquet processing
* [x] PostgreSQL data storage
* [x] Analytical SQL views
* [x] BI dataset
* [x] Data validation
* [x] Aiven PostgreSQL synchronization
* [x] Looker Studio dashboard
* [x] Environment-based database configuration

### Planned

* [ ] Automated scheduling
* [ ] Expanded data-quality tests
* [ ] Negative-price prediction
* [ ] Price forecasting
* [ ] Advanced analytics
* [ ] AI-assisted market analysis

---

# Author

**Kavana**

Data Analytics / Data Engineering Project

This project demonstrates an end-to-end workflow from public energy-market data ingestion through data engineering, SQL analytics, cloud database deployment, and business intelligence reporting.
