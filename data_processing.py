import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use Agg backend for non-interactive plotting
import matplotlib.pyplot as plt
import io
import base64
from flask import jsonify

# from connector import connect
# conn =connect()

def cases_deaths_query(c1, c2, param1, param2):
    # Determine the column to query based on param2
    case = {
        "cumulative_cases": "Confirmed",
        "total_deaths": "Deaths"
    }.get(param2)
    sql = f"""
    SELECT 
        COUNTRY_REGION AS Country, 
        {param1}(CASES) AS CASES,
        min(date) as Starting_date, 
        max(date) as Ending_date
    FROM 
        JHU_COVID_19
    WHERE 
        COUNTRY_REGION IN ('{c1}', '{c2}') AND CASE_TYPE ='{case}'
    GROUP BY 
        COUNTRY_REGION;
    """
    return sql

def plot_graph_cases(c1, c2, param1, param2, conn):
    column = {
        "cumulative_cases": "Cumulative cases",
        "total_deaths": "Total deaths"
    }.get(param2)

    df_c1 = pd.read_sql(cases_deaths_query(c1, c2, param1, param2), conn)
    # Ensure the date column is in datetime format
    df_c1['STARTING_DATE'] = pd.to_datetime(df_c1['STARTING_DATE'])
    df_c1['ENDING_DATE'] = pd.to_datetime(df_c1['ENDING_DATE'])
    start_date = df_c1.loc[0, 'STARTING_DATE'].strftime('%Y-%m-%d')
    end_date = df_c1.loc[0, 'ENDING_DATE'].strftime('%Y-%m-%d')


    # Plot the cases in a bar graph
    plt.figure(figsize=(10, 6))
    plt.bar(df_c1['COUNTRY'], df_c1['CASES'], width=0.4)
    plt.title(f'COVID-19 {column} in {c1} and {c2} from {start_date} to {end_date}')
    plt.xlabel('Country')
    plt.ylabel('Cumulative number of cases')
    plt.legend()
    # plt.show()

    # Save the plot to a bytes buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()

    
    # Return the image as a base64 encoded string in a JSON response
    return jsonify({"plot": img_base64})


def relative_cases(c1):
    sql_query = f'''
SELECT 
    jhu.date, 
    jhu.country_region, 
    (SUM(jhu.cases) / ecdc.population)*100 AS relative_daily_cases
FROM 
    jhu_covid_19 jhu
INNER JOIN 
    (SELECT country_region, population AS population FROM ecdc_global GROUP BY country_region, population) ecdc
    ON jhu.country_region = ecdc.country_region
WHERE 
    jhu.date BETWEEN '2020-01-22' AND '2023-03-09'
    AND jhu.country_region = '{c1}' AND jhu.case_type ='Confirmed'
GROUP BY 
    jhu.date, jhu.country_region, ecdc.population
ORDER BY 
    jhu.date, jhu.country_region;
'''
    return sql_query

def plot_graph_relative(c1, c2, conn):
    df_c1 = pd.read_sql(relative_cases(c1), conn)
    df_c2 = pd.read_sql(relative_cases(c2), conn)
    # Ensure the date column is in datetime format
    df_c1['DATE'] = pd.to_datetime(df_c1['DATE']).dt.date
    df_c2['DATE'] = pd.to_datetime(df_c2['DATE']).dt.date

    # Plot the relative daily cases for both countries
    plt.figure(figsize=(10, 6))
    plt.plot(df_c1['DATE'], df_c1['RELATIVE_DAILY_CASES'], label=f'Relative Daily Cases {c1}(%)')
    plt.plot(df_c2['DATE'], df_c2['RELATIVE_DAILY_CASES'], label=f'Relative Daily Cases {c2}(%)')
    plt.title(f'COVID-19 Relative Daily Cases in {c1} and {c2}')
    plt.xlabel('Date')
    plt.ylabel('Relative Daily Cases (%)')
    plt.legend()
    # plt.show()

    # Save the plot to a bytes buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()

    
    # Return the image as a base64 encoded string in a JSON response
    return jsonify({"plot": img_base64})

# c1 = 'Germany'
# c2 = 'France'
# print(plot_graph(c1, c2, conn))