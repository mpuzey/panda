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
            translated_errors = self.translate_errors(service_result.errors)
            self.write({PANDA_RESPONSE_FIELD_ERROR: translated_errors[0]})
            return

        self.set_status(200)
        self.write(service_result.data)

    def post(self, nhs_number):
        patient = json.loads(self.request.body)
        service_result = self.patient_service.create_patient(patient, nhs_number)
        
        if service_result.result_type == ResultType.VALIDATION_ERROR:
            self.set_status(400)
            translated_errors = self.translate_errors(service_result.errors)
            self.write_error(400, translated_errors)
            return

        if service_result.result_type == ResultType.DATABASE_ERROR:
            self.set_status(500)
            translated_errors = self.translate_errors(service_result.errors)
            self.write({PANDA_RESPONSE_FIELD_ERROR: translated_errors[0]})
            return

        self.set_status(201)
        translated_message = self.translate_message(service_result.message['key'], **service_result.message['params'])
        self.write({PANDA_RESPONSE_FIELD_MESSAGE: translated_message})

    def put(self, nhs_number):
        patient = json.loads(self.request.body)
        service_result = self.patient_service.update_patient(patient, nhs_number)

        if service_result.result_type == ResultType.VALIDATION_ERROR:
            self.set_status(400)
            translated_errors = self.translate_errors(service_result.errors)
            self.write_error(400, translated_errors)
            return

        if service_result.result_type == ResultType.DATABASE_ERROR:
            self.set_status(500)
            translated_errors = self.translate_errors(service_result.errors)
            self.write({PANDA_RESPONSE_FIELD_ERROR: translated_errors[0]})
            return

        self.set_status(200)
        translated_message = self.translate_message(service_result.message['key'], **service_result.message['params'])
        self.write({PANDA_RESPONSE_FIELD_MESSAGE: translated_message})

    def delete(self, nhs_number):
        service_result = self.patient_service.delete_patient(nhs_number)

        if service_result.result_type == ResultType.NOT_FOUND:
            self.set_status(404)
            translated_errors = self.translate_errors(service_result.errors)
            self.write({PANDA_RESPONSE_FIELD_ERROR: translated_errors[0]})
            return

        self.set_status(200)
        translated_message = self.translate_message(service_result.message['key'], **service_result.message['params'])
        self.write({PANDA_RESPONSE_FIELD_MESSAGE: translated_message})
