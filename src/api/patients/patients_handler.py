import json
from src.api.base_handler import BaseHandler
from src.db.mongo import MongoDB
from bson.json_util import dumps as bson_dumps


class PatientsHandler(BaseHandler):
    def initialize(self, db_client):
        self.db = MongoDB(db_client, 'patients')

    def get(self):
        patients = self.db.getAll()
        patients_bson_string = bson_dumps(patients)
        # TODO: clean up by stripping bson fields
        patients_json = json.loads(patients_bson_string)
        self.write({'patients': patients_json})
