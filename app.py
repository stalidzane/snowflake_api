import os
#import ngrok
import logging

from flask import Flask, jsonify, make_response, send_file, render_template
from connector import connector
#from snowpark import snowpark

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
app.register_blueprint(connector, url_prefix='/connector')
#app.register_blueprint(snowpark, url_prefix='/snowpark')

@app.route("/")
def default():
    # return make_response(jsonify(result='Nothing to see here'))
    return render_template('combined.html')

@app.route("/test")
def tester():
    
    return send_file("combined.html")

@app.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify(error='Not found!'), 404)

if __name__ == '__main__':
    # print("Available routes:")
    # for rule in app.url_map.iter_rules():
    #     print(f"{rule.endpoint}: {rule}")
    app.run(port=8001, host='0.0.0.0')