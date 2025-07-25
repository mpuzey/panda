import os

# TODO: Consider breaking out constants into separate files for each module

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
PUBLIC_ROOT = os.path.join(ROOT_PATH, 'static')

# Database and Collection Names
MONGODB_DATABASE_NAME = 'panda'
MONGODB_COLLECTION_APPOINTMENTS = 'appointments'
MONGODB_COLLECTION_PATIENTS = 'patients'

# Files
PATIENTS_FILENAME = 'example_patients.json'
APPOINTMENTS_FILENAME = 'example_appointments.json'

# MongoDB 
DEFAULT_MONGODB_URI = 'mongodb://localhost:27017/'
BSON_OBJECT_ID = '_id'

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

# Handler Field Key Names
HANDLER_FIELD_DATABASE_CLIENT = 'database_client'
HANDLER_FIELD_PATIENT_REPOSITORY = 'patient_repository'
HANDLER_FIELD_APPOINTMENT_REPOSITORY = 'appointment_repository'

# Patient Dict Key Names
PATIENT_FIELD_NHS_NUMBER = 'nhs_number'
PATIENT_FIELD_NAME = 'name'
PATIENT_FIELD_DATE_OF_BIRTH = 'date_of_birth'
PATIENT_FIELD_POSTCODE = 'postcode'

# MongoDB Constants
BSON_OBJECT_ID = '_id'

# Appointment Dict Key Names
APPOINTMENT_FIELD_PATIENT = 'patient'
APPOINTMENT_FIELD_STATUS = 'status'
APPOINTMENT_FIELD_TIME = 'time'
APPOINTMENT_FIELD_DURATION = 'duration'
APPOINTMENT_FIELD_CLINICIAN = 'clinician'
APPOINTMENT_FIELD_DEPARTMENT = 'department'
APPOINTMENT_FIELD_ID = 'id'
APPOINTMENT_FIELD_POSTCODE = 'postcode'

# Patient Service Result Field Names
PATIENT_SERVICE_FIELD_ERROR = 'error'
PATIENT_SERVICE_FIELD_VALIDATION_ERRORS = 'errors'
# HTTP status code not to be confused with appointment status
PATIENT_SERVICE_FIELD_STATUS = 'status'
PATIENT_SERVICE_FIELD_MESSAGE = 'message'
PATIENT_SERVICE_FIELD_PATIENT = 'patient'
PATIENT_SERVICE_FIELD_PATIENTS = 'patients'

# Appointment Service Result Field Names
APPOINTMENT_SERVICE_FIELD_ERROR = 'error'
APPOINTMENT_SERVICE_FIELD_VALIDATION_ERRORS = 'errors'
# HTTP status code not to be confused with appointment status
APPOINTMENT_SERVICE_FIELD_STATUS = 'status'
APPOINTMENT_SERVICE_FIELD_MESSAGE = 'message'
APPOINTMENT_SERVICE_FIELD_APPOINTMENT = 'appointment'
APPOINTMENT_SERVICE_FIELD_APPOINTMENTS = 'appointments'

# Response Field Names
PANDA_RESPONSE_FIELD_ERRORS = 'errors'
PANDA_RESPONSE_FIELD_MESSAGE = 'message'
PANDA_RESPONSE_FIELD_PATIENTS = 'patients'
PANDA_RESPONSE_FIELD_APPOINTMENTS = 'appointments'


# Status Values
STATUS_ACTIVE = 'active'
STATUS_ATTENDED = 'attended'
STATUS_CANCELLED = 'cancelled'
STATUS_MISSED = 'missed'

# Regex Patterns
NHS_NUMBER_REGEX = r'^\d{10}$'
DURATION_REGEX = r'^\d+[hm]$'
DATE_FORMAT = '%Y-%m-%d'
UK_POSTCODE_VALIDATION_REGEX = r'^([A-Z][A-HJ-Y]?\d[A-Z\d]? ?\d[A-Z]{2}|GIR ?0A{2})$'



# Error/Message Templates
ERR_PATIENT_NOT_FOUND = 'patient not found'
ERR_APPOINTMENT_NOT_FOUND = 'appointment not found'
ERR_COULD_NOT_CREATE_PATIENT = 'could not create patient'
ERR_COULD_NOT_CREATE_APPOINTMENT = 'could not create appointment'
ERR_COULD_NOT_UPDATE_PATIENT = 'could not update patient'
ERR_COULD_NOT_UPDATE_APPOINTMENT = 'could not update appointment'
MSG_NEW_PATIENT_ADDED = 'new patient added: {}'
MSG_NEW_APPOINTMENT_ADDED = 'new appointment added: {}'
MSG_PATIENT_UPDATED = 'patient updated: {}'
MSG_APPOINTMENT_UPDATED = 'appointment updated: {}'
MSG_PATIENT_DELETED = 'patient deleted: {}'
MSG_APPOINTMENT_CANCELLED = 'appointment cancelled: {}'

# Readable formatting
READABLE_DATE_FORMAT = 'YYYY-MM-DD'

# Error strings
INVALID_DATE_FORMAT_ERROR_TEXT = f'Invalid date format for {PATIENT_FIELD_DATE_OF_BIRTH}. Expected "{READABLE_DATE_FORMAT}"'
INVALID_DATE_OF_BIRTH_ERROR_TEXT = f'Invalid date of birth. Cannot be in the future'
INVALID_UK_POSTCODE_ERROR_TEXT = 'Invalid UK postcode format'
MISSING_REQUIRED_FIELD_ERROR_TEXT = 'Missing required field: {}'
INVALID_NHS_NUMBER_ERROR_TEXT = 'Invalid NHS number. Must be a 10-digit number'
INVALID_NAME_ERROR_TEXT = 'Invalid name. Must be a non-empty string of at least 3 characters'
INVALID_UUID_ERROR_TEXT = f'Invalid UUID format for {{}}'
INVALID_ISO8601_TIME_ERROR_TEXT = f'Invalid ISO 8601 datetime format for {{}}'
INVALID_DURATION_FORMAT_ERROR_TEXT = f'Invalid format for {{}} (expected formats like "1h" or "30m")'
INVALID_STATUS_ERROR_TEXT = f"Invalid '{APPOINTMENT_FIELD_STATUS}' value. Allowed: '{STATUS_ACTIVE}', '{STATUS_ATTENDED}', '{STATUS_CANCELLED}', '{STATUS_MISSED}'"
INVALID_PATIENT_ID_ERROR_TEXT = f'Invalid {APPOINTMENT_FIELD_PATIENT!r} ID. Expected 10-digit number'
INVALID_CLINICIAN_ERROR_TEXT = f'Invalid {APPOINTMENT_FIELD_CLINICIAN!r} value'
INVALID_DEPARTMENT_ERROR_TEXT = f'Invalid {APPOINTMENT_FIELD_DEPARTMENT!r} value'
MISSING_POSTCODE_ERROR_TEXT = f'Missing {APPOINTMENT_FIELD_POSTCODE}'
