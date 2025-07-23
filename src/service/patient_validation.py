import re
from datetime import datetime

from constants import UK_POSTCODE_VALIDATION_REGEX, FIELD_NHS_NUMBER, FIELD_NAME, FIELD_DATE_OF_BIRTH, FIELD_POSTCODE, \
    NHS_NUMBER_REGEX, DATE_FORMAT
from src.service.validation_utils import check_required_fields, check_regex, check_min_length, check_date_format


def validate(patient):
    errors = []
    required_fields = [FIELD_NHS_NUMBER, FIELD_NAME, FIELD_DATE_OF_BIRTH, FIELD_POSTCODE]
    errors += check_required_fields(patient, required_fields)
    if errors:
        print('Invalid appointment:', errors)
        return errors
    errors += check_regex(patient['nhs_number'], NHS_NUMBER_REGEX, "Invalid NHS number. Must be a 10-digit number")
    errors += check_min_length(patient['name'], 3, "Invalid name. Must be a non-empty string of at least 3 characters")
    errors += check_date_format(
        patient['date_of_birth'], DATE_FORMAT,
        f"Invalid date format for {FIELD_DATE_OF_BIRTH}. Expected '{DATE_FORMAT}'",
        "Invalid date of birth. Cannot be in the future"
    )
    errors += validate_postcode(patient['postcode'])
    if errors:
        print('Invalid appointment:', errors)
    return errors

# https://ideal-postcodes.co.uk/guides/uk-postcode-format
def validate_postcode(value):
    if not isinstance(value, str):
        return ['Invalid UK postcode format']
    if not re.match(UK_POSTCODE_VALIDATION_REGEX, value.strip(), re.IGNORECASE):
        return ['Invalid UK postcode format']
    return []
