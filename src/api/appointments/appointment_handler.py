import json

from src.api.base_handler import BaseHandler
from src.service.appointment_validation import validate
from src.db.mongo import MongoDB
from constants import MONGODB_COLLECTION_APPOINTMENTS, ERR_APPOINTMENT_NOT_FOUND, ERR_COULD_NOT_CREATE_APPOINTMENT, \
    ERR_COULD_NOT_UPDATE_APPOINTMENT, MSG_NEW_APPOINTMENT_ADDED, MSG_APPOINTMENT_UPDATED, MSG_APPOINTMENT_CANCELLED, \
    HTTP_201_CREATED, HTTP_200_OK


class AppointmentHandler(BaseHandler):
    def initialize(self, database_client):
        self.mongo_database = MongoDB(database_client, MONGODB_COLLECTION_APPOINTMENTS)

    def get(self, appointment_id):
        result = self.mongo_database.get({'id': appointment_id})
        if not result:
            self.write({'error': ERR_APPOINTMENT_NOT_FOUND})
            return

        self.write({
            'patient': result.get('patient'),
            'status': result.get('status'),
            'time': result.get('time'),
            'duration': result.get('duration'),
            'clinician': result.get('clinician'),
            'department': result.get('department'),
            'postcode': result.get('postcode'),
            'id': result.get('id')
        })

    def post(self, appointment_id):
        appointment = json.loads(self.request.body)
        errors = validate(appointment)
        if errors:
            self.write_error(400, errors)
            return

        result = self.mongo_database.create(appointment)
        if not result.acknowledged:
            self.write({'error': ERR_COULD_NOT_CREATE_APPOINTMENT})
            return

        self.set_status(HTTP_201_CREATED)
        self.write({'message': MSG_NEW_APPOINTMENT_ADDED.format(appointment_id)})

    def put(self, appointment_id):
        appointment = json.loads(self.request.body)
        errors = validate(appointment)
        if errors:
            self.write_error(400, errors)
            return

        result =  self.mongo_database.update({'id': appointment_id}, appointment)
        if not result.acknowledged:
            self.write({'error': ERR_COULD_NOT_UPDATE_APPOINTMENT})
            return

        self.set_status(HTTP_200_OK)
        self.write({'message': MSG_APPOINTMENT_UPDATED.format(appointment_id)})

    def delete(self, id):
        self.mongo_database.update({'id': id}, {'status': 'cancelled'})
        self.write({'message': MSG_APPOINTMENT_CANCELLED.format(id)})
