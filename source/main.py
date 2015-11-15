"""
Copyright (c) Parabyte Intelligence LLC 2015
Author: Micah Thomas

Description: Adds Documents to Mongo & ElasticSearch

"""

from pymongo import MongoClient
from subprocess import call
import json
from procurement import ProcurementDocument

DB_NAME = 'council_record'
COLLECTION = 'procurement'


def new_documents(documents, collection):
    new_docs = []
    for doc in documents:
        if collection.find_one({"item_id": doc["item_id"]}) is None:
            new_docs.append(doc)
    return new_docs


def main():
    # create instance of procurement doc
    procurement = ProcurementDocument()

    # Call the PhantomJS Crawler
    call(["phantomjs", "phantomjs/get-documents.js"])

    # Parse JSON
    with open('doc-list.json') as data_file:
        doc_list = json.load(data_file)

    # Connect to MONGO Instance
    client = MongoClient()
    db = client[DB_NAME]
    coll = db[COLLECTION]

    # Connect to ES & Create Index
    es = ElasticSearch()
    if not es.indices.exists(index=DB_NAME):
        indicies_body = {
            "settings": {
                "number_of_shards": 1,
                "number_of_replicas": 0
            },
            "mappings": {
                "procurement": {
                    "properties": {
                        "title": {
                            "type": "string"
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
                            "type": "number",
                            "index": "not_analyzed"
                        },
                        "document": {
                            "type": "string",
                            "index": "analyzed"
                        }
                    }
                }
            }
        }
        es.indices.create(index=DB_NAME, body=indicies_body)

    for doc in new_documents(doc_list, coll):
        parsed_doc = procurement.parse(doc)
        print("Parsed Doc: {}".format(parsed_doc))
        coll.insert_one(parsed_doc)
        es.create(index=DB_NAME, doc_type=COLLECTION, body=parsed_doc)
        print "New Item Added: {}".format(parsed_doc['item_id'])

    es.indicies.refresh(index=DB_NAME)

if __name__ == '__main__':
    main()
