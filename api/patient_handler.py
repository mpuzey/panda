import json

from api.base_handler import BaseHandler
from constants import ROOT_PATH, EXAMPLE_PATIENTS_FILENAME
from api.patients.validation import validate


class PatientHandler(BaseHandler):
    def initialize(self):
        with open(ROOT_PATH + EXAMPLE_PATIENTS_FILENAME, 'r') as outfile:
            self.patients = json.load(outfile)

    def get(self, nhs_number):
        for patient in self.patients:
            if patient['nhs_number'] == nhs_number:
                self.write(patient)
                return

    def post(self, _):
        patient = json.loads(self.request.body)
        errors = validate(patient)
        if errors:
            self.write({'errors': errors})
            return

        self.patients.append(patient)
        self.write({'message': 'new patient added:' + json.dumps(patient)})

    def delete(self, nhs_number):
        for i, patient in self.patients:
            if patient['nhs_number'] == nhs_number:
                del self.patients[patient]
                self.write({'message': 'patient' + nhs_number + 'deleted'})
                return
