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
            translated_errors = self.translate_errors(service_result.errors)
            self.write({PANDA_RESPONSE_FIELD_ERROR: translated_errors[0]})
            return

        self.set_status(200)
        self.write(service_result.data)

    def post(self, appointment_id):
        appointment = json.loads(self.request.body)
        service_result = self.appointment_service.create_appointment(appointment, appointment_id)

        # TODO: Consolidate "error" and "errors" response fields into just "errors"
        if service_result.result_type == ResultType.VALIDATION_ERROR:
            self.set_status(400)
            translated_errors = self.translate_errors(service_result.errors)
            self.write_error(400, translated_errors)
            return

        if service_result.result_type == ResultType.BUSINESS_ERROR:
            self.set_status(400)
            translated_errors = self.translate_errors(service_result.errors)
            self.write({PANDA_RESPONSE_FIELD_ERROR: translated_errors[0]})
            return

        if service_result.result_type == ResultType.DATABASE_ERROR:
            self.set_status(500)
            translated_errors = self.translate_errors(service_result.errors)
            self.write({PANDA_RESPONSE_FIELD_ERROR: translated_errors[0]})
            return

        self.set_status(201)
        translated_message = self.translate_message(service_result.message['key'], **service_result.message['params'])
        self.write({PANDA_RESPONSE_FIELD_MESSAGE: translated_message})

    def put(self, appointment_id):
        appointment = json.loads(self.request.body)
        service_result = self.appointment_service.update_appointment(appointment, appointment_id)

        if service_result.result_type == ResultType.VALIDATION_ERROR:
            self.set_status(400)
            translated_errors = self.translate_errors(service_result.errors)
            self.write_error(400, translated_errors)
            return

        if service_result.result_type == ResultType.BUSINESS_ERROR:
            self.set_status(400)
            translated_errors = self.translate_errors(service_result.errors)
            self.write({PANDA_RESPONSE_FIELD_ERROR: translated_errors[0]})
            return

        if service_result.result_type == ResultType.DATABASE_ERROR:
            self.set_status(500)
            translated_errors = self.translate_errors(service_result.errors)
            self.write({PANDA_RESPONSE_FIELD_ERROR: translated_errors[0]})
            return

        self.set_status(200)
        translated_message = self.translate_message(service_result.message['key'], **service_result.message['params'])
        self.write({PANDA_RESPONSE_FIELD_MESSAGE: translated_message})

    def delete(self, appointment_id):
        service_result = self.appointment_service.delete_appointment(appointment_id)

        if service_result.result_type == ResultType.NOT_FOUND:
            self.set_status(404)
            translated_errors = self.translate_errors(service_result.errors)
            self.write({PANDA_RESPONSE_FIELD_ERROR: translated_errors[0]})
            return

        self.set_status(200)
        translated_message = self.translate_message(service_result.message['key'], **service_result.message['params'])
        self.write({PANDA_RESPONSE_FIELD_MESSAGE: translated_message})
