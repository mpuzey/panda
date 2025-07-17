import os

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
PUBLIC_ROOT = os.path.join(ROOT_PATH, 'static')
EXAMPLE_PATIENTS_FILENAME = '/example_patients.json'
EXAMPLE_APPOINTMENTS_FILENAME = '/example_appointments.json'
UK_POSTCODE_VALIDATION_REGEX = r'^([A-Z][A-HJ-Y]?\d[A-Z\d]? ?\d[A-Z]{2}|GIR ?0A{2})$'

