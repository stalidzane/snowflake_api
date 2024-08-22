# COVID-19 Data Integration, Analysis, and Visualization Platform - snowflake_api

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Data Sources](#data-sources)
- [Techniques Used](#modeling-techniques)

## Introduction
This project aims to provide an application which provides integrated approach of COVID-19 data querying, analysis and visualization, use of different databases and various resources all in one.

## Features
- Time series forecasting for COVID-19 metrics (infection rate, mortality rate)
- Interactive visualizations for forecasts and various parameters
- Support for comparison of multiple countries for effective analysis

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/stalidzane/snowflake_api.git
   ```
2. Navigate to the project directory:
   ```bash
   cd snowflake_api
   ```
3. Create a virtual environment using Python 3.12:
   ```bash
   python3 -m venv api_env
   ```
4. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Run the application:
   ```bash
   python3 app.py
   ```
   NOTE. Some machines need python to work.

## Usage
- Run the application and navigate to `http://localhost:8001` in your browser.
- Select the countries and parameters you wish to compare.
- Choose one of the parameters available for analysis, click "Submit" to display the results.
- Click "Get Prediction" to generate forecasts.
- View the interactive plots and leave comments for future analysis.

## Data Sources
- COVID-19 data from [COVID19_EPIDEMIOLOGICAL_DATA provided by Starschema](https://app.snowflake.com/marketplace/listing/GZSNZ7F5UH/starschema-covid-19-epidemiological-data?dbName=COVID19_EPIDEMIOLOGICAL_DATA&originTab=provider&providerName=Starschema&profileGlobalName=GZSNZ7F5UL)

## Techniques Used
- **Plot generation:** Uses Matplotlib in collaboration with pandas to generate insightful plots.
- **Time Series Forecasting:** Uses Facebook's Prophet model for predicting future infection and mortality rates.
- **SQL Querying** Used to query extensive Snowflake dataset.