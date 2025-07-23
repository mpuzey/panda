from src.db.mongo import MongoDB

from constants import (
    ERR_COULD_NOT_CREATE_PATIENT,
    ERR_COULD_NOT_UPDATE_PATIENT,
    ERR_PATIENT_NOT_FOUND,
    MSG_NEW_PATIENT_ADDED,
    MSG_PATIENT_UPDATED,
    MSG_PATIENT_DELETED,
    HTTP_201_CREATED,
    HTTP_200_OK,
    PATIENT_SERVICE_FIELD_ERROR,
    PATIENT_SERVICE_FIELD_VALIDATION_ERRORS,
    PATIENT_SERVICE_FIELD_STATUS,
    PATIENT_SERVICE_FIELD_MESSAGE,
    PATIENT_SERVICE_FIELD_PATIENT,
    PATIENT_SERVICE_FIELD_PATIENTS,
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
            return {PATIENT_SERVICE_FIELD_STATUS: 400, PATIENT_SERVICE_FIELD_VALIDATION_ERRORS: errors}

        result = self.mongo_database.create(patient)
        if not result.acknowledged:
            return {PATIENT_SERVICE_FIELD_STATUS: 500, PATIENT_SERVICE_FIELD_ERROR: ERR_COULD_NOT_CREATE_PATIENT}

        return {
            PATIENT_SERVICE_FIELD_STATUS: HTTP_201_CREATED,
            PATIENT_SERVICE_FIELD_MESSAGE: MSG_NEW_PATIENT_ADDED.format(nhs_number)
        }

    def update_patient(self, patient, nhs_number):
        """Update an existing patient with validation."""
        errors = validate(patient)
        if errors:
            return {PATIENT_SERVICE_FIELD_STATUS: 400, PATIENT_SERVICE_FIELD_VALIDATION_ERRORS: errors}

        result = self.mongo_database.update({PATIENT_FIELD_NHS_NUMBER: nhs_number}, patient)
        if not result.acknowledged:
            return {PATIENT_SERVICE_FIELD_STATUS: 500, PATIENT_SERVICE_FIELD_ERROR: ERR_COULD_NOT_UPDATE_PATIENT}

        return {
            PATIENT_SERVICE_FIELD_STATUS: HTTP_200_OK,
            PATIENT_SERVICE_FIELD_MESSAGE: MSG_PATIENT_UPDATED.format(nhs_number)
        }

    def get_patient(self, nhs_number):
        """Get a patient by NHS number."""
        result = self.mongo_database.get({PATIENT_FIELD_NHS_NUMBER: nhs_number})
        if not result:
            return {PATIENT_SERVICE_FIELD_STATUS: 404, PATIENT_SERVICE_FIELD_ERROR: ERR_PATIENT_NOT_FOUND}

        return {
            PATIENT_SERVICE_FIELD_STATUS: HTTP_200_OK,
            PATIENT_SERVICE_FIELD_PATIENT: {
                # TODO: add constants for fields for both PANDA response and result fields
                'nhs_number': result.get('nhs_number'),
                'name': result.get('name'),
                'date_of_birth': result.get('date_of_birth'),
                'postcode': result.get('postcode')
            }
        }

    def delete_patient(self, nhs_number):
        """Delete a patient by NHS number."""
        result = self.mongo_database.delete({PATIENT_FIELD_NHS_NUMBER: nhs_number})
        # TODO: should this be a 200 aka an idempotent delete response?
        if not result.deleted_count:
            return {PATIENT_SERVICE_FIELD_STATUS: 500, PATIENT_SERVICE_FIELD_ERROR: ERR_PATIENT_NOT_FOUND}

        return {
            PATIENT_SERVICE_FIELD_STATUS: HTTP_200_OK,
            PATIENT_SERVICE_FIELD_MESSAGE: MSG_PATIENT_DELETED.format(nhs_number)
        }

    def get_all_patients(self):
        """Get all patients."""
        patients = self.mongo_database.getAll()
        return {
            PATIENT_SERVICE_FIELD_STATUS: HTTP_200_OK,
            PATIENT_SERVICE_FIELD_PATIENTS: patients
        }
