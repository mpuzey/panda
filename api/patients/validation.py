import re
from datetime import datetime

from constants import UK_POSTCODE_VALIDATION_REGEX


def validate(patient):
    errors = []

    required_fields = ['nhs_number', 'name', 'date_of_birth', 'postcode']
    errors.extend(validate_required_fields(patient, required_fields))

    if not patient.get('nhs_number'):
        errors.extend(validate_nhs_number(patient['nhs_number']))

    if not patient.get('name'):
        errors.extend(validate_name(patient['name']))

    if not patient.get('date_of_birth'):
        errors.extend(validate_date_of_birth(patient['date_of_birth']))

    if not patient.get('postcode'):
        errors.extend(validate_postcode(patient['postcode']))

    return errors


def validate_required_fields(patient, fields):
    return [f'Missing required field: {field}' for field in fields if not patient.get(field)]


"""
https://www.datadictionary.nhs.uk/attributes/nhs_number.html
"""
def validate_nhs_number(value):
    if not re.fullmatch(r'\d{10}', str(value)):
        return ["Invalid NHS number. Must be a 10-digit number"]
    return []


def validate_name(value):
    if not isinstance(value, str) or len(value.strip()) < 3:
        return ['Invalid name. Must be a non-empty string of at least 3 characters']
    return []


def validate_date_of_birth(value):
    try:
        dob = datetime.strptime(value, '%Y-%m-%d').date()
        if dob > datetime.today().date():
            return ['Invalid date of birth. Cannot be in the future']
        return []
    except (ValueError, TypeError):
        return ['Invalid date format for date_of_birth. Expected \'YYYY-MM-DD\'']


def validate_postcode(value):
    if not isinstance(value, str):
        return ['Invalid UK postcode format']
    pattern = UK_POSTCODE_VALIDATION_REGEX
    if not re.match(pattern, value.strip(), re.IGNORECASE):
        return ['Invalid UK postcode format']
    return []
