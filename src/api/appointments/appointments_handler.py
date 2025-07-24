import json
from src.api.base_handler import BaseHandler
from src.service.appointment_service import AppointmentService
from src.service.results import ResultType
from bson.json_util import dumps as bson_dumps
from constants import (
    PANDA_RESPONSE_FIELD_APPOINTMENTS,
)


class AppointmentsHandler(BaseHandler):
    def initialize(self, database_client):
        self.appointment_service = AppointmentService(database_client)

    def get(self):
        response = self.appointment_service.get_all_appointments()

        # TODO: Convert BSON objects to JSON for response and move this cleanup to service
        appointments_bson_string = bson_dumps(response.data)
        appointments_json = json.loads(appointments_bson_string)

        self.set_status(200)
        self.write({PANDA_RESPONSE_FIELD_APPOINTMENTS: appointments_json})

