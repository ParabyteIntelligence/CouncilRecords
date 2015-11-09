"""
Copyright (c) Parabyte Intelligence LLC 2015
Author: Micah Thomas
Description: Crawler for Council Records
"""
import requests
import re
from bs4 import BeautifulSoup

class Crawler():
    """

    """

    def __init__(self):
        self.not_document_agenda = re.compile(r".*This Agenda is not available.*")
        self.items_id = "ctl00_ContentPlaceHolder1_SearchAgendasMeetings_radGridItems_ctl00"

    def getDocumentId(self, item_id, meeting_id):
        """
        Get the Document with a unique Id

        @return {string} Html Document
        """
        document_baseurl = 'http://houston.novusagenda.com/agendapublic/Coversheet.aspx'
        payload = {
            "ItemID": item_id,
            "MeetingID": meeting_id
        }

        r = requests.get(document_baseurl, params=payload);

        r.raise_for_status()

        if self.not_document_agenda.match(r.text):
            raise Exception("Agenda Doesn't Exist")

        return r.text

    def getListOfProcurmentsFromPage(self, page):
        """
        Get the List of All Purchases from single page
        """
        page.find("table", _class="rgMasterTable", id=)

    def getPageFromRecords(self):

        soup = BeautifulSoup(html_doc, 'lxml')
