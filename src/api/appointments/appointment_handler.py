import json

from src.api.base_handler import BaseHandler
from src.api.appointments.validation import validate
from src.db.mongo import MongoDB
from constants import COLLECTION_APPOINTMENTS, ERR_APPOINTMENT_NOT_FOUND, ERR_COULD_NOT_CREATE_APPOINTMENT, \
    ERR_COULD_NOT_UPDATE_APPOINTMENT, MSG_NEW_APPOINTMENT_ADDED, MSG_APPOINTMENT_UPDATED, MSG_APPOINTMENT_CANCELLED, \
    HTTP_201_CREATED, HTTP_200_OK


class AppointmentHandler(BaseHandler):
    def initialize(self, db_client):
        self.db = MongoDB(db_client, COLLECTION_APPOINTMENTS)

    def get(self, id):
        result = self.db.get({'id': id})
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

    def post(self, _):
        appointment = json.loads(self.request.body)
        errors = validate(appointment)
        if errors:
            self.write_error(400, errors)
            return

        result = self.db.create(appointment)
        if not result.acknowledged:
            self.write({'error': ERR_COULD_NOT_CREATE_APPOINTMENT})
            return

        self.set_status(HTTP_201_CREATED)
        self.write({'message': MSG_NEW_APPOINTMENT_ADDED + appointment.get('id')})

    def put(self, id):
        appointment = json.loads(self.request.body)
        errors = validate(appointment)
        if errors:
            self.write_error(400, errors)
            return

        result =  self.db.update({'id': id}, appointment)
        if not result.acknowledged:
            self.write({'error': ERR_COULD_NOT_UPDATE_APPOINTMENT})
            return

        self.set_status(HTTP_200_OK)
        self.write({'message': MSG_APPOINTMENT_UPDATED + appointment.get('id')})

    def delete(self, id):
        self.db.update({'id': id}, {'status': 'cancelled'})
        self.write({'message': MSG_APPOINTMENT_CANCELLED.format(id)})
