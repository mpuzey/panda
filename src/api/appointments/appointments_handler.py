import json
from src.api.base_handler import BaseHandler
from src.db.mongo import MongoDB
from bson.json_util import dumps as bson_dumps


class AppointmentsHandler(BaseHandler):
    def initialize(self, db_client):
        self.db = MongoDB(db_client, 'appointments')

    def get(self):
        appointments = self.db.getAll()
        appointments_bson_string = bson_dumps(appointments)
        # TODO: clean up by stripping bson fields
        appointments_json = json.loads(appointments_bson_string)
        self.write({'appointments': appointments_json})

