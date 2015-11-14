"""
Copyright (c) Parabyte Intelligence LLC 2015
Author: Rakshak Talwar

Description: The REST API which connects the client to the backend

"""

from flask import Flask, jsonify, request, url_for
from elasticsearch import Elasticsearch
import datetime, json, os

# create the application object
app = Flask(__name__)

# config
app.secret_key = 'kjrbglwjegbkgnerlkbluibgugle'

# some global variables
index_name = 'councilrec'
type_name = 'recs'

# create elasticsearch client instance
es = Elasticsearch()

def generate_filters(start_date, end_date, min_amount, max_amount):
    """ Generates a list of filters for use in the Elastic Search query """
    # take in query information
    if start_date == '0':
        start_date = 0
    if end_date == '0':
        end_date = 0

    if min_amount == '-1':
        min_amount = 0
    if max_amount == '-1':
        max_amount = 0

    # create date range dict
    if start_date and end_date: # if both start and end date exist
        date_range_dict = {"range" : {"date" : {"from" : start_date, "to" : end_date} } }
    elif (not start_date) and end_date: # if only end date exists
        date_range_dict = {"range" : {"date" : {"lte" : end_date} } }
    elif start_date and (not end_date): # if only start date exists
        date_range_dict = {"range" : {"date" : {"gte" : start_date} } }
    else:
        date_range_dict = False

    # create amount range dict
    if min_amount and max_amount: # if both min and max amount exist
        amount_range_dict = {"range" : {"amount" : {"from" : min_amount, "to" : max_amount} } }
    elif (not min_amount) and max_amount: # if only max amount exists
        amount_range_dict = {"range" : {"amount" : {"lte" : max_amount} } }
    elif min_amount and (not max_amount): # if only min amount exists
        amount_range_dict = {"range" : {"amount" : {"gte" : min_amount} } }
    else:
        amount_range_dict = False

    # a list with filters
    filters = []
    if date_range_dict:
        filters.append(date_range_dict)
    if amount_range_dict:
        filters.append(amount_range_dict)

    return filters

#the main request route
@app.route('/council_records/<start_date>/<end_date>/<min_amount>/<max_amount>/<search_query>', methods=['GET'])
def council_records(start_date, end_date, min_amount, max_amount, search_query):
    """Returns a respective JSON object when issued a query"""
    """start_date and end_date are strings in format YYYY-MM-DD. Use '0' for blank"""
    """min_amount and max_amount are strings. Use '-1' for blank"""
    """search_query is a string"""

    # generate the body, written in Elastic Search's DSL
    dsl_query = {
        "query" : {
            "filter" : generate_filters(start_date, end_date, min_amount, max_amount)
        }
    }

    # query Elastic Search for appropriate documents with respect to the query
    res = es.search(index=index_name, body = dsl_query)
