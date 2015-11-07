"""
Copyright (c) Parabyte Intelligence LLC 2015
Author: Micah Thomas

Description:
Crawler gets new Documents from CouncilRecords
"""

import pymongo
import requests
import time

DOCUMENT_DATE_START_FROM =  

class Crawler():
    """
    Crawler gets new Documents from CouncilRecords
    """
    def getNewDocuments():
        """
        Query the CouncilRecords & Only Return the new Documents
        @return Array of {
            "item_id": Unique Id of the Document,
            "meeting_id": Id of the Meeting,
            "url": Url of the Document
        }
        """
