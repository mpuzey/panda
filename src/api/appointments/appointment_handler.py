import json

from src.api.base_handler import BaseHandler
from constants import ROOT_PATH, EXAMPLE_APPOINTMENTS_FILENAME
from src.api.appointments.validation import validate


class AppointmentHandler(BaseHandler):
    def initialize(self, db_client):
        with open(ROOT_PATH + EXAMPLE_APPOINTMENTS_FILENAME, 'r') as outfile:
            self.appointments = json.load(outfile)

    def get(self, id):
        for appointment in self.appointments:
            if appointment['id'] == id:
                self.write(appointment)
                return

    def post(self, _):
        appointment = json.loads(self.request.body)
        errors = validate(appointment)
        if errors:
            self.write({'errors': errors})
            return

        self.appointments.append(appointment)
        self.write({'message': 'new appointment added:' + json.dumps(appointment)})

    def delete(self, id):
        for appointment in self.appointments:
            if appointment['id'] == id:
                del self.appointments[appointment]
                self.write({'message': 'appointment' + id + 'deleted'})
                return
