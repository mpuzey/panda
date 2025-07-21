import json

from src.api.base_handler import BaseHandler
from constants import ROOT_PATH, EXAMPLE_PATIENTS_FILENAME


class PatientsHandler(BaseHandler):
    def initialize(self):
        with open(ROOT_PATH + EXAMPLE_PATIENTS_FILENAME, 'r') as outfile:
            self.patients = json.load(outfile)

    def get(self):
        self.write({'patients': self.patients})

