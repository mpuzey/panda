import os

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
PUBLIC_ROOT = os.path.join(ROOT_PATH, 'static')

UK_POSTCODE_VALIDATION_REGEX = r'^([A-Z][A-HJ-Y]?\d[A-Z\d]? ?\d[A-Z]{2}|GIR ?0A{2})$'

# Database and Collection Names
DB_NAME = 'panda'
COLLECTION_APPOINTMENTS = 'appointments'
COLLECTION_PATIENTS = 'patients'

# Files
PATIENTS_FILENAME = 'example_patients.json'
APPOINTMENTS_FILENAME = 'example_appointments.json'

# MongoDB URI
DEFAULT_MONGODB_URI = 'mongodb://localhost:27017/'

# HTTP Status Codes
HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_204_NO_CONTENT = 204
HTTP_400_BAD_REQUEST = 400

# HTTP Header Names and Values
HEADER_ALLOW_ORIGIN = 'Access-Control-Allow-Origin'
HEADER_ALLOW_HEADERS = 'Access-Control-Allow-Headers'
HEADER_ALLOW_METHODS = 'Access-Control-Allow-Methods'
HEADER_ALLOW_ORIGIN_VALUE = '*'
HEADER_ALLOW_HEADERS_VALUE = (
    'x-requested-with,'
    'access-control-allow-headers,'
    'cache-control,'
    'content-type,'
    'pragma'
)
HEADER_ALLOW_METHODS_VALUE = 'GET, OPTIONS'

# Field Names
FIELD_NHS_NUMBER = 'nhs_number'
FIELD_NAME = 'name'
FIELD_DATE_OF_BIRTH = 'date_of_birth'
FIELD_POSTCODE = 'postcode'
FIELD_PATIENT = 'patient'
FIELD_STATUS = 'status'
FIELD_TIME = 'time'
FIELD_DURATION = 'duration'
FIELD_CLINICIAN = 'clinician'
FIELD_DEPARTMENT = 'department'
FIELD_ID = 'id'

# Status Values
STATUS_ACTIVE = 'active'
STATUS_ATTENDED = 'attended'
STATUS_CANCELLED = 'cancelled'
STATUS_MISSED = 'missed'

# Regex Patterns
NHS_NUMBER_REGEX = r'^\d{10}$'
DURATION_REGEX = r'^\d+[hm]$'
DATE_FORMAT = '%Y-%m-%d'

# Error/Message Templates
ERR_PATIENT_NOT_FOUND = 'patient not found'
ERR_APPOINTMENT_NOT_FOUND = 'appointment not found'
ERR_COULD_NOT_CREATE_PATIENT = 'could not create patient'
ERR_COULD_NOT_CREATE_APPOINTMENT = 'could not create appointment'
ERR_COULD_NOT_UPDATE_PATIENT = 'could not update patient'
ERR_COULD_NOT_UPDATE_APPOINTMENT = 'could not update appointment'
MSG_NEW_PATIENT_ADDED = 'new patient added: '
MSG_NEW_APPOINTMENT_ADDED = 'new appointment added: '
MSG_PATIENT_UPDATED = 'patient updated: '
MSG_APPOINTMENT_UPDATED = 'appointment updated: '
MSG_PATIENT_DELETED = 'patient {} deleted'
MSG_APPOINTMENT_CANCELLED = 'appointment {} cancelled'
