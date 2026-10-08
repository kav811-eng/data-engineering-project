# Looker Studio Dashboard

## Germany Energy Analytics

### Electricity Prices, Demand & Renewable Generation Analytics

This folder contains documentation and screenshots for the Looker Studio dashboard developed as part of the **Germany Energy Analytics** project.

The dashboard provides an interactive view of Germany's electricity market, focusing on electricity prices, electricity demand, renewable generation, and residual load.

---

## Dashboard Purpose

The dashboard was designed to answer the following business question:

> **How do renewable generation, electricity demand, and residual load influence electricity prices in Germany?**

Users can explore the data across different time periods and investigate relationships between electricity-market variables.

---

## Data Source

The dashboard uses a BI dataset hosted in **Aiven PostgreSQL**.

The underlying data originates from **SMARD**, the German Federal Network Agency's electricity-market data platform.

Data flow:

```text
SMARD
  ↓
Python ingestion
  ↓
Data cleaning
  ↓
Local PostgreSQL
  ↓
BI analytical dataset
  ↓
Aiven PostgreSQL
  ↓
Looker Studio
```

---

## Dashboard

**[View the interactive dashboard](https://datastudio.google.com/reporting/f0e135d2-bb43-4063-8b3d-f6f9f7392114)**

### 1. Date Range Analysis

This page provides flexible analysis across selected date ranges.

It includes:

* Average electricity price
* Electricity price over time
* Renewable generation
* Electricity consumption
* Residual load
* Price vs. residual load
* Average price by hour
* Renewable generation mix
* Data freshness

The date-range controls allow users to investigate specific periods and compare market behavior over time.

---

### 2. Year & Month Analysis

This page provides more structured time-based analysis using:

* Year
* Month
* Hour
* Other available calendar dimensions

This allows users to investigate differences between years and months and identify recurring market patterns.

---

## Key Metrics

### Average Electricity Price

Measures the average day-ahead electricity price for the selected period.

**Unit:** €/MWh

---

### Electricity Consumption

Measures electricity demand during the selected period.

**Unit:** MWh per reporting interval

---

### Renewable Generation

Combines:

* Solar generation
* Onshore wind generation
* Offshore wind generation

**Unit:** MWh per reporting interval

---

### Residual Load

Represents the electricity demand remaining after accounting for renewable generation.

**Unit:** MWh per reporting interval

Residual load is used as an important analytical variable when investigating electricity-price behavior.

---

## Main Visualizations

### Electricity Price Over Time

Shows how electricity prices change across the selected period.

This helps identify:

* Price spikes
* Low-price periods
* Negative-price events
* Changes in market conditions

---

### Renewable Generation vs. Consumption

Compares renewable electricity generation with electricity consumption.

This helps illustrate how renewable availability relates to overall electricity demand.

---

### Residual Load Over Time

Shows changes in residual load across the selected period.

This helps identify periods when renewable generation accounts for a larger or smaller share of electricity demand.

---

### Price vs. Residual Load

A scatter plot comparing:

* **X-axis:** Residual load
* **Y-axis:** Electricity price

This visualization is used to investigate whether changes in residual load are associated with changes in electricity prices.

---

### Average Price by Hour

Shows the average electricity price for each hour of the day.

This helps identify recurring intraday price patterns.

---

### Renewable Generation Mix

Shows the composition of renewable generation across:

* Solar
* Onshore wind
* Offshore wind

This provides a simple view of the contribution of each renewable source.

---

### Data Freshness

The BI dataset contains a refresh timestamp so that the dashboard can indicate when the underlying dataset was last synchronized.

---

## Dashboard Filters

The dashboard provides interactive time controls including:

* Date range
* Year
* Month

These controls allow users to focus the analysis on specific periods.

---

## Dashboard Screenshots

Screenshots of the dashboard are stored in this folder.

Planned structure:

```text
looker/
├── README.md
├── dashboard_overview.png
├── date_range_analysis.png
└── year_month_analysis.png
```

---

## Dashboard Access

The dashboard is currently maintained in Looker Studio.

A public dashboard link can be added here once the report has been configured for appropriate public or viewer access.

**Dashboard:** *Link to be added*

---

## Notes on Data Modeling

The dashboard primarily uses the PostgreSQL BI dataset:

```text
energy_market.bi_energy_market
```

A separate analytical view is used for renewable-generation composition:

```text
energy_market.bi_generation
```

The BI model was designed to keep the main hourly dataset at one row per timestamp while allowing generation-source breakdowns for visualization.

---

## Analytical Focus

The dashboard is intended to support analysis of:

* Electricity price behavior
* Renewable generation patterns
* Electricity demand
* Residual load
* Intraday price patterns
* Renewable generation mix
* Relationships between residual load and electricity prices
* Negative electricity-price periods

---

## Future Dashboard Improvements

Potential future improvements include:

* Negative-price event KPIs
* Renewable penetration percentage
* Price volatility indicators
* Seasonal analysis
* More detailed wind and solar analysis
* Additional year-over-year comparisons
* Automated dashboard annotations
* Predictive price indicators
* Machine-learning outputs
* Evidence-grounded AI market explanations

---

## Project

This dashboard is part of the **Germany Energy Analytics** project.

For the full project architecture, data pipeline, database design, validation process, and setup instructions, see the main project README.

---
