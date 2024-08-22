import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64
from flask import jsonify

def mortality_rate_query(c1):
    sql=f"""
    SELECT
        SUB.DATE,
        CASE 
            WHEN SUM(SUB.TOTAL_CONFIRMED) OVER (ORDER BY SUB.DATE) > 0 
            THEN (SUM(SUB.TOTAL_DEATHS) OVER (ORDER BY SUB.DATE) /
                SUM(SUB.TOTAL_CONFIRMED) OVER (ORDER BY SUB.DATE)) * 100
            ELSE NULL
        END AS MORTALITY_RATE
    FROM
        (
            SELECT
                DATE,
                SUM(CASE WHEN CASE_TYPE = 'Confirmed' THEN CASES ELSE 0 END) AS TOTAL_CONFIRMED,
                SUM(CASE WHEN CASE_TYPE = 'Deaths' THEN CASES ELSE 0 END) AS TOTAL_DEATHS
            FROM
                JHU_COVID_19
            WHERE
                COUNTRY_REGION = '{c1}'  
                AND DATE BETWEEN '2020-01-22' AND '2023-03-09'
            GROUP BY
                DATE
        ) SUB
    ORDER BY
        SUB.DATE;
    """
    return sql

def plot_graph_mortality(c1, c2, param, conn):
    df_c1 = pd.read_sql(mortality_rate_query(c1), conn)
    df_c2 = pd.read_sql(mortality_rate_query(c2), conn)

    # Ensure the cases are numbers, not strings
    df_c1['MORTALITY_RATE'] = pd.to_numeric(df_c1['MORTALITY_RATE'], errors='coerce')
    df_c2['MORTALITY_RATE'] = pd.to_numeric(df_c2['MORTALITY_RATE'], errors='coerce')


    # Ensure the date column is in datetime format
    df_c1['DATE'] = pd.to_datetime(df_c1['DATE']).dt.date
    df_c2['DATE'] = pd.to_datetime(df_c2['DATE']).dt.date
 
    # Plot the mortality rate in a bar graph
    plt.figure(figsize=(10, 6))
    plt.plot(df_c1['DATE'], df_c1['MORTALITY_RATE'], label=f'Mortality rate in {c1}')
    plt.plot(df_c2['DATE'], df_c2['MORTALITY_RATE'], label=f'Mortality rate in {c2}')
    plt.title(f'COVID-19 mortality rate in {c1} and {c2} from 2020-01-22 to 2023-03-09')
    plt.xlabel('Country')
    plt.ylabel('Number of cases')
    plt.legend()

    # Save the plot to a bytes buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()

    
    # Return the image as a base64 encoded string in a JSON response
    return jsonify({"plot": img_base64})

def cases_deaths_query(c1, param):
    # Determine the case to query based on param
    case = {
        "cumulative_cases": "Confirmed",
        "total_deaths": "Deaths"
    }.get(param)
    sql = f"""
    SELECT 
        COUNTRY_REGION AS COUNTRY, 
        SUM(CASES) AS CASES,
        DATE
    FROM 
        JHU_COVID_19
    WHERE 
        COUNTRY_REGION = '{c1}' AND CASE_TYPE ='{case}'
        AND DATE BETWEEN '2020-01-22' AND '2023-03-09'
    GROUP BY 
        COUNTRY_REGION, DATE
    ORDER BY 
        DATE;
    """
    return sql

def plot_graph_cases(c1, c2, param, conn):
    column = {
        "cumulative_cases": "Cumulative cases",
        "total_deaths": "Total deaths"
    }.get(param)

    df_c1 = pd.read_sql(cases_deaths_query(c1, param), conn)
    df_c2 = pd.read_sql(cases_deaths_query(c2, param), conn)
    # Ensure the cases are numbers, not strings
    df_c1['CASES'] = pd.to_numeric(df_c1['CASES'], errors='coerce')
    df_c2['CASES'] = pd.to_numeric(df_c2['CASES'], errors='coerce')


    # Ensure the date column is in datetime format
    df_c1['DATE'] = pd.to_datetime(df_c1['DATE']).dt.date
    df_c2['DATE'] = pd.to_datetime(df_c2['DATE']).dt.date

    # Plot the cases in a bar graph
    plt.figure(figsize=(10, 6))
    plt.plot(df_c1['DATE'], df_c1['CASES'], label=f'Cases in {c1}')
    plt.plot(df_c2['DATE'], df_c2['CASES'], label=f'Cases in {c2}')
    plt.title(f'COVID-19 {column} in {c1} and {c2} from 2020-01-22 to 2023-03-09')    #from {start_date} to {end_date}')
    plt.xlabel('Country')
    plt.ylabel('Number of cases')
    plt.legend()

    # Save the plot to a bytes buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()

    
    # Return the image as a base64 encoded string in a JSON response
    return jsonify({"plot": img_base64})


