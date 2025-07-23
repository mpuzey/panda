import re
from datetime import datetime
from constants import MISSING_REQUIRED_FIELD_ERROR_TEXT


def check_required_fields(data, required_fields):
    return [MISSING_REQUIRED_FIELD_ERROR_TEXT.format(field) for field in required_fields if not data.get(field)]


def check_regex(value, regex, error_msg):
    if not re.fullmatch(regex, str(value)):
        return [error_msg]
    return []


def check_min_length(value, min_length, error_msg):
    if not isinstance(value, str) or len(value.strip()) < min_length:
        return [error_msg]
    return []


def check_date_format(value, date_format, error_msg, future_error_msg=None):
    try:
        dob = datetime.strptime(value, date_format).date()
        if future_error_msg and dob > datetime.today().date():
            return [future_error_msg]
        return []
    except (ValueError, TypeError):
        return [error_msg]
