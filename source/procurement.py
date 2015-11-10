"""
Copyright (c) Parabyte Intelligence LLC 2015
Author: Rakshak Talwar and Micah Thomas

Description: Defines a class which parses procurement documents for relevant information
"""

import datetime
import pdb
import re
import bs4
import requests


class ProcurementDocument():
    """Pass in a url, title, meeting_id, and item_id for a City Council procurement. Returns a Python dictionary with procurement information."""

    def __init__(self):

        # dict template
        self.data_dict = {
            "item_id": int(),
            "meeting_id": int(),
            "title": str(),
            # use regex to find any number starting with a $ and grab the
            # biggest number since it's total
            "amount": float(),
            "authorization_date": datetime.datetime(2000, 1, 1),
            "document_date": datetime.datetime(2000, 1, 1),
            "document": str(),  # entire body tag
            "url": str()
        }

    def parse(self, doc):
        """ This is the main method which is called to return the Python dictionary based on
        the procurement page's title, item_id, meeting_id, and url"""

        url = "http://houston.novusagenda.com/agendapublic/Coversheet.aspx?ItemID={0}&MeetingID={1}".format(
            doc['item_id'], doc['meeting_id'])

        # create beautifulsoup4 object from url
        self.html_doc = requests.get(url).text
        self.soup = bs4.BeautifulSoup(self.html_doc, 'lxml')

        # store the passed in values
        return {
            'title': doc['title'],
            'item_id': doc['item_id'],
            'meeting_id': doc['meeting_id'],
            'url': url,
            "amount": self._find_amount(),
            "authorization_date": self._find_authorization_date(doc['date']),
            "document": self._find_document()
        }

    def _find_authorization_date(self, doc_date):
        """Returns the document's creation date as a python datetime object"""

        date_ls = doc_date.split('/')
        year, month, day = int(date_ls[2]), int(date_ls[0]), int(date_ls[1])

        return datetime.datetime(year, month, day)  # return date object

    def _find_amount(self):
        """Finds the greatest dollar amount in the entire document"""

        pattern = re.compile('(\$(\d*\,){0,}\d{1,3}\.\d{2})')
        items = re.findall(pattern, self.soup.text)
        amounts = []
        for tup in items:
            a1 = tup[0].replace('$', '')
            a1 = a1.replace(',', '')
            amounts.append(float(a1))
        sorted_amounts = sorted(amounts)
        return sorted_amounts[-1]

    def _find_document(self):
        """Finds the visible text inside of the document"""

        texts = self.soup.findAll(text=True)
        visible_texts = filter(ProcurementDocument._visible_text, texts)

        return " ".join(visible_texts)

    @staticmethod
    def _visible_text(element):
        """Filter for Visible Text"""
        if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
            return False
        elif re.match(r'<!--.*-->', element):
            return False
        return True
