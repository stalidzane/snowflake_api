import os
import logging

from flask import Flask, jsonify, make_response, render_template
from connector import connector

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
app.register_blueprint(connector, url_prefix='/connector')

@app.route("/")
def default():
    return render_template('combined.html')


@app.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify(error='Not found!'), 404)

if __name__ == '__main__':
    app.run(port=8001, host='0.0.0.0')