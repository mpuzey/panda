import json

from src.api.base_handler import BaseHandler
from src.service.patient_service import PatientService
from src.db.mongo import MongoDB
from constants import MONGODB_COLLECTION_PATIENTS


class PatientHandler(BaseHandler):
    def initialize(self, database_client):
        self.mongo_database = MongoDB(database_client, MONGODB_COLLECTION_PATIENTS)
        self.patient_service = PatientService(self.mongo_database)

    def get(self, nhs_number):
        response = self.patient_service.get_patient(nhs_number)
        
        if 'error' in response:
            self.set_status(response['status'])
            self.write({'error': response['error']})
        else:
            self.set_status(response['status'])
            self.write(response['patient'])

    def post(self, nhs_number):
        patient = json.loads(self.request.body)
        response = self.patient_service.create_patient(patient, nhs_number)
        
        if 'errors' in response:
            self.write_error(response['status'], response['errors'])
        elif 'error' in response:
            self.set_status(response['status'])
            self.write({'error': response['error']})
        else:
            self.set_status(response['status'])
            self.write({'message': response['message']})

    def put(self, nhs_number):
        patient = json.loads(self.request.body)
        response = self.patient_service.update_patient(patient, nhs_number)

        if 'errors' in response:
            self.write_error(response['status'], response['errors'])
            return

        if 'error' in response:
            self.set_status(response['status'])
            self.write({'error': response['error']})
            return

        self.set_status(response['status'])
        self.write({'message': response['message']})

    def delete(self, nhs_number):
        response = self.patient_service.delete_patient(nhs_number)

        if 'error' in response:
            self.set_status(response['status'])
            self.write({'error': response['error']})
            return

        self.set_status(response['status'])
        self.write({'message': response['message']})
