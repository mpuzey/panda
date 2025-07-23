import json

from src.api.base_handler import BaseHandler
from src.service.patient_service import PatientService
from constants import (
    MONGODB_COLLECTION_PATIENTS,
    PATIENT_SERVICE_FIELD_STATUS,
    PANDA_RESPONSE_FIELD_ERROR,
    PATIENT_SERVICE_FIELD_VALIDATION_ERRORS,
    PATIENT_SERVICE_FIELD_ERROR,
    PATIENT_SERVICE_FIELD_MESSAGE,
    PANDA_RESPONSE_FIELD_MESSAGE
)


class PatientHandler(BaseHandler):
    def initialize(self, database_client):
        self.patient_service = PatientService(database_client)

    def get(self, nhs_number):
        response = self.patient_service.get_patient(nhs_number)
        
        error = response.get(PATIENT_SERVICE_FIELD_ERROR)

        if error:
            self.set_status(response[PATIENT_SERVICE_FIELD_STATUS])
            self.write({PANDA_RESPONSE_FIELD_ERROR: error})
            return

        self.set_status(response[PATIENT_SERVICE_FIELD_STATUS])
        self.write(response['patient'])

    def post(self, nhs_number):
        patient = json.loads(self.request.body)
        response = self.patient_service.create_patient(patient, nhs_number)
        
        if PATIENT_SERVICE_FIELD_VALIDATION_ERRORS in response:
            self.write_error(response[PATIENT_SERVICE_FIELD_STATUS], response[PATIENT_SERVICE_FIELD_VALIDATION_ERRORS])
            return

        if PATIENT_SERVICE_FIELD_ERROR in response:
            self.set_status(response[PATIENT_SERVICE_FIELD_STATUS])
            self.write({PANDA_RESPONSE_FIELD_ERROR: response[PATIENT_SERVICE_FIELD_ERROR]})
            return

        self.set_status(response[PATIENT_SERVICE_FIELD_STATUS])
        self.write({PANDA_RESPONSE_FIELD_MESSAGE: response[PATIENT_SERVICE_FIELD_MESSAGE]})

    def put(self, nhs_number):
        patient = json.loads(self.request.body)
        response = self.patient_service.update_patient(patient, nhs_number)

        if PATIENT_SERVICE_FIELD_VALIDATION_ERRORS in response:
            self.write_error(response[PATIENT_SERVICE_FIELD_STATUS], response[PATIENT_SERVICE_FIELD_VALIDATION_ERRORS])
            return

        if PATIENT_SERVICE_FIELD_ERROR in response:
            self.set_status(response[PATIENT_SERVICE_FIELD_STATUS])
            self.write({PANDA_RESPONSE_FIELD_ERROR: response[PATIENT_SERVICE_FIELD_ERROR]})
            return

        self.set_status(response[PATIENT_SERVICE_FIELD_STATUS])
        self.write({PANDA_RESPONSE_FIELD_MESSAGE: response[PATIENT_SERVICE_FIELD_MESSAGE]})

    def delete(self, nhs_number):
        response = self.patient_service.delete_patient(nhs_number)

        if PATIENT_SERVICE_FIELD_ERROR in response:
            self.set_status(response[PATIENT_SERVICE_FIELD_STATUS])
            self.write({PANDA_RESPONSE_FIELD_ERROR: response[PATIENT_SERVICE_FIELD_MESSAGE]})
            return

        self.set_status(response[PATIENT_SERVICE_FIELD_STATUS])
        self.write({PANDA_RESPONSE_FIELD_MESSAGE: response[PATIENT_SERVICE_FIELD_MESSAGE]})
