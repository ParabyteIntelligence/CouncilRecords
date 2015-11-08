"""
Copyright (c) Parabyte Intelligence LLC 2015
Author: Rakshak Talwar

Description: Tests the procurement.py file
"""

import bs4, datetime, re, sys
import requests
from source.procurement import ProcurementDocument

### ProcurementDocument class ###

# fixed url to test
url = 'http://houston.novusagenda.com/agendapublic/Coversheet.aspx?ItemID=5610&MeetingID=126'
# generate a requests object and store the html doc
html_doc = requests.get(url).text

# create class instance
inst = ProcurementDocument()

def test_to_dict():
    # title
    title = "S25442 Recreational, Educational and Miscellaneous Supplies"
    # body text
    bod = bs4.BeautifulSoup(html_doc, 'lxml').find('body').text.strip()

    # capture data as a python dict from the html document
    data = inst.to_dict(title, html_doc)

    # the dict we will test against
    test_dict = {
            "title" : title,
            "amount" : 753750.00,
            "authorization_date" : datetime.date(2015, 11, 10),
            "document_date" : datetime.date(2015, 10, 22),
            "document" : bod
    }

    #testing the class
    assert data == test_dict

def test_find_document_date():
    assert inst._find_document_date() == datetime.date(2015, 10, 22)

def test_find_authorization_date():
    assert inst._find_authorization_date() == datetime.date(2015, 11, 10)

def test_find_amount():
    assert inst._find_amount() == 753750.00
