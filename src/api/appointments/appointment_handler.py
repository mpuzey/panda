import json

from src.api.base_handler import BaseHandler
from src.service.appointment_service import AppointmentService
from constants import (
    APPOINTMENT_FIELD_STATUS,
    PANDA_RESPONSE_FIELD_ERROR,
    PANDA_RESPONSE_FIELD_MESSAGE,
    APPOINTMENT_SERVICE_FIELD_VALIDATION_ERRORS,
    APPOINTMENT_SERVICE_FIELD_ERROR,
    APPOINTMENT_SERVICE_FIELD_STATUS,
    APPOINTMENT_SERVICE_FIELD_MESSAGE,
)


class AppointmentHandler(BaseHandler):
    def initialize(self, database_client):
        self.appointment_service = AppointmentService(database_client)

    def get(self, appointment_id):
        response = self.appointment_service.get_appointment(appointment_id)

        error = response.get(APPOINTMENT_SERVICE_FIELD_ERROR)

        if error:
            self.set_status(response[APPOINTMENT_SERVICE_FIELD_STATUS])
            self.write({PANDA_RESPONSE_FIELD_ERROR: error})
            return

        self.set_status(response[APPOINTMENT_SERVICE_FIELD_STATUS])
        self.write(response['appointment'])

    def post(self, appointment_id):
        appointment = json.loads(self.request.body)
        response = self.appointment_service.create_appointment(appointment, appointment_id)

        if APPOINTMENT_SERVICE_FIELD_VALIDATION_ERRORS in response:
            self.write_error(response[APPOINTMENT_SERVICE_FIELD_STATUS], response[APPOINTMENT_SERVICE_FIELD_VALIDATION_ERRORS])
            return

        if APPOINTMENT_SERVICE_FIELD_ERROR in response:
            self.set_status(response[APPOINTMENT_SERVICE_FIELD_STATUS])
            self.write({PANDA_RESPONSE_FIELD_ERROR: response[APPOINTMENT_SERVICE_FIELD_ERROR]})
            return

        self.set_status(response[APPOINTMENT_SERVICE_FIELD_STATUS])
        self.write({PANDA_RESPONSE_FIELD_MESSAGE: response[APPOINTMENT_SERVICE_FIELD_MESSAGE]})

    def put(self, appointment_id):
        appointment = json.loads(self.request.body)
        response = self.appointment_service.update_appointment(appointment, appointment_id)

        if 'errors' in response:
            self.write_error(response[APPOINTMENT_SERVICE_FIELD_STATUS], response[APPOINTMENT_SERVICE_FIELD_VALIDATION_ERRORS])
            return

        if 'error' in response:
            self.set_status(response[APPOINTMENT_SERVICE_FIELD_STATUS])
            self.write({PANDA_RESPONSE_FIELD_ERROR: response[APPOINTMENT_SERVICE_FIELD_ERROR]})
            return

        self.set_status(response['status'])
        self.write({PANDA_RESPONSE_FIELD_MESSAGE: response[APPOINTMENT_SERVICE_FIELD_MESSAGE]})

    def delete(self, appointment_id):
        response = self.appointment_service.delete_appointment(appointment_id)

        if 'error' in response:
            self.set_status(response[APPOINTMENT_SERVICE_FIELD_STATUS])
            self.write({PANDA_RESPONSE_FIELD_ERROR: response[APPOINTMENT_SERVICE_FIELD_MESSAGE]})
            return

        self.set_status(response[APPOINTMENT_FIELD_STATUS])
        self.write({PANDA_RESPONSE_FIELD_MESSAGE: response[APPOINTMENT_SERVICE_FIELD_MESSAGE]})
