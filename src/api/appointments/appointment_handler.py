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
        service_result = self.appointment_service.get_appointment(appointment_id)

        if service_result.result_type == ResultType.NOT_FOUND:
            self.set_status(404)
            self.write({PANDA_RESPONSE_FIELD_ERROR: service_result.errors[0]})
            return

        self.set_status(200)
        self.write(service_result.data)

    def post(self, appointment_id):
        appointment = json.loads(self.request.body)
        service_result = self.appointment_service.create_appointment(appointment, appointment_id)

        if service_result.result_type == ResultType.VALIDATION_ERROR:
            self.set_status(400)
            self.write_error(400, service_result.errors)
            return

        if service_result.result_type == ResultType.DATABASE_ERROR:
            self.set_status(500)
            self.write({PANDA_RESPONSE_FIELD_ERROR: service_result.errors[0]})
            return

        self.set_status(201)
        self.write({PANDA_RESPONSE_FIELD_MESSAGE: service_result.message})

    def put(self, appointment_id):
        appointment = json.loads(self.request.body)
        service_result = self.appointment_service.update_appointment(appointment, appointment_id)

        if service_result.result_type == ResultType.VALIDATION_ERROR:
            self.set_status(400)
            self.write_error(400, service_result.errors)
            return

        if service_result.result_type == ResultType.DATABASE_ERROR:
            self.set_status(500)
            self.write({PANDA_RESPONSE_FIELD_ERROR: service_result.errors[0]})
            return

        self.set_status(200)
        self.write({PANDA_RESPONSE_FIELD_MESSAGE: service_result.message})

    def delete(self, appointment_id):
        service_result = self.appointment_service.delete_appointment(appointment_id)

        if service_result.result_type == ResultType.NOT_FOUND:
            self.set_status(404)
            self.write({PANDA_RESPONSE_FIELD_ERROR: service_result.errors[0]})
            return

        self.set_status(200)
        self.write({PANDA_RESPONSE_FIELD_MESSAGE: service_result.message})
