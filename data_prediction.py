from prophet import Prophet
import pandas as pd
import matplotlib
# matplotlib.use('Agg')  # Use Agg backend for non-interactive plotting
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import io
from data_processing import infection_rate_query, mortality_rate_query
from flask import jsonify

# from connector import connect
# conn = connect()

def plot_prediction(c1, c2, conn, pred):
    if pred == "infection_rate":
        sql_c1 = infection_rate_query(c1)
        sql_c2 = infection_rate_query(c2)
    elif pred == "mortality_rate":
        sql_c1 = mortality_rate_query(c1)
        sql_c2 = mortality_rate_query(c2)
    
    param = {
        "infection_rate": "INFECTION_RATE",
        "mortality_rate": "MORTALITY_RATE"
    }.get(pred)

    parameter = param.replace("_", " ").title()
    df_c1 = pd.read_sql(sql_c1, conn)
    df_c2 = pd.read_sql(sql_c2, conn)

    # Ensure the date column is in the correct format and rename it to 'ds'
    df_c1['ds'] = pd.DatetimeIndex(df_c1['DATE'])
    df_c2['ds'] = pd.DatetimeIndex(df_c2['DATE'])
    # Rename the column you want to forecast to 'y'
    df_c1['y'] = df_c1[f'{param}']
    df_c2['y'] = df_c2[f'{param}']
    print(df_c1.head())
    print(df_c2.head())
    # Initialize the Prophet model
    model_c1 = Prophet()
    model_c2 = Prophet()

    # Fit the model to your data
    model_c1.fit(df_c1)
    model_c2.fit(df_c2)

    # Create a DataFrame to hold future dates (e.g., next 30 days)
    future = model_c1.make_future_dataframe(periods=300)
    future = model_c2.make_future_dataframe(periods=300)
    # Generate predictions
    forecast_c1 = model_c1.predict(future)
    forecast_c2 = model_c2.predict(future)

    # # Optional: Plot forecast components (trend, weekly, yearly effects)
    model_c1.plot_components(forecast_c1).show()

    # Generate and plot the forecast
    plt.figure(figsize=(10, 6))
    # fig = model_c1.plot(forecast)
    # Fit the models to your data
    
    # Plot actual data for Country 1
    plt.plot(df_c1['ds'], df_c1['y'], label=f'{c1} Actual {parameter}', color='blue', linestyle='-')

    # Plot forecast for Country 1
    plt.plot(forecast_c1['ds'], forecast_c1['yhat'], label=f'{c1} Predicted {parameter}', color='blue', linestyle='--')

    # Plot actual data for Country 2
    plt.plot(df_c2['ds'], df_c2['y'], label=f'{c2} Actual {parameter}', color='red', linestyle='-')

    # Plot forecast for Country 2
    plt.plot(forecast_c2['ds'], forecast_c2['yhat'], label=f'{c2} Predicted {parameter}', color='red', linestyle='--')

    
    plt.title(f'COVID-19 {parameter} Forecast')
    plt.xlabel('Date')
    plt.ylabel(parameter)
    plt.legend()

    # Save the plot to a PNG image in memory
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    # Convert the image to a base64 string to embed in HTML
    plot_url = base64.b64encode(buf.getvalue()).decode('utf-8')
    print("prediction was created")
    buf.close()
    return jsonify({"plot_url": plot_url})


# plot_prediction('Germany', 'France', conn)