# COVID Atlas

An interactive dashboard for exploring and comparing COVID-19 epidemiological trends across countries. Select two countries on a clickable world map, compare key metrics side by side, generate Prophet forecasts, and leave annotations that persist in MongoDB — all served through a Flask API backed by Snowflake.

---

## Overview

**Data layer:** COVID-19 case and death data is queried live from the [Starschema COVID-19 dataset](https://app.snowflake.com/marketplace/listing/GZSNZ7F5UH/) on the Snowflake Marketplace, joined with ECDC population data for rate calculations.

**Compute layer:** Flask serves a REST API with endpoints for querying Snowflake, generating Matplotlib charts as base64-encoded images, and running Prophet time-series forecasts.

**Persistence layer:** User comments are stored in and retrieved from MongoDB Atlas, scoped to the country pair and metric being viewed.

---

## Features

- **Clickable world map** — select two countries for comparison directly on the map
- **Four metrics:** cumulative cases, total deaths, infection rate, mortality rate
- **Prophet forecasting** — 300-day ahead forecasts for infection and mortality rate, plotted alongside actuals
- **Comment system** — leave notes on any country/metric combination, saved to MongoDB and visible to all users

---

## Architecture

```
browser
  └── combined.html (map + charts UI)
        └── Flask (app.py)
              ├── connector.py       # API routes
              ├── data_processing.py # SQL queries + Matplotlib charts
              ├── data_prediction.py # Prophet forecasting
              └── mongo_connect.py   # MongoDB read/write
                    ├── Snowflake (COVID-19 data, population data)
                    └── MongoDB Atlas (user comments)
```

---

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/your-username/covid-atlas.git
cd covid-atlas
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv env

# macOS / Linux
source env/bin/activate

# Windows
env\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure credentials

Create a `.env` file in the project root (this file is gitignored — never commit it):

```env
SNOWFLAKE_ACCOUNT=your_account_locator
SNOWFLAKE_USER=your_username
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_WAREHOUSE=your_warehouse
SNOWFLAKE_HOST=your_account_url_without_https

MONGO_URI=your_mongodb_connection_string
```

### 5. Set up Snowflake data access

In a Snowflake worksheet, run the following — replacing `<shared_db>` with your chosen database name:

```sql
CREATE DATABASE <shared_db> FROM SHARE SZ21568.SNOW_API;
```

This gives you access to the pre-built share containing the JHU and ECDC datasets used by the app.

### 6. Run the app

```bash
python3 app.py
```

Navigate to `http://localhost:8001` in your browser.

---

## Usage

1. Click two countries on the world map to select them
2. Choose a metric (cumulative cases, total deaths, infection rate, mortality rate)
3. Click **Submit** to display a comparison chart
4. Click **Get Prediction** to generate a 300-day Prophet forecast for that metric
5. Leave a comment — it will be saved to MongoDB and displayed for that country/metric combination

---

## Repo Structure

```
covid-atlas/
│
├── app.py                 # Flask app entry point
├── connector.py           # API route definitions
├── data_processing.py     # Snowflake queries and chart generation
├── data_prediction.py     # Prophet forecasting
├── mongo_connect.py       # MongoDB connection and comment CRUD
│
├── templates/
│   └── combined.html      # Frontend — map, charts, comments UI
│
├── requirements.txt
├── .env                   # Credentials — gitignored, never committed
├── .gitignore
└── README.md
```

---

## Data Sources

- **JHU COVID-19** — Johns Hopkins University case and death data, accessed via [Starschema on Snowflake Marketplace](https://app.snowflake.com/marketplace/listing/GZSNZ7F5UH/)
- **ECDC Global** — European Centre for Disease Prevention and Control population data, used to compute per-capita rates

Data covers **2020-01-22 to 2023-03-09**, matching the active JHU reporting period.

---

## Known Limitations

- The Starschema dataset on Snowflake Marketplace must be independently provisioned — data is not bundled with this repo
- Infection rate for the United Kingdom requires a special-cased query due to a naming inconsistency (`United Kingdom` vs `United_Kingdom`) between the JHU and ECDC tables
- Prophet forecasts assume the pandemic trend continues — predictions beyond the training window should be interpreted cautiously
- Comments are shared globally across all users (no authentication)
