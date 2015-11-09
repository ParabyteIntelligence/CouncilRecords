"""
Copyright (c) Parabyte Intelligence LLC 2015
Author: Rakshak Talwar
Description: Tests the ordinance.py file
"""
from requests.exceptions import *
import pytest
from source.crawler import Crawler

crawler = Crawler();

def test_getDocumentId():

    assert crawler.getDocumentId(1069, 28);

    try:
        crawler.getDocumentId(10000,100000);
    except HTTPError:
        pass
