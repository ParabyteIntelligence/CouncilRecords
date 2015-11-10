"""
Copyright (c) Parabyte Intelligence LLC 2015
Author: Rakshak Talwar

Description: The REST API which connects the client to the backend

Uses flask
"""

from flask import Flask, jsonify, request, url_for
import requests
import datetime, json, os

# create the application object
app = Flask(__name__)

# config
app.secret_key = 'kjrbglwjegbkgnerlkbluibgugle'

#the main request route
@app.route('/council_record/<start_date>/<end_date>/<min_amount>/<max_amount>/<search_query>', methods=['GET'])
def council_record(start_date, end_date, min_amount, max_amount, search_query):
    """Returns a respective JSON object when issued a query"""
    """start_date and end_date are strings in format YYYYMMDD. Use '0' for blank"""
    """min_amount and max_amount are floats. Use -1.0 for """
    """search_query is a string"""

    results = [] # will store all of the appropriate documents from elastic search, returned later

    # query Elastic Search for appropriate documents with respect to the query


    return jsonify({'results' : results})
