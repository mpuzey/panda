from src.repository.patient import PatientRepository
from src.service.results import ServiceResponse, ResponseType

from constants import (
    ERR_COULD_NOT_CREATE_PATIENT,
    ERR_COULD_NOT_UPDATE_PATIENT,
    ERR_PATIENT_NOT_FOUND,
    MSG_NEW_PATIENT_ADDED,
    MSG_PATIENT_UPDATED,
    MSG_PATIENT_DELETED,
)
from src.service.patient_validation import validate


class PatientService:

    def __init__(self, patient_repository: PatientRepository):
        """Initialize PatientService with a patient repository.

        Args:
            patient_repository: Repository instance for patient data access
        """
        self.patient_repository = patient_repository

    def create_patient(self, patient, nhs_number):
        """Create a new patient with validation."""
        errors = validate(patient)
        if errors:
            return ServiceResponse(ResponseType.VALIDATION_ERROR, errors=errors)

        success = self.patient_repository.create(patient)
        if not success:
            return ServiceResponse(ResponseType.DATABASE_ERROR, errors=[ERR_COULD_NOT_CREATE_PATIENT])

        return ServiceResponse(
            ResponseType.SUCCESS,
            message=MSG_NEW_PATIENT_ADDED.format(nhs_number)
        )

    def update_patient(self, patient, nhs_number):
        """Update an existing patient with validation."""
        errors = validate(patient)
        if errors:
            return ServiceResponse(ResponseType.VALIDATION_ERROR, errors=errors)

        success = self.patient_repository.update_by_nhs_number(nhs_number, patient)
        if not success:
            return ServiceResponse(ResponseType.DATABASE_ERROR, errors=[ERR_COULD_NOT_UPDATE_PATIENT])

        return ServiceResponse(
            ResponseType.SUCCESS,
            message=MSG_PATIENT_UPDATED.format(nhs_number)
        )

    def get_patient(self, nhs_number):
        """Get a patient by NHS number."""
        patient_data = self.patient_repository.get_by_nhs_number(nhs_number)
        if not patient_data:
            return ServiceResponse(ResponseType.NOT_FOUND, errors=[ERR_PATIENT_NOT_FOUND])

        return ServiceResponse(ResponseType.SUCCESS, data=patient_data)

    def delete_patient(self, nhs_number):
        """Delete a patient by NHS number."""
        success = self.patient_repository.delete_by_nhs_number(nhs_number)
        if not success:
            return ServiceResponse(ResponseType.NOT_FOUND, errors=[ERR_PATIENT_NOT_FOUND])

        return ServiceResponse(
            ResponseType.SUCCESS,
            message=MSG_PATIENT_DELETED.format(nhs_number)
        )

    def get_all_patients(self):
        """Get all patients."""
        patients = self.patient_repository.get_all()
        return ServiceResponse(ResponseType.SUCCESS, data=patients)
