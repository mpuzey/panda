import json

import pymongo


class MongoDB:

    def __init__(self, client, collection_name):
        # Connect to the MongoDB instance
        self.client = client
        self.db = self.client['panda']
        self.collection = self.db[collection_name]

    def get(self, query):
        result = self.collection.find_one(query)

        print(result)
        return result

    def getAll(self):
        cursor = self.collection.find()
        collection_documents = []
        for document in cursor:
            collection_documents.append(document)

        print(collection_documents)
        return collection_documents

    def create(self, document):
        result = self.collection.insert_one(document)

        print('inserted id' + str(result.inserted_id))
        return result

    def update(self, query, new_values):
        # query = {"name": "John"}
        # new_values = {"$set": {"age": 31}}

        result = self.collection.update_one(query, new_values)

        # Print the number of documents updated
        print(result.modified_count)
        return result

    def delete(self, query):
        result = self.collection.delete_one(query)

        print(result)
        return result
