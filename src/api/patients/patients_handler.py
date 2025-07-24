import json
from src.api.base_handler import BaseHandler
from src.service.patient_service import PatientService
from src.service.results import ResultType
from bson.json_util import dumps as bson_dumps
from constants import (
    PANDA_RESPONSE_FIELD_PATIENTS
)


class PatientsHandler(BaseHandler):
    def initialize(self, database_client):
        self.patient_service = PatientService(database_client)

    def get(self):
        service_result = self.patient_service.get_all_patients()

        # TODO: Convert BSON objects to JSON for response and move this cleanup to mongo layer
        patients_bson_string = bson_dumps(service_result.data)
        patients_json = json.loads(patients_bson_string)

        self.set_status(200)
        self.write({PANDA_RESPONSE_FIELD_PATIENTS: patients_json})
