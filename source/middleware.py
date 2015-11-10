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

#the main request route
@app.route('/council_records/<start_date>/<end_date>/<min_amount>/<max_amount>/<search_query>', methods=['GET'])
def council_records(start_date, end_date, min_amount, max_amount, search_query):
    """Returns a respective JSON object when issued a query"""
    """start_date and end_date are strings in format YYYY-MM-DD. Use '0' for blank"""
    """min_amount and max_amount are strings. Use '-1' for blank"""
    """search_query is a string"""

    # take in query information
    dates = [] # first index will store start_date if it exists; 0 otherwise. Second index will do the same for the end_date
    if start_date != '0':
        dates.insert(0, start_date)
    else:
        dates.insert(0, 0)
    if end_date != '0':
        dates.insert(1, end_date)
    else:
        dates.insert(1, 0)

    amounts = [] # first index will store min_amount if it exists; 0 otherwise. Second index will do the same for the max_amount
    if min_amount != '-1':
        amounts.insert(0, float(min_amount))
    else:
        amounts.insert(0, 0)
    if max_amount != '-1':
        amounts.insert(1, float(max_amount))
    else:
        amounts.insert(1, 0)

    # create date range dict
    if dates[0] and dates[1]: # if both start and end date exist
        date_range_dict = {"range" : {"date" : {"from" : dates[0], "to" : dates[1]} }}
    elif (not dates[0]) and dates[1]: # if only end date exists
        date_range_dict = {"range" : {"date" : {"lte" : dates[1] } } }
    elif dates[0] and (not dates[1]): # if only start date exists
        date_range_dict = {"range" : {"date" : {"gte" : dates[0] } } }
    else:
        date_range_dict = False

    # create amount range dict
    if dates[0] and dates[1]: # if both min and max amount exist
        amount_range_dict = {"range" : {"amount" : {"from" : amounts[0], "to" : amounts[1]} }}
    elif (not dates[0]) and dates[1]: # if only max amount exists
        amount_range_dict = {"range" : {"amount" : {"lte" : amounts[1] } } }
    elif dates[0] and (not dates[1]): # if only min amount exists
        amount_range_dict = {"range" : {"amount" : {"gte" : amounts[0] } } }
    else:
        amount_range_dict = False

    # generate the body, written in Elastic Search's DSL
    dsl_query = {
        "query" : {
            "filter" : [
                date_range_dict,
                amount_range_dict
            ]
        }
    }

    # query Elastic Search for appropriate documents with respect to the query
    res = es.search(index=index_name, body = dsl_query)
