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

# some global variables
index_names = ['councilrec']
type_names = ['recs']

# create elasticsearch client instance
es = Elasticsearch()

def generate_filters(start_date, end_date, min_amount, max_amount):
    """ Generates a list of filters for use in the Elastic Search query """

    # create date range dict
    if start_date and end_date: # if both start and end date exist
        date_range_dict = {"range" : {"date" : {"from" : start_date, "to" : end_date} } }
    elif (not start_date) and end_date: # if only end date exists
        date_range_dict = {"range" : {"date" : {"lte" : end_date} } }
    elif start_date and (not end_date): # if only start date exists
        date_range_dict = {"range" : {"date" : {"gte" : start_date} } }
    else:
        date_range_dict = None

    # create amount range dict
    if min_amount and max_amount: # if both min and max amount exist
        amount_range_dict = {"range" : {"amount" : {"from" : min_amount, "to" : max_amount} } }
    elif (not min_amount) and max_amount: # if only max amount exists
        amount_range_dict = {"range" : {"amount" : {"lte" : max_amount} } }
    elif min_amount and (not max_amount): # if only min amount exists
        amount_range_dict = {"range" : {"amount" : {"gte" : min_amount} } }
    else:
        amount_range_dict = None

    # a list with filters
    filters = []
    if date_range_dict:
        filters.append(date_range_dict)
    if amount_range_dict:
        filters.append(amount_range_dict)

    return filters

#the main request route
@app.route('/search', methods=['GET'])
def council_records():
    """Returns a respective JSON object when issued a query"""
    """start_date and end_date are dates"""
    """min_amount and max_amount are floats"""
    """search_query is a string"""

    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    min_amount = request.args.get('min_amount')
    max_amount = request.args.get('max_amount')
    search_query = request.args.get('search_query')
    num_hits = request.args.get('num_hits') if request.args.get('num_hits') else 10

    # generate the body, written in Elastic Search's DSL
    dsl_query = {
        "query" : {
            "filtered" : {
                "query" : {"match" : {"_all" : search_query}},
                "filter" : generate_filters(start_date, end_date, min_amount, max_amount)
            }
        }
    }

    # query Elastic Search for appropriate documents with respect to the query
    res = es.search(index=index_names, doc_type=type_names, body = dsl_query, size=num_hits)

    # return the hits
    return jsonify(res['hits'])

if __name__ == "__main__":
    app.run(port=9099, debug=True)
