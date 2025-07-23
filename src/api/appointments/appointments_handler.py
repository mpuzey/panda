import json
from src.api.base_handler import BaseHandler
from src.service.appointment_service import AppointmentService
from src.db.mongo import MongoDB
from bson.json_util import dumps as bson_dumps
from constants import MONGODB_COLLECTION_APPOINTMENTS


class AppointmentsHandler(BaseHandler):
    def initialize(self, database_client):
        self.mongo_database = MongoDB(database_client, MONGODB_COLLECTION_APPOINTMENTS)
        self.appointment_service = AppointmentService(self.mongo_database)

    def get(self):
        response = self.appointment_service.get_all_appointments()

        # TODO: Convert BSON objects to JSON for response and move this cleanup to service
        appointments_bson_string = bson_dumps(response['appointments'])
        appointments_json = json.loads(appointments_bson_string)

        self.set_status(response['status'])
        self.write({'appointments': appointments_json})

