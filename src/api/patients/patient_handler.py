import json

from src.api.base_handler import BaseHandler
from src.api.patients.validation import validate
from src.db.mongo import MongoDB
from constants import MONGODB_COLLECTION_PATIENTS, ERR_PATIENT_NOT_FOUND, ERR_COULD_NOT_CREATE_PATIENT,  \
    ERR_COULD_NOT_UPDATE_PATIENT, MSG_NEW_PATIENT_ADDED, MSG_PATIENT_UPDATED, MSG_PATIENT_DELETED, HTTP_201_CREATED,  \
    HTTP_200_OK


class PatientHandler(BaseHandler):
    def initialize(self, database_client):
        self.mongo_database = MongoDB(database_client, MONGODB_COLLECTION_PATIENTS)

    def get(self, nhs_number):
        result = self.mongo_database.get({'nhs_number': nhs_number})
        if not result:
            self.write({'error': ERR_PATIENT_NOT_FOUND})
            return

        self.write({
            'nhs_number': result.get('nhs_number'),
            'name': result.get('name'),
            'date_of_birth': result.get('date_of_birth'),
            'postcode': result.get('postcode')
        })

    def post(self, _):
        patient = json.loads(self.request.body)
        errors = validate(patient)
        if errors:
            self.write_error(400, errors)
            return

        result = self.mongo_database.create(patient)
        if not result.acknowledged:
            self.write({'error': ERR_COULD_NOT_CREATE_PATIENT})
            return

        self.set_status(HTTP_201_CREATED)
        self.write({'message': MSG_NEW_PATIENT_ADDED + patient.get('nhs_number')})

    def put(self, nhs_number):
        patient = json.loads(self.request.body)
        errors = validate(patient)
        if errors:
            self.write_error(400, errors)
            return

        result = self.mongo_database.update({'nhs_number': nhs_number}, patient)
        if not result.acknowledged:
            self.write({'error': ERR_COULD_NOT_UPDATE_PATIENT})
            return

        self.set_status(HTTP_200_OK)
        self.write({'message': MSG_PATIENT_UPDATED + patient.get('nhs_number')})

    def delete(self, nhs_number):
        self.mongo_database.delete({'nhs_number': nhs_number})
        self.write({'message': MSG_PATIENT_DELETED.format(nhs_number)})
