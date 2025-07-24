from src.api.base_handler import BaseHandler
from src.service.patient_service import PatientService
from constants import (
    PANDA_RESPONSE_FIELD_PATIENTS
)


class PatientsHandler(BaseHandler):
    def initialize(self, patient_repository):
        """Initialize handler with injected patient repository.

        Args:
            patient_repository: Repository instance for patient data access
        """
        self.patient_service = PatientService(patient_repository)

    def get(self):
        service_response = self.patient_service.get_all_patients()

        self.set_status(200)
        self.write({PANDA_RESPONSE_FIELD_PATIENTS: service_response.data})
