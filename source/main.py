from pymongo import MongoClient
from subprocess import call
import json

DB_NAME = 'council_records'
COLLECTION = 'procurements'

def new_documents(documents, collection):
    new_docs = []
    for doc in documents:
        if collection.find_one({"item_id": doc["item_id"]}) is None:
            new_docs.append(doc)
    return new_docs

def main():
    # Call the PhantomJS Crawler
    call(["phantomjs", "phantomjs/get-documents.js"])

    # Parse JSON
    with open('doc-list.json') as data_file:
        doc_list = json.load(data_file)

    # Connect to MONGO Instance
    client = MongoClient()
    db = client[DB_NAME]
    coll = db[COLLECTION]

    for doc in new_documents(doc_list, coll):
        print doc
        # parsed_doc = procurement.parse(doc)
        # coll.insert_one(parsed_doc)

if __name__ == '__main__':
    main()
