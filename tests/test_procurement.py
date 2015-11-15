"""
Copyright (c) Parabyte Intelligence LLC 2015
Authors: Rakshak Talwar and Micah Thomas

Description: Tests the procurement.py file
"""

import bs4
import datetime
import re
import sys
import requests
from source.procurement import ProcurementDocument

### ProcurementDocument class ###

# predefined url to test
url = 'http://houston.novusagenda.com/agendapublic/Coversheet.aspx?ItemID=5610&MeetingID=126'
# generate a requests object and store the html doc
html_doc = requests.get(url).text

# create class instance
inst = ProcurementDocument()


def test_parse():
    # store variables which would otherwise be provided to the class
    doc = {
        'title': "S25442 Recreational, Educational and Miscellaneous Supplies",
        'item_id': 5610,
        'meeting_id': 126,
        'date': '11/10/2015'
    }
    # body text
    bod = bs4.BeautifulSoup(html_doc, 'lxml').find('body').text.strip()

    # capture data as a python dict from the html document
    data = inst.parse(doc)

    # the dict we will test against
    test_dict = {
        "item_id": 5610,
        "meeting_id": 126,
        "title": doc['title'],
        "amount": 753750.00,
        "authorization_date": datetime.datetime(2015, 11, 10).isoformat(),
        "document": bod
    }

    # testing the class
    assert data['amount'] == test_dict['amount']


def test_find_authorization_date():
    assert inst._find_authorization_date(
        '11/10/2015') == datetime.datetime(2015, 11, 10).isoformat()


def test_find_amount():
    assert inst._find_amount() == 753750.00
