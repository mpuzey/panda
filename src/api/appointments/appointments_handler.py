import json
from src.api.base_handler import BaseHandler
from src.db.mongo import MongoDB
from bson.json_util import dumps as bson_dumps
from constants import MONGODB_COLLECTION_APPOINTMENTS


class AppointmentsHandler(BaseHandler):
    def initialize(self, database_client):
        self.mongo_database = MongoDB(database_client, MONGODB_COLLECTION_APPOINTMENTS)

    def get(self):
        appointments = self.mongo_database.getAll()
        appointments_bson_string = bson_dumps(appointments)
        # TODO: clean up by stripping BSON fields
        appointments_json = json.loads(appointments_bson_string)
        self.write({'appointments': appointments_json})

