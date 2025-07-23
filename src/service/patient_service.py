from constants import (
    ERR_COULD_NOT_CREATE_PATIENT, 
    ERR_COULD_NOT_UPDATE_PATIENT, 
    ERR_PATIENT_NOT_FOUND,
    MSG_NEW_PATIENT_ADDED, 
    MSG_PATIENT_UPDATED, 
    MSG_PATIENT_DELETED,
    HTTP_201_CREATED,
    HTTP_200_OK
)
from src.service.patient_validation import validate


class PatientService:

    def __init__(self, mongo_database):
        self.mongo_database = mongo_database    

    def create_patient(self, patient, nhs_number):
        """Create a new patient with validation."""
        errors = validate(patient)
        if errors:
            return {'status': 400, 'errors': errors}

        result = self.mongo_database.create(patient)
        if not result.acknowledged:
            return {'status': 500, 'error': ERR_COULD_NOT_CREATE_PATIENT}

        return {
            'status': HTTP_201_CREATED,
            'message': MSG_NEW_PATIENT_ADDED.format(nhs_number)
        }


    def update_patient(self, patient, nhs_number):
        """Update an existing patient with validation."""
        errors = validate(patient)
        if errors:
            return {'status': 400, 'errors': errors}

        result = self.mongo_database.update({'nhs_number': nhs_number}, patient)
        if not result.acknowledged:
            return {'status': 500, 'error': ERR_COULD_NOT_UPDATE_PATIENT}

        return {
            'status': HTTP_200_OK,
            'message': MSG_PATIENT_UPDATED.format(nhs_number)
        }


    def get_patient(self, nhs_number):
        """Get a patient by NHS number."""
        result = self.mongo_database.get({'nhs_number': nhs_number})
        if not result:
            return {'status': 404, 'error': ERR_PATIENT_NOT_FOUND}

        return {
            'status': HTTP_200_OK,
            'patient': {
                'nhs_number': result.get('nhs_number'),
                'name': result.get('name'),
                'date_of_birth': result.get('date_of_birth'),
                'postcode': result.get('postcode')
            }
        }


    def delete_patient(self, nhs_number):
        """Delete a patient by NHS number."""
        result = self.mongo_database.delete({'nhs_number': nhs_number})
        if not result.deleted_count:
            return {'status': 404, 'error': ERR_PATIENT_NOT_FOUND}

        return {
            'status': HTTP_200_OK,
            'message': MSG_PATIENT_DELETED.format(nhs_number)
        }

    def get_all_patients(self):
        """Get all patients."""
        patients = self.mongo_database.getAll()
        return {
            'status': HTTP_200_OK,
            'patients': patients
        } 