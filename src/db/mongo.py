import pymongo


class MongoDB:

    def __init__(self, client, collection):
        # Connect to the MongoDB instance
        self.client = client
        self.db = self.client['panda']
        self.collection = self.db[collection]

    def get(self, query):
        result = self.collection.find_one(query)

        print(result)
        return result

    def create(self, document):
        result = self.collection.insert_one(document)

        print('inserted id' + str(result.inserted_id))
        return result

    def update(self, query, new_values):
        #query = {"name": "John"}
        # new_values = {"$set": {"age": 31}}

        result = self.collection.update_one(query, new_values)

        # Print the number of documents updated
        print(result.modified_count)
        return result

    def delete(self, query):
        result = self.collection.delete_one(query)

        print(result)
        return result
