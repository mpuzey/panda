import json

from src.api.base_handler import BaseHandler
from src.service.patient_service import PatientService
from src.service.results import ResponseType
from constants import (
    PANDA_RESPONSE_FIELD_ERRORS,
    PANDA_RESPONSE_FIELD_MESSAGE,
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR
)


class PatientHandler(BaseHandler):
    def initialize(self, patient_repository):
        """Initialize handler with injected patient repository.
        Args:
            patient_repository: Repository instance for patient data access
        """
        self.patient_service = PatientService(patient_repository)

    def get(self, nhs_number):
        """Get a patient by NHS number."""
        service_response = self.patient_service.get_patient(nhs_number)
        
        if service_response.response_type == ResponseType.NOT_FOUND:
            self.set_status(HTTP_404_NOT_FOUND)
            self.write({PANDA_RESPONSE_FIELD_ERRORS: service_response.errors})
            return

        self.set_status(HTTP_200_OK)
        self.write(service_response.data)

    def post(self, nhs_number):
        """Create a new patient with the given NHS number."""
        patient = json.loads(self.request.body)
        service_response = self.patient_service.create_patient(patient, nhs_number)
        
        if service_response.response_type == ResponseType.VALIDATION_ERROR:
            self.set_status(HTTP_400_BAD_REQUEST)
            self.write({PANDA_RESPONSE_FIELD_ERRORS: service_response.errors})
            return

        if service_response.response_type == ResponseType.DATABASE_ERROR:
            self.set_status(HTTP_500_INTERNAL_SERVER_ERROR)
            self.write({PANDA_RESPONSE_FIELD_ERRORS: service_response.errors})
            return

        self.set_status(HTTP_201_CREATED)
        self.write({PANDA_RESPONSE_FIELD_MESSAGE: service_response.message})

    def put(self, nhs_number):
        """Update an existing patient by NHS number."""
        patient = json.loads(self.request.body)
        service_response = self.patient_service.update_patient(patient, nhs_number)

        if service_response.response_type == ResponseType.VALIDATION_ERROR:
            self.set_status(HTTP_400_BAD_REQUEST)
            self.write({PANDA_RESPONSE_FIELD_ERRORS: service_response.errors})
            return

        if service_response.response_type == ResponseType.DATABASE_ERROR:
            self.set_status(HTTP_500_INTERNAL_SERVER_ERROR)
            self.write({PANDA_RESPONSE_FIELD_ERRORS: service_response.errors})
            return

        self.set_status(HTTP_200_OK)
        self.write({PANDA_RESPONSE_FIELD_MESSAGE: service_response.message})

    def delete(self, nhs_number):
        """Delete a patient by NHS number."""
        service_response = self.patient_service.delete_patient(nhs_number)

        if service_response.response_type == ResponseType.NOT_FOUND:
            self.set_status(HTTP_404_NOT_FOUND)
            self.write({PANDA_RESPONSE_FIELD_ERRORS: service_response.errors})
            return

        self.set_status(HTTP_200_OK)
        self.write({PANDA_RESPONSE_FIELD_MESSAGE: service_response.message})
