import re
from datetime import datetime
from uuid import UUID

from constants import (
    UK_POSTCODE_VALIDATION_REGEX,
    APPOINTMENT_FIELD_PATIENT,
    APPOINTMENT_FIELD_STATUS,
    APPOINTMENT_FIELD_TIME,
    APPOINTMENT_FIELD_DURATION,
    APPOINTMENT_FIELD_CLINICIAN,
    APPOINTMENT_FIELD_DEPARTMENT,
    APPOINTMENT_FIELD_POSTCODE,
    APPOINTMENT_FIELD_ID,
    STATUS_ACTIVE,
    STATUS_ATTENDED,
    STATUS_CANCELLED,
    STATUS_MISSED,
    DURATION_REGEX,
    NHS_NUMBER_REGEX,
    DATE_FORMAT,
    INVALID_UUID_ERROR_TEXT,
    INVALID_ISO8601_TIME_ERROR_TEXT,
    INVALID_DURATION_FORMAT_ERROR_TEXT,
    INVALID_STATUS_ERROR_TEXT,
    INVALID_PATIENT_ID_ERROR_TEXT,
    INVALID_CLINICIAN_ERROR_TEXT,
    INVALID_DEPARTMENT_ERROR_TEXT,
    MISSING_POSTCODE_ERROR_TEXT,
    INVALID_UK_POSTCODE_ERROR_TEXT,
)
from src.service.validation_utils import check_required_fields, check_regex, check_min_length, check_date_format, validate_nhs_number_checksum


def validate(appointment):
    errors = []
    required_fields = [
        APPOINTMENT_FIELD_PATIENT, APPOINTMENT_FIELD_STATUS, APPOINTMENT_FIELD_TIME, APPOINTMENT_FIELD_DURATION,
        APPOINTMENT_FIELD_CLINICIAN, APPOINTMENT_FIELD_DEPARTMENT, APPOINTMENT_FIELD_POSTCODE, APPOINTMENT_FIELD_ID
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
    if APPOINTMENT_FIELD_ID in appointment:
        try:
            UUID(appointment[APPOINTMENT_FIELD_ID])
        except ValueError:
            errors.append(INVALID_UUID_ERROR_TEXT.format(APPOINTMENT_FIELD_ID))
    if APPOINTMENT_FIELD_TIME in appointment:
        try:
            datetime.fromisoformat(appointment[APPOINTMENT_FIELD_TIME])
        except ValueError:
            errors.append(INVALID_ISO8601_TIME_ERROR_TEXT.format(APPOINTMENT_FIELD_TIME))
    if APPOINTMENT_FIELD_DURATION in appointment:
        errors += check_regex(appointment[APPOINTMENT_FIELD_DURATION],
                              DURATION_REGEX,
                              INVALID_DURATION_FORMAT_ERROR_TEXT.format(APPOINTMENT_FIELD_DURATION))

    if APPOINTMENT_FIELD_STATUS in appointment:
        valid_status_list = [STATUS_ACTIVE, STATUS_ATTENDED, STATUS_CANCELLED, STATUS_MISSED]

        if appointment[APPOINTMENT_FIELD_STATUS] not in valid_status_list:
            errors.append(INVALID_STATUS_ERROR_TEXT)

    return errors


def validate_personnel(appointment, errors):
    if APPOINTMENT_FIELD_PATIENT in appointment:
        # Validate NHS number format and checksum
        patient_nhs_number = appointment[APPOINTMENT_FIELD_PATIENT]
        if not re.match(NHS_NUMBER_REGEX, patient_nhs_number):
            errors.append(INVALID_PATIENT_ID_ERROR_TEXT)
        elif not validate_nhs_number_checksum(patient_nhs_number):
            errors.append('Invalid NHS number checksum for patient')

    if APPOINTMENT_FIELD_CLINICIAN in appointment:
        errors += check_min_length(appointment[APPOINTMENT_FIELD_CLINICIAN], 3, INVALID_CLINICIAN_ERROR_TEXT)
    return errors


def validate_location(appointment, errors):
    postcode = appointment.get(APPOINTMENT_FIELD_POSTCODE)
    if not postcode:
        errors.append(MISSING_POSTCODE_ERROR_TEXT)
        return errors

    # https://ideal-postcodes.co.uk/guides/uk-postcode-format
    if not re.match(UK_POSTCODE_VALIDATION_REGEX, postcode, re.IGNORECASE):
        errors.append(INVALID_UK_POSTCODE_ERROR_TEXT)

    if APPOINTMENT_FIELD_DEPARTMENT in appointment:
        if not isinstance(appointment[APPOINTMENT_FIELD_DEPARTMENT], str) or not appointment[APPOINTMENT_FIELD_DEPARTMENT]:
            errors.append(INVALID_DEPARTMENT_ERROR_TEXT)

    return errors
