import json
from src.api.base_handler import BaseHandler
from src.service.appointment_service import AppointmentService
from bson.json_util import dumps as bson_dumps
from constants import MONGODB_COLLECTION_APPOINTMENTS, APPOINTMENT_SERVICE_FIELD_APPOINTMENTS, APPOINTMENT_SERVICE_FIELD_STATUS, PANDA_RESPONSE_FIELD_APPOINTMENTS


class AppointmentsHandler(BaseHandler):
    def initialize(self, database_client):
        self.appointment_service = AppointmentService(database_client)

    def get(self):
        response = self.appointment_service.get_all_appointments()

        # TODO: Convert BSON objects to JSON for response and move this cleanup to service
        appointments_bson_string = bson_dumps(response[APPOINTMENT_SERVICE_FIELD_APPOINTMENTS])
        appointments_json = json.loads(appointments_bson_string)

        self.set_status(response[APPOINTMENT_SERVICE_FIELD_STATUS])
        self.write({PANDA_RESPONSE_FIELD_APPOINTMENTS: appointments_json})

