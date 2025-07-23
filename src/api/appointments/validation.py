import re
from datetime import datetime
from uuid import UUID

from constants import UK_POSTCODE_VALIDATION_REGEX, FIELD_PATIENT, FIELD_STATUS, FIELD_TIME, FIELD_DURATION, FIELD_CLINICIAN, FIELD_DEPARTMENT, FIELD_POSTCODE, FIELD_ID, STATUS_ACTIVE, STATUS_ATTENDED, STATUS_CANCELLED, STATUS_MISSED, DURATION_REGEX, NHS_NUMBER_REGEX


def validate(appointment):
    errors = []

    required_fields = [
        FIELD_PATIENT, FIELD_STATUS, FIELD_TIME, FIELD_DURATION,
        FIELD_CLINICIAN, FIELD_DEPARTMENT, FIELD_POSTCODE, FIELD_ID
    ]
    for field in required_fields:
        if field not in appointment or not appointment[field]:
            errors.append(f'Missing required field: {field}')

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
            errors.append(f'Invalid UUID format for {FIELD_ID!r}')

    if FIELD_TIME in appointment:
        try:
            datetime.fromisoformat(appointment[FIELD_TIME])
        except ValueError:
            errors.append(f'Invalid ISO 8601 datetime format for {FIELD_TIME!r}')

    if FIELD_DURATION in appointment:
        if not re.match(DURATION_REGEX, appointment[FIELD_DURATION]):
            errors.append(f'Invalid format for {FIELD_DURATION!r} (expected formats like "1h" or "30m")')

    if FIELD_STATUS in appointment:
        if appointment[FIELD_STATUS] not in [STATUS_ACTIVE, STATUS_ATTENDED, STATUS_CANCELLED, STATUS_MISSED]:
            errors.append(f'Invalid {FIELD_STATUS!r} value. Allowed: {STATUS_ACTIVE!r}, {STATUS_ATTENDED!r}, {STATUS_CANCELLED!r}, {STATUS_MISSED!r}')

    return errors


def validate_personnel(appointment, errors):
    if FIELD_PATIENT in appointment:
        if not re.match(NHS_NUMBER_REGEX, appointment[FIELD_PATIENT]):
            errors.append(f'Invalid {FIELD_PATIENT!r} ID. Expected 10-digit number')

    if FIELD_CLINICIAN in appointment:
        if not isinstance(appointment[FIELD_CLINICIAN], str) or len(appointment[FIELD_CLINICIAN]) < 3:
            errors.append(f'Invalid {FIELD_CLINICIAN!r} value')

    return errors


def validate_location(appointment, errors):
    postcode = appointment.get(FIELD_POSTCODE)
    if not postcode:
        errors.append(f'Missing {FIELD_POSTCODE}')
        return errors

    # https://ideal-postcodes.co.uk/guides/uk-postcode-format
    if not re.match(UK_POSTCODE_VALIDATION_REGEX, postcode, re.IGNORECASE):
        errors.append('Invalid UK postcode format')

    if FIELD_DEPARTMENT in appointment:
        if not isinstance(appointment[FIELD_DEPARTMENT], str) or not appointment[FIELD_DEPARTMENT]:
            errors.append(f'Invalid {FIELD_DEPARTMENT!r} value')

    return errors
