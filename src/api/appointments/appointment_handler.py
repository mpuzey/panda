import json

from src.api.base_handler import BaseHandler
from src.service.appointment_service import AppointmentService
from src.service.results import ResultType
from constants import (
    PANDA_RESPONSE_FIELD_ERROR,
    PANDA_RESPONSE_FIELD_MESSAGE,
)


class AppointmentHandler(BaseHandler):
    def initialize(self, database_client):
        self.appointment_service = AppointmentService(database_client)

    def get(self, appointment_id):
        response = self.appointment_service.get_appointment(appointment_id)

        if response.result_type == ResultType.NOT_FOUND:
            self.set_status(404)
            self.write({PANDA_RESPONSE_FIELD_ERROR: response.errors[0]})
            return

        if response.result_type == ResultType.SUCCESS:
            self.set_status(200)
            self.write(response.data)
            return

    def post(self, appointment_id):
        appointment = json.loads(self.request.body)
        response = self.appointment_service.create_appointment(appointment, appointment_id)

        if response.result_type == ResultType.VALIDATION_ERROR:
            self.set_status(400)
            self.write_error(400, response.errors)
            return

        if response.result_type == ResultType.DATABASE_ERROR:
            self.set_status(500)
            self.write({PANDA_RESPONSE_FIELD_ERROR: response.errors[0]})
            return

        if response.result_type == ResultType.SUCCESS:
            self.set_status(201)
            self.write({PANDA_RESPONSE_FIELD_MESSAGE: response.message})
            return

    def put(self, appointment_id):
        appointment = json.loads(self.request.body)
        response = self.appointment_service.update_appointment(appointment, appointment_id)

        if response.result_type == ResultType.VALIDATION_ERROR:
            self.set_status(400)
            self.write_error(400, response.errors)
            return

        if response.result_type == ResultType.DATABASE_ERROR:
            self.set_status(500)
            self.write({PANDA_RESPONSE_FIELD_ERROR: response.errors[0]})
            return

        if response.result_type == ResultType.SUCCESS:
            self.set_status(200)
            self.write({PANDA_RESPONSE_FIELD_MESSAGE: response.message})
            return

    def delete(self, appointment_id):
        response = self.appointment_service.delete_appointment(appointment_id)

        if response.result_type == ResultType.NOT_FOUND:
            self.set_status(404)
            self.write({PANDA_RESPONSE_FIELD_ERROR: response.errors[0]})
            return

        if response.result_type == ResultType.SUCCESS:
            self.set_status(200)
            self.write({PANDA_RESPONSE_FIELD_MESSAGE: response.message})
            return
