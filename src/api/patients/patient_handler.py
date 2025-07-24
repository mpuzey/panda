import json

from src.api.base_handler import BaseHandler
from src.service.patient_service import PatientService
from src.service.results import ResultType
from constants import (
    PANDA_RESPONSE_FIELD_ERROR,
    PANDA_RESPONSE_FIELD_MESSAGE
)


class PatientHandler(BaseHandler):
    def initialize(self, database_client):
        self.patient_service = PatientService(database_client)

    def get(self, nhs_number):
        service_result = self.patient_service.get_patient(nhs_number)
        
        if service_result.result_type == ResultType.NOT_FOUND:
            self.set_status(404)
            self.write({PANDA_RESPONSE_FIELD_ERROR: service_result.errors[0]})
            return

        self.set_status(200)
        self.write(service_result.data)

    def post(self, nhs_number):
        patient = json.loads(self.request.body)
        service_result = self.patient_service.create_patient(patient, nhs_number)
        
        if service_result.result_type == ResultType.VALIDATION_ERROR:
            self.set_status(400)
            self.write_error(400, service_result.errors)
            return

        if service_result.result_type == ResultType.DATABASE_ERROR:
            self.set_status(500)
            self.write({PANDA_RESPONSE_FIELD_ERROR: service_result.errors[0]})
            return

        self.set_status(201)
        self.write({PANDA_RESPONSE_FIELD_MESSAGE: service_result.message})

    def put(self, nhs_number):
        patient = json.loads(self.request.body)
        service_result = self.patient_service.update_patient(patient, nhs_number)

        if service_result.result_type == ResultType.VALIDATION_ERROR:
            self.set_status(400)
            self.write_error(400, service_result.errors)
            return

        if service_result.result_type == ResultType.DATABASE_ERROR:
            self.set_status(500)
            self.write({PANDA_RESPONSE_FIELD_ERROR: service_result.errors[0]})
            return

        self.set_status(200)
        self.write({PANDA_RESPONSE_FIELD_MESSAGE: service_result.message})

    def delete(self, nhs_number):
        service_result = self.patient_service.delete_patient(nhs_number)

        if service_result.result_type == ResultType.NOT_FOUND:
            self.set_status(404)
            self.write({PANDA_RESPONSE_FIELD_ERROR: service_result.errors[0]})
            return

        self.set_status(200)
        self.write({PANDA_RESPONSE_FIELD_MESSAGE: service_result.message})
