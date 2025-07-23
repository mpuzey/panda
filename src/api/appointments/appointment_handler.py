import json

from src.api.base_handler import BaseHandler
from src.service.appointment_service import AppointmentService
from src.db.mongo import MongoDB
from constants import MONGODB_COLLECTION_APPOINTMENTS


class AppointmentHandler(BaseHandler):
    def initialize(self, database_client):
        self.mongo_database = MongoDB(database_client, MONGODB_COLLECTION_APPOINTMENTS)
        self.appointment_service = AppointmentService(self.mongo_database)

    def get(self, appointment_id):
        response = self.appointment_service.get_appointment(appointment_id)

        if 'error' in response:
            self.set_status(response['status'])
            self.write({'error': response['error']})
            return

        self.set_status(response['status'])
        self.write(response['appointment'])

    def post(self, appointment_id):
        appointment = json.loads(self.request.body)
        response = self.appointment_service.create_appointment(appointment, appointment_id)

        if 'errors' in response:
            self.write_error(response['status'], response['errors'])
            return

        if 'error' in response:
            self.set_status(response['status'])
            self.write({'error': response['error']})
            return

        self.set_status(response['status'])
        self.write({'message': response['message']})

    def put(self, appointment_id):
        appointment = json.loads(self.request.body)
        response = self.appointment_service.update_appointment(appointment, appointment_id)

        if 'errors' in response:
            self.write_error(response['status'], response['errors'])
            return

        if 'error' in response:
            self.set_status(response['status'])
            self.write({'error': response['error']})
            return

        self.set_status(response['status'])
        self.write({'message': response['message']})

    def delete(self, appointment_id):
        response = self.appointment_service.delete_appointment(appointment_id)

        if 'error' in response:
            self.set_status(response['status'])
            self.write({'error': response['error']})
            return

        self.set_status(response['status'])
        self.write({'message': response['message']})
