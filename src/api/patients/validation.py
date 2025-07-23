import re
from datetime import datetime

from constants import UK_POSTCODE_VALIDATION_REGEX, FIELD_NHS_NUMBER, FIELD_NAME, FIELD_DATE_OF_BIRTH, FIELD_POSTCODE, NHS_NUMBER_REGEX, DATE_FORMAT


def validate(patient):
    errors = []

    required_fields = [FIELD_NHS_NUMBER, FIELD_NAME, FIELD_DATE_OF_BIRTH, FIELD_POSTCODE]

    errors.extend([f'Missing required field: {field}' for field in required_fields if not patient.get(field)])
    if errors:
        print('Invalid appointment:', errors)
        return errors

    errors.extend(validate_nhs_number(patient['nhs_number']))
    errors.extend(validate_name(patient['name']))
    errors.extend(validate_date_of_birth(patient['date_of_birth']))
    errors.extend(validate_postcode(patient['postcode']))

    if errors:
        print('Invalid appointment:', errors)

    return errors


# TODO: Ensure that all NHS numbers are checksum validated.
# https://www.datadictionary.nhs.uk/attributes/nhs_number.html
def validate_nhs_number(value):
    if not re.fullmatch(NHS_NUMBER_REGEX, str(value)):
        return ["Invalid NHS number. Must be a 10-digit number"]
    return []


def validate_name(value):
    if not isinstance(value, str) or len(value.strip()) < 3:
        return ['Invalid name. Must be a non-empty string of at least 3 characters']
    return []


def validate_date_of_birth(value):
    try:
        dob = datetime.strptime(value, DATE_FORMAT).date()
        if dob > datetime.today().date():
            return ['Invalid date of birth. Cannot be in the future']
        return []
    except (ValueError, TypeError):
        return [f'Invalid date format for {FIELD_DATE_OF_BIRTH}. Expected \'{DATE_FORMAT}\'']

# https://ideal-postcodes.co.uk/guides/uk-postcode-format
def validate_postcode(value):
    if not isinstance(value, str):
        return ['Invalid UK postcode format']
    if not re.match(UK_POSTCODE_VALIDATION_REGEX, value.strip(), re.IGNORECASE):
        return ['Invalid UK postcode format']
    return []
