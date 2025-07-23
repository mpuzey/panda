import json
from src.api.base_handler import BaseHandler
from src.db.mongo import MongoDB
from bson.json_util import dumps as bson_dumps
from constants import MONGODB_COLLECTION_PATIENTS


class PatientsHandler(BaseHandler):
    def initialize(self, database_client):
        self.mongo_database = MongoDB(database_client, MONGODB_COLLECTION_PATIENTS)

    def get(self):
        patients = self.mongo_database.getAll()
        patients_bson_string = bson_dumps(patients)
        # TODO: clean up by stripping bson fields
        patients_json = json.loads(patients_bson_string)
        self.write({'patients': patients_json})
