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

# Handler Field Key Names
HANDLER_FIELD_DATABASE_CLIENT = 'database_client'

# Patient Dict Key Names
PATIENT_FIELD_NHS_NUMBER = 'nhs_number'
PATIENT_FIELD_NAME = 'name'
PATIENT_FIELD_DATE_OF_BIRTH = 'date_of_birth'
PATIENT_FIELD_POSTCODE = 'postcode'

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

# PANDA Response Field Names
PANDA_RESPONSE_FIELD_ERROR = 'error'
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



# Message Keys for localisation
ERR_PATIENT_NOT_FOUND = 'patient_not_found'
ERR_APPOINTMENT_NOT_FOUND = 'appointment_not_found'
ERR_COULD_NOT_CREATE_PATIENT = 'could_not_create_patient'
ERR_COULD_NOT_CREATE_APPOINTMENT = 'could_not_create_appointment'
ERR_COULD_NOT_UPDATE_PATIENT = 'could_not_update_patient'
ERR_COULD_NOT_UPDATE_APPOINTMENT = 'could_not_update_appointment'
MSG_NEW_PATIENT_ADDED = 'new_patient_added'
MSG_NEW_APPOINTMENT_ADDED = 'new_appointment_added'
MSG_PATIENT_UPDATED = 'patient_updated'
MSG_APPOINTMENT_UPDATED = 'appointment_updated'
MSG_PATIENT_DELETED = 'patient_deleted'
MSG_APPOINTMENT_CANCELLED = 'appointment_cancelled'

# Readable formatting
READABLE_DATE_FORMAT = 'YYYY-MM-DD'

# Error Message Keys for localisation
INVALID_DATE_FORMAT_ERROR_TEXT = 'invalid_date_format'
INVALID_DATE_OF_BIRTH_ERROR_TEXT = 'invalid_date_of_birth'
INVALID_UK_POSTCODE_ERROR_TEXT = 'invalid_uk_postcode'
MISSING_REQUIRED_FIELD_ERROR_TEXT = 'missing_required_field'
INVALID_NHS_NUMBER_ERROR_TEXT = 'invalid_nhs_number'
INVALID_NHS_NUMBER_CHECKSUM_ERROR_TEXT = 'invalid_nhs_number_checksum'
INVALID_NHS_NUMBER_CHECKSUM_PATIENT_ERROR_TEXT = 'invalid_nhs_number_checksum_patient'
INVALID_NAME_ERROR_TEXT = 'invalid_name'
INVALID_UUID_ERROR_TEXT = 'invalid_uuid'
INVALID_ISO8601_TIME_ERROR_TEXT = 'invalid_iso8601_time'
INVALID_DURATION_FORMAT_ERROR_TEXT = 'invalid_duration_format'
INVALID_STATUS_ERROR_TEXT = 'invalid_status'
INVALID_PATIENT_ID_ERROR_TEXT = 'invalid_patient_id'
INVALID_CLINICIAN_ERROR_TEXT = 'invalid_clinician'
INVALID_DEPARTMENT_ERROR_TEXT = 'invalid_department'
MISSING_POSTCODE_ERROR_TEXT = 'missing_postcode'
