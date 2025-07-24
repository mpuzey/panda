import json

from src.api.base_handler import BaseHandler
from src.service.appointment_service import AppointmentService
from src.service.results import ResponseType
from constants import (
    PANDA_RESPONSE_FIELD_ERROR,
    PANDA_RESPONSE_FIELD_ERRORS,
    PANDA_RESPONSE_FIELD_MESSAGE,
)


class AppointmentHandler(BaseHandler):
    def initialize(self, appointment_repository):
        """Initialize handler with injected appointment repository.

        Args:
            appointment_repository: Repository instance for appointment data access
        """
        self.appointment_service = AppointmentService(appointment_repository)

    def get(self, appointment_id):
        service_response = self.appointment_service.get_appointment(appointment_id)

        if service_response.response_type == ResponseType.NOT_FOUND:
            self.set_status(404)
            self.write({PANDA_RESPONSE_FIELD_ERROR: service_response.errors[0]})
            return

        self.set_status(200)
        self.write(service_response.data)

    def post(self, appointment_id):
        appointment = json.loads(self.request.body)
        service_response = self.appointment_service.create_appointment(appointment, appointment_id)

        # TODO: Consolidate "error" and "errors" response fields into just "errors"
        if service_response.response_type == ResponseType.VALIDATION_ERROR:
            self.set_status(400)
            self.write({PANDA_RESPONSE_FIELD_ERRORS: service_response.errors})
            return

        if service_response.response_type == ResponseType.BUSINESS_ERROR:
            self.set_status(400)
            self.write({PANDA_RESPONSE_FIELD_ERROR: service_response.errors[0]})
            return

        if service_response.response_type == ResponseType.DATABASE_ERROR:
            self.set_status(500)
            self.write({PANDA_RESPONSE_FIELD_ERROR: service_response.errors[0]})
            return

        self.set_status(201)
        self.write({PANDA_RESPONSE_FIELD_MESSAGE: service_response.message})

    def put(self, appointment_id):
        appointment = json.loads(self.request.body)
        service_response = self.appointment_service.update_appointment(appointment, appointment_id)

        if service_response.response_type == ResponseType.VALIDATION_ERROR:
            self.set_status(400)
            self.write({PANDA_RESPONSE_FIELD_ERRORS: service_response.errors})
            return

        if service_response.response_type == ResponseType.BUSINESS_ERROR:
            self.set_status(400)
            self.write({PANDA_RESPONSE_FIELD_ERROR: service_response.errors[0]})
            return

        if service_response.response_type == ResponseType.DATABASE_ERROR:
            self.set_status(500)
            self.write({PANDA_RESPONSE_FIELD_ERROR: service_response.errors[0]})
            return

        self.set_status(200)
        self.write({PANDA_RESPONSE_FIELD_MESSAGE: service_response.message})

    def delete(self, appointment_id):
        service_response = self.appointment_service.delete_appointment(appointment_id)

        if service_response.response_type == ResponseType.NOT_FOUND:
            self.set_status(404)
            self.write({PANDA_RESPONSE_FIELD_ERROR: service_response.errors[0]})
            return

        self.set_status(200)
        self.write({PANDA_RESPONSE_FIELD_MESSAGE: service_response.message})
