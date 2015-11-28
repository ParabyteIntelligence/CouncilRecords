"""
Copyright (c) Parabyte Intelligence LLC 2015
Author: Micah Thomas

Description: Adds Documents to Mongo & ElasticSearch

"""

import sys
from pymongo import MongoClient
from subprocess import call
import json
from procurement import ProcurementDocument
from elasticsearch import Elasticsearch

DB_NAME = 'council_records'
COLLECTION = 'records'


def new_documents(documents, collection):
    new_docs = []
    for doc in documents:
        if collection.find_one({"item_id": doc["item_id"]}) is None:
            new_docs.append(doc)
    return new_docs


def main(run_new_crawl=True):
    # create instance of procurement doc
    procurement = ProcurementDocument()

    # Call the PhantomJS Crawler
    if run_new_crawl:
        print("INFO: Running Crawler")
        call(["phantomjs", "crawler/get-documents.js"])
        print("INFO: Crawler Finished")

    # Read the JSON into doc_list
    with open('doc-list.json') as data_file:
        print("INFO: Load JSON file output from crawler")
        doc_list = json.load(data_file)

    # Connect to MONGO Instance
    print("INFO: Connecting to MongoDB")
    client = MongoClient()
    db = client[DB_NAME]
    coll = db[COLLECTION]

    # Connect to ES & Create Index
    print("INFO: Connecting to ElasticSearch")
    es = Elasticsearch()
    print("INFO: Checking if {} Index Exists".format(DB_NAME))
    if not es.indices.exists(index=DB_NAME):
        indicies_body = {
            "settings": {
                "number_of_shards": 1,
                "number_of_replicas": 0,
                "analysis": {
                    "analyzer": {
                        "stem": {
                            "tokenizer": "standard",
                            "filter": ["standard", "lowercase", "stop", "porter_stem"]
                        }
                    }
                }
            },
            "mappings": {
                "records": {
                    "properties": {
                        "title": {
                            "type": "string",
                            "analyzer": "stem"
                        },
                        "item_id": {
                            "type": "string",
                            "index": "not_analyzed"
                        },
                        "meeting_id": {
                            "type": "string",
                            "index": "not_analyzed"
                        },
                        "url": {
                            "type": "string",
                            "index": "not_analyzed"
                        },
                        "authorization_date":  {
                            "type": "date",
                            "format": "strict_date_optional_time"
                        },
                        "amount": {
                            "type": "double",
                            "index": "not_analyzed"
                        },
                        "document": {
                            "type": "string",
                            "index": "analyzed",
                            "analyzer": "stem"
                        },
                        "summary": {
                            "type": "string",
                            "index": "not_analyzed",
                        }
                    }
                }
            }
        }
        print("INFO: Creating Index {}".format(DB_NAME))
        es.indices.create(index=DB_NAME, body=indicies_body)

    for doc in new_documents(doc_list, coll):
        parsed_doc = procurement.parse(doc)
        es.create(index=DB_NAME, doc_type=COLLECTION,
                  body=parsed_doc)
        coll.insert_one(parsed_doc)
        print("INFO: Item #{} Added!".format(parsed_doc['item_id']))

    print("INFO: Refreshing Index {}".format(DB_NAME))
    es.indices.refresh(index=DB_NAME)

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "nocrawl":
        main(False)
    else:
        main()
