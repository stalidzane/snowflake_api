import os

import snowflake.connector
from flask import Blueprint, request, jsonify

from data_processing import plot_graph_infection, plot_graph_cases, plot_graph_mortality
from data_prediction import plot_prediction
from mongo_connect import add_user_comment, get_user_comments

# Make the Snowflake connection
def connect() -> snowflake.connector.SnowflakeConnection:
    creds = {
            'account': "TE31414",
            'user': 'lindastalidzane',
            'password': "Apelsins15!",
            'warehouse': "COMPUTE_WH",
            'database': "COVID19_DATA",
            'schema': "PUBLIC",
            'host' : "te31414.us-east-2.aws.snowflakecomputing.com",
            'client_session_keep_alive': True
        }
    return snowflake.connector.connect(**creds)

conn = connect()

connector = Blueprint('connector', __name__)

@connector.route('/cases/<c1>/<c2>/<param>')
def cases(c1, c2, param):
    if param in ["cumulative_cases", "total_deaths"]:
        return plot_graph_cases(c1, c2, param, conn)
    elif param == "infection_rate":
        return plot_graph_infection(c1, c2, conn)
    elif param == "mortality_rate":
        return plot_graph_mortality(c1, c2, param, conn)
    
@connector.route('/add_comment', methods=['POST'])
def add_comment():
    data = request.json
    response = add_user_comment(data)
    return jsonify(response), 201

@connector.route('/get_comments', methods=['GET'])
def get_comments():
    return get_user_comments()

@connector.route('/get_prediction/<c1>/<c2>/<pred>')
def get_prediction(c1, c2, pred):
    return plot_prediction(c1, c2, conn, pred)