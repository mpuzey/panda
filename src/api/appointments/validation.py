import re
from datetime import datetime
from uuid import UUID

from constants import UK_POSTCODE_VALIDATION_REGEX, FIELD_PATIENT, FIELD_STATUS, FIELD_TIME, FIELD_DURATION, FIELD_CLINICIAN, FIELD_DEPARTMENT, FIELD_POSTCODE, FIELD_ID, STATUS_ACTIVE, STATUS_ATTENDED, STATUS_CANCELLED, STATUS_MISSED, DURATION_REGEX, NHS_NUMBER_REGEX, DATE_FORMAT
from src.api.validation_utils import check_required_fields, check_regex, check_min_length, check_date_format


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
            errors.append(f'Invalid UUID format for {FIELD_ID!r}')
    if FIELD_TIME in appointment:
        try:
            datetime.fromisoformat(appointment[FIELD_TIME])
        except ValueError:
            errors.append(f'Invalid ISO 8601 datetime format for {FIELD_TIME!r}')
    if FIELD_DURATION in appointment:
        errors += check_regex(appointment[FIELD_DURATION],
                              DURATION_REGEX,
                              f'Invalid format for {FIELD_DURATION!r} (expected formats like "1h" or "30m")')

    if FIELD_STATUS in appointment:
        valid_status_list = [STATUS_ACTIVE, STATUS_ATTENDED, STATUS_CANCELLED, STATUS_MISSED]

        if appointment[FIELD_STATUS] not in valid_status_list:
            errors.append(f'Invalid {FIELD_STATUS!r} value. Allowed: {STATUS_ACTIVE!r}, {STATUS_ATTENDED!r}, \
{STATUS_CANCELLED!r}, {STATUS_MISSED!r}')

    return errors


def validate_personnel(appointment, errors):
    if FIELD_PATIENT in appointment:
        errors += check_regex(appointment[FIELD_PATIENT],
                              NHS_NUMBER_REGEX,
                              f'Invalid {FIELD_PATIENT!r} ID. Expected 10-digit number')

    if FIELD_CLINICIAN in appointment:
        errors += check_min_length(appointment[FIELD_CLINICIAN], 3, f'Invalid {FIELD_CLINICIAN!r} value')
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
