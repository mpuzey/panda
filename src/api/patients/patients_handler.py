import json
from src.api.base_handler import BaseHandler
from src.service.patient_service import PatientService
from src.db.mongo import MongoDB
from bson.json_util import dumps as bson_dumps
from constants import MONGODB_COLLECTION_PATIENTS


class PatientsHandler(BaseHandler):
    def initialize(self, database_client):
        self.mongo_database = MongoDB(database_client, MONGODB_COLLECTION_PATIENTS)
        self.patient_service = PatientService(self.mongo_database)

    def get(self):
        response = self.patient_service.get_all_patients()

        # TODO: Convert BSON objects to JSON for response and move this cleanup to service
        patients_bson_string = bson_dumps(response['patients'])
        patients_json = json.loads(patients_bson_string)

        self.set_status(response['status'])
        self.write({'patients': patients_json})
