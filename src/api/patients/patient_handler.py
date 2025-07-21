import json

from src.api.base_handler import BaseHandler
from src.api.patients.validation import validate
from src.db.mongo import MongoDB


class PatientHandler(BaseHandler):
    def initialize(self, db_client):
        self.db = MongoDB(db_client, 'patients')

    def get(self, nhs_number):
        result = self.db.get({'nhs_number': nhs_number})
        if not result:
            self.write({'error': 'patient not found'})
            return

        self.write({
            'nhs_number': result.get('nhs_number'),
            'name': result.get('name'),
            'date_of_birth': result.get('date_of_birth'),
            'postcode': result.get('postcode')
        })
        return

    def post(self, _):
        patient = json.loads(self.request.body)
        errors = validate(patient)
        if errors:
            self.write_error(400, errors)
            return

        result = self.db.create(patient)
        if not result.acknowledged:
            self.write({'error': 'could not create patient'})
            return

        self.write({'message': 'new patient added:' + patient.get('nhs_number')})
        return

    def delete(self, nhs_number):
        self.db.delete({'nhs_number': nhs_number})
        self.write({'message': 'patient' + nhs_number + 'deleted'})
        return