def infection_rate_query(c1):
    # Both databases have different names for United Kingdom
    if c1 == "United Kingdom":
        sql = f'''
SELECT 
    JHU.DATE, 
    JHU.COUNTRY_REGION, 
    (SUM(JHU.CASES) / ECDC.POPULATION) * 100 AS INFECTION_RATE
FROM 
    JHU_COVID_19 JHU
INNER JOIN 
    (SELECT COUNTRY_REGION, POPULATION AS POPULATION FROM ECDC_GLOBAL WHERE COUNTRY_REGION = 'United_Kingdom' GROUP BY COUNTRY_REGION, POPULATION) ECDC
    ON JHU.COUNTRY_REGION = 'United Kingdom'
WHERE 
    JHU.DATE BETWEEN '2020-01-22' AND '2023-03-09'
    AND JHU.COUNTRY_REGION = 'United Kingdom' 
    AND JHU.CASE_TYPE = 'Confirmed'
GROUP BY 
    JHU.DATE, JHU.COUNTRY_REGION, ECDC.POPULATION
ORDER BY 
    JHU.DATE, JHU.COUNTRY_REGION;

'''
    else:
        sql = f'''
SELECT 
    JHU.DATE, 
    JHU.COUNTRY_REGION, 
    (SUM(JHU.CASES) / ECDC.POPULATION) * 100 AS INFECTION_RATE
FROM 
    JHU_COVID_19 JHU
INNER JOIN 
    (SELECT COUNTRY_REGION, POPULATION AS POPULATION FROM ECDC_GLOBAL GROUP BY COUNTRY_REGION, POPULATION) ECDC
    ON JHU.COUNTRY_REGION = ECDC.COUNTRY_REGION
WHERE 
    JHU.DATE BETWEEN '2020-01-22' AND '2023-03-09'
    AND JHU.COUNTRY_REGION = '{c1}' AND JHU.CASE_TYPE = 'Confirmed'
GROUP BY 
    JHU.DATE, JHU.COUNTRY_REGION, ECDC.POPULATION
ORDER BY 
    JHU.DATE, JHU.COUNTRY_REGION;

'''
    return sql

def plot_graph_infection(c1, c2, conn):
    df_c1 = pd.read_sql(infection_rate_query(c1), conn)
    df_c2 = pd.read_sql(infection_rate_query(c2), conn)
    # Ensure the cases are numbers, not strings
    df_c1['INFECTION_RATE'] = pd.to_numeric(df_c1['INFECTION_RATE'], errors='coerce')
    df_c2['INFECTION_RATE'] = pd.to_numeric(df_c2['INFECTION_RATE'], errors='coerce')


    # Ensure the date column is in datetime format
    df_c1['DATE'] = pd.to_datetime(df_c1['DATE']).dt.date
    df_c2['DATE'] = pd.to_datetime(df_c2['DATE']).dt.date

    # Plot the infection rate for both countries
    plt.figure(figsize=(10, 6))
    plt.plot(df_c1['DATE'], df_c1['INFECTION_RATE'], label=f'Infection Rate {c1}(%)')
    plt.plot(df_c2['DATE'], df_c2['INFECTION_RATE'], label=f'Infection Rate {c2}(%)')
    plt.title(f'COVID-19 Infection Rate in {c1} and {c2}')
    plt.xlabel('Date')
    plt.ylabel('Infection Rate (%)')
    plt.legend()

    # Save the plot to a bytes buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()

    
    # Return the image as a base64 encoded string in a JSON response
    return jsonify({"plot": img_base64})