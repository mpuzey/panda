import json
import logging
import pymongo
from bson.json_util import dumps as bson_dumps
from constants import MONGODB_DATABASE_NAME, BSON_OBJECT_ID, MONGODB_SET_OPERATOR, MONGODB_UNKNOWN_ID


class MongoDB:

    def __init__(self, client, collection_name):
        # Connect to the MongoDB instance
        self.client = client
        self.db = self.client[MONGODB_DATABASE_NAME]
        self.collection = self.db[collection_name]
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self.collection_name = collection_name

    def _convert_bson_to_json(self, bson_data):
        """Convert BSON objects to JSON-serializable dictionaries.
        
        Args:
            bson_data: BSON data from MongoDB
            
        Returns:
            JSON-serializable dictionary or None
        """
        if bson_data is None:
            return None
        
        # Convert BSON to JSON string then back to dict to handle ObjectId and other BSON types
        bson_string = bson_dumps(bson_data)
        json_data = json.loads(bson_string)

        if BSON_OBJECT_ID in json_data:
            del json_data[BSON_OBJECT_ID]

        return json_data

    def get(self, query):
        self.logger.debug(f"Querying {self.collection_name} with: {query}")
        result = self.collection.find_one(query)
        
        if result:
            self.logger.debug(f"Found document in {self.collection_name}: {result.get(BSON_OBJECT_ID, MONGODB_UNKNOWN_ID)}")
        else:
            self.logger.debug(f"No document found in {self.collection_name} matching query: {query}")
            
        return self._convert_bson_to_json(result)

    def getAll(self):
        self.logger.debug(f"Retrieving all documents from {self.collection_name}")
        cursor = self.collection.find()
        collection_documents = []
        for document in cursor:
            collection_documents.append(self._convert_bson_to_json(document))

        self.logger.info(f"Retrieved {len(collection_documents)} documents from {self.collection_name}")
        return collection_documents

    def create(self, document):
        self.logger.debug(f"Creating document in {self.collection_name}")
        result = self.collection.insert_one(document)

        if result.acknowledged:
            self.logger.info(f"Successfully created document in {self.collection_name} with id: {result.inserted_id}")
        else:
            self.logger.error(f"Failed to create document in {self.collection_name}")
            
        return result

    def update(self, query, updated_values):
        self.logger.debug(f"Updating document in {self.collection_name} with query: {query}")
        new_values = {MONGODB_SET_OPERATOR: updated_values}

        result = self.collection.update_one(query, new_values)

        if result.acknowledged:
            if result.modified_count > 0:
                self.logger.info(f"Successfully updated {result.modified_count} document(s) in {self.collection_name}")
            else:
                self.logger.warning(f"Update query matched {result.matched_count} document(s) in {self.collection_name} but no changes were made")
        else:
            self.logger.error(f"Failed to update document in {self.collection_name}")
            
        return result

    def delete(self, query):
        self.logger.debug(f"Deleting document from {self.collection_name} with query: {query}")
        result = self.collection.delete_one(query)

        if result.acknowledged:
            if result.deleted_count > 0:
                self.logger.info(f"Successfully deleted {result.deleted_count} document(s) from {self.collection_name}")
            else:
                self.logger.warning(f"No documents found to delete in {self.collection_name} matching query: {query}")
        else:
            self.logger.error(f"Failed to delete document from {self.collection_name}")
            
        return result
