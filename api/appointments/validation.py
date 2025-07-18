import re
from datetime import datetime
from uuid import UUID

from constants import UK_POSTCODE_VALIDATION_REGEX


def validate(appointment):
    errors = []

    required_fields = [
        'patient', 'status', 'time', 'duration',
        'clinician', 'department', 'postcode', 'id'
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

    if 'id' in appointment:
        try:
            UUID(appointment['id'])
        except ValueError:
            errors.append('Invalid UUID format for \'id\'')

    if 'time' in appointment:
        try:
            datetime.fromisoformat(appointment['time'])
        except ValueError:
            errors.append('Invalid ISO 8601 datetime format for \'time\'')

    if 'duration' in appointment:
        if not re.match(r'^\d+[hm]$', appointment['duration']):  # e.g., '1h' or '30m'
            errors.append('Invalid format for \'duration\' (expected formats like \'1h\' or \'30m\')')

    if 'status' in appointment:
        if appointment['status'] not in ['active', 'inactive', 'pending']:
            errors.append('Invalid \'status\' value. Allowed: \'active\', \'inactive\', \'pending\'')

    return errors


def validate_personnel(appointment, errors):
    if 'patient' in appointment:
        if not re.match(r'^\d{10}$', appointment['patient']):
            errors.append('Invalid \'patient\' ID. Expected 10-digit number')

    if 'clinician' in appointment:
        if not isinstance(appointment['clinician'], str) or len(appointment['clinician']) < 3:
            errors.append('Invalid \'clinician\' value')

    return errors


def validate_location(appointment, errors):
    postcode = appointment.get('postcode')
    if not postcode:
        errors.append('Missing postcode')
        return errors

    if not re.match(UK_POSTCODE_VALIDATION_REGEX, postcode, re.IGNORECASE):
        errors.append('Invalid UK postcode format')

    if 'department' in appointment:
        if not isinstance(appointment['department'], str) or not appointment['department']:
            errors.append('Invalid \'department\' value')

    return errors
