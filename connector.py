import datetime
import os
import logging

import snowflake.connector
from snowflake.connector import DictCursor
from flask import Blueprint, request, abort, jsonify, make_response

from data_processing import plot_graph_relative, plot_graph_cases
from mongo_connect import add_user_comment, get_user_comments

# Make the Snowflake connection
def connect() -> snowflake.connector.SnowflakeConnection:
    creds = {
            'account': "SZ21568",
            'user': 'linda',
            'password': "Galdalete1",
            'warehouse': "DATA_API",
            'database': "COVID19_EPIDEMIOLOGICAL_DATA",
            'schema': "PUBLIC",
            'host' : "sz21568.us-east-2.aws.snowflakecomputing.com",
            'client_session_keep_alive': True
        }
    return snowflake.connector.connect(**creds)

conn = connect()

# Make the API endpoints
connector = Blueprint('connector', __name__)

@connector.route('/cases/<c1>/<c2>/<param1>/<param2>')
def cases(c1, c2, param1, param2):
    if param2 in ["cumulative_cases", "total_deaths"]:
        # print("hello")
        # sql = cases_deaths_query(c1, c2, param1, param2)
        # try:
        #     res = conn.cursor(DictCursor).execute(sql)
        #     return make_response(jsonify(res.fetchall()))
        # except Exception as e:
        #     logging.error(f"Error executing query: {e}")
        #     abort(500, "Error reading from Snowflake. Check the logs for details.")
        return plot_graph_cases(c1, c2, param1, param2, conn)

    elif param2 == "relative_cases":
        # sql = get_relative_cases_query(c1, c2)
        return plot_graph_relative(c1, c2, conn)
    
@connector.route('/add_comment', methods=['POST'])
def add_comment():
    data = request.json
    response = add_user_comment(data)
    return jsonify(response), 201

@connector.route('/get_comments', methods=['GET'])
def get_comments():
    return get_user_comments()