import json

from src.api.base_handler import BaseHandler
from src.api.appointments.validation import validate
from src.db.mongo import MongoDB


class AppointmentHandler(BaseHandler):
    def initialize(self, db_client):
        self.db = MongoDB(db_client, 'appointments')

    def get(self, id):
        result = self.db.get({'id': id})
        if not result:
            self.write({'error': 'appointment not found'})
            return

        self.write({'patient': result.get('patient'),
                    'status': result.get('status'),
                    'time': result.get('time'),
                    'duration': result.get('duration'),
                    'clinician': result.get('clinician'),
                    'department': result.get('department'),
                    'postcode': result.get('postcode'),
                    'id': result.get('id')
                    })

    def post(self, _):
        appointment = json.loads(self.request.body)
        errors = validate(appointment)
        if errors:
            self.write_error(400, errors)
            return

        result = self.db.create(appointment)
        if not result.acknowledged:
            self.write({'error': 'could not create appointment'})
            return

        self.write({'message': 'new appointment added:' + appointment.get('id')})

    def delete(self, id):
        self.db.update({'id': id}, {'status': 'cancelled'})
        self.write({'message': 'appointment' + id + 'cancelled'})
