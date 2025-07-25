import re

from src.service.validation_utils import check_required_fields, check_regex, check_min_length, check_date_format, validate_nhs_number_checksum
from constants import (
    UK_POSTCODE_VALIDATION_REGEX,
    PATIENT_FIELD_NHS_NUMBER,
    PATIENT_FIELD_NAME,
    PATIENT_FIELD_DATE_OF_BIRTH,
    PATIENT_FIELD_POSTCODE,
    NHS_NUMBER_REGEX,
    DATE_FORMAT,
    INVALID_DATE_FORMAT_ERROR_TEXT,
    INVALID_DATE_OF_BIRTH_ERROR_TEXT,
    INVALID_NHS_NUMBER_ERROR_TEXT,
    INVALID_NHS_NUMBER_CHECKSUM_ERROR_TEXT,
    INVALID_NAME_ERROR_TEXT,
    INVALID_UK_POSTCODE_ERROR_TEXT
)


def validate(patient):
    """Validate a patient record against business rules and format requirements."""
    errors = []
    required_fields = [PATIENT_FIELD_NHS_NUMBER, PATIENT_FIELD_NAME, PATIENT_FIELD_DATE_OF_BIRTH, PATIENT_FIELD_POSTCODE]
    errors += check_required_fields(patient, required_fields)

    if errors:
        print('Invalid patient:', errors)
        return errors

    # Validate NHS number format and checksum
    nhs_number = patient.get(PATIENT_FIELD_NHS_NUMBER, '')
    if not re.match(NHS_NUMBER_REGEX, nhs_number):
        errors.append(INVALID_NHS_NUMBER_ERROR_TEXT)
    elif not validate_nhs_number_checksum(nhs_number):
        errors.append(INVALID_NHS_NUMBER_CHECKSUM_ERROR_TEXT)

    errors += check_min_length(patient[PATIENT_FIELD_NAME], 3, INVALID_NAME_ERROR_TEXT)
    errors += check_date_format(
        patient[PATIENT_FIELD_DATE_OF_BIRTH], DATE_FORMAT,
        INVALID_DATE_FORMAT_ERROR_TEXT,
        INVALID_DATE_OF_BIRTH_ERROR_TEXT
    )
    errors += validate_postcode(patient[PATIENT_FIELD_POSTCODE])

    if errors:
        print('Invalid patient:', errors)
    return errors

# https://ideal-postcodes.co.uk/guides/uk-postcode-format
def validate_postcode(value):
    """Validate a UK postcode format."""
    if not isinstance(value, str):
        return [INVALID_UK_POSTCODE_ERROR_TEXT]
        
    if not re.match(UK_POSTCODE_VALIDATION_REGEX, value.strip(), re.IGNORECASE):
        return [INVALID_UK_POSTCODE_ERROR_TEXT]
    return []
