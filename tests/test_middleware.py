"""
Copyright (c) Parabyte Intelligence LLC 2015
Author: Rakshak Talwar

Description: Tests the API which connects the client to the backend
"""
import datetime
from source.middleware import generate_filters

### generate_filters function ###

def test_generate_filters():
    """ testing the generate_filters function """

    # some test values
    start_date = datetime.datetime(2010, 5, 2)
    end_date = datetime.datetime(2015, 5, 2)
    min_amount = 500.00
    max_amount = 4000000.00
    search_query = "houston first"
    num_hits = 10

    # the filters we're going to test against, the output from the function we're testing should look like this
    test_filters = [
        {"range" : {"authorization_date" : {"from" : start_date, "to" : end_date} } },
        {"range" : {"amount" : {"from" : min_amount, "to" : max_amount} } }
    ]

    # test the function
    assert test_filters == generate_filters(start_date, end_date, min_amount, max_amount)
