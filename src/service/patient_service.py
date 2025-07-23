from src.db.mongo import MongoDB
from src.service.results import ServiceResult, ResultType

from constants import (
    ERR_COULD_NOT_CREATE_PATIENT,
    ERR_COULD_NOT_UPDATE_PATIENT,
    ERR_PATIENT_NOT_FOUND,
    MSG_NEW_PATIENT_ADDED,
    MSG_PATIENT_UPDATED,
    MSG_PATIENT_DELETED,
    PATIENT_FIELD_NHS_NUMBER,
    MONGODB_COLLECTION_PATIENTS
)
from src.service.patient_validation import validate


class PatientService:

    def __init__(self, mongo_database_client):
        self.mongo_database = MongoDB(mongo_database_client, MONGODB_COLLECTION_PATIENTS)

    def create_patient(self, patient, nhs_number):
        """Create a new patient with validation."""
        errors = validate(patient)
        if errors:
            return ServiceResult(ResultType.VALIDATION_ERROR, errors=errors)

        result = self.mongo_database.create(patient)
        if not result.acknowledged:
            return ServiceResult(ResultType.DATABASE_ERROR, errors=[ERR_COULD_NOT_CREATE_PATIENT])

        return ServiceResult(
            ResultType.SUCCESS,
            message=MSG_NEW_PATIENT_ADDED.format(nhs_number)
        )

    def update_patient(self, patient, nhs_number):
        """Update an existing patient with validation."""
        errors = validate(patient)
        if errors:
            return ServiceResult(ResultType.VALIDATION_ERROR, errors=errors)

        result = self.mongo_database.update({PATIENT_FIELD_NHS_NUMBER: nhs_number}, patient)
        if not result.acknowledged:
            return ServiceResult(ResultType.DATABASE_ERROR, errors=[ERR_COULD_NOT_UPDATE_PATIENT])

        return ServiceResult(
            ResultType.SUCCESS,
            message=MSG_PATIENT_UPDATED.format(nhs_number)
        )

    def get_patient(self, nhs_number):
        """Get a patient by NHS number."""
        result = self.mongo_database.get({PATIENT_FIELD_NHS_NUMBER: nhs_number})
        if not result:
            return ServiceResult(ResultType.NOT_FOUND, errors=[ERR_PATIENT_NOT_FOUND])

        return ServiceResult(
            ResultType.SUCCESS,
            data={
                'nhs_number': result.get('nhs_number'),
                'name': result.get('name'),
                'date_of_birth': result.get('date_of_birth'),
                'postcode': result.get('postcode')
            }
        )

    def delete_patient(self, nhs_number):
        """Delete a patient by NHS number."""
        result = self.mongo_database.delete({PATIENT_FIELD_NHS_NUMBER: nhs_number})
        if not result.deleted_count:
            return ServiceResult(ResultType.NOT_FOUND, errors=[ERR_PATIENT_NOT_FOUND])

        return ServiceResult(
            ResultType.SUCCESS,
            message=MSG_PATIENT_DELETED.format(nhs_number)
        )

    def get_all_patients(self):
        """Get all patients."""
        patients = self.mongo_database.getAll()
        return ServiceResult(ResultType.SUCCESS, data=patients)
