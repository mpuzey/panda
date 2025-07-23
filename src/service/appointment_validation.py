import re
from datetime import datetime
from uuid import UUID

from constants import UK_POSTCODE_VALIDATION_REGEX, FIELD_PATIENT, FIELD_STATUS, FIELD_TIME, FIELD_DURATION, \
    FIELD_CLINICIAN, FIELD_DEPARTMENT, FIELD_POSTCODE, FIELD_ID, STATUS_ACTIVE, STATUS_ATTENDED, STATUS_CANCELLED, \
    STATUS_MISSED, DURATION_REGEX, NHS_NUMBER_REGEX, DATE_FORMAT, \
    INVALID_UUID_ERROR_TEXT, INVALID_ISO8601_TIME_ERROR_TEXT, INVALID_DURATION_FORMAT_ERROR_TEXT, \
    INVALID_STATUS_ERROR_TEXT, INVALID_PATIENT_ID_ERROR_TEXT, INVALID_CLINICIAN_ERROR_TEXT, INVALID_DEPARTMENT_ERROR_TEXT, \
    MISSING_POSTCODE_ERROR_TEXT, INVALID_UK_POSTCODE_ERROR_TEXT
from src.service.validation_utils import check_required_fields, check_regex, check_min_length, check_date_format


def validate(appointment):
    errors = []
    required_fields = [
        FIELD_PATIENT, FIELD_STATUS, FIELD_TIME, FIELD_DURATION,
        FIELD_CLINICIAN, FIELD_DEPARTMENT, FIELD_POSTCODE, FIELD_ID
    ]
    errors += check_required_fields(appointment, required_fields)
    if errors:
        print('Invalid appointment:', errors)
        return errors
    errors = validate_details(appointment, errors)
    errors = validate_personnel(appointment, errors)
    errors = validate_location(appointment, errors)
    if errors:
        print('Invalid appointment:', errors)
    return errors


def validate_details(appointment, errors):
    if FIELD_ID in appointment:
        try:
            UUID(appointment[FIELD_ID])
        except ValueError:
            errors.append(INVALID_UUID_ERROR_TEXT.format(FIELD_ID))
    if FIELD_TIME in appointment:
        try:
            datetime.fromisoformat(appointment[FIELD_TIME])
        except ValueError:
            errors.append(INVALID_ISO8601_TIME_ERROR_TEXT.format(FIELD_TIME))
    if FIELD_DURATION in appointment:
        errors += check_regex(appointment[FIELD_DURATION],
                              DURATION_REGEX,
                              INVALID_DURATION_FORMAT_ERROR_TEXT.format(FIELD_DURATION))

    if FIELD_STATUS in appointment:
        valid_status_list = [STATUS_ACTIVE, STATUS_ATTENDED, STATUS_CANCELLED, STATUS_MISSED]

        if appointment[FIELD_STATUS] not in valid_status_list:
            errors.append(INVALID_STATUS_ERROR_TEXT)

    return errors


def validate_personnel(appointment, errors):
    if FIELD_PATIENT in appointment:
        errors += check_regex(appointment[FIELD_PATIENT],
                              NHS_NUMBER_REGEX,
                              INVALID_PATIENT_ID_ERROR_TEXT)

    if FIELD_CLINICIAN in appointment:
        errors += check_min_length(appointment[FIELD_CLINICIAN], 3, INVALID_CLINICIAN_ERROR_TEXT)
    return errors


def validate_location(appointment, errors):
    postcode = appointment.get(FIELD_POSTCODE)
    if not postcode:
        errors.append(MISSING_POSTCODE_ERROR_TEXT)
        return errors

    # https://ideal-postcodes.co.uk/guides/uk-postcode-format
    if not re.match(UK_POSTCODE_VALIDATION_REGEX, postcode, re.IGNORECASE):
        errors.append(INVALID_UK_POSTCODE_ERROR_TEXT)

    if FIELD_DEPARTMENT in appointment:
        if not isinstance(appointment[FIELD_DEPARTMENT], str) or not appointment[FIELD_DEPARTMENT]:
            errors.append(INVALID_DEPARTMENT_ERROR_TEXT)

    return errors
