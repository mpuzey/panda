import json

from src.api.base_handler import BaseHandler
from constants import ROOT_PATH, EXAMPLE_APPOINTMENTS_FILENAME


class AppointmentsHandler(BaseHandler):
    def initialize(self):
        with open(ROOT_PATH + EXAMPLE_APPOINTMENTS_FILENAME, 'r') as outfile:
            self.appointments = json.load(outfile)

    def get(self):
        self.write({'appointments': self.appointments})
