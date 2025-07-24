import re
from datetime import datetime


def check_required_fields(data, required_fields):
    errors = []
    for field in required_fields:
        data_field_value = data.get(field)
        if not data_field_value:
            errors.append(f'Missing required field: {field}')
    return errors


def check_regex(value, regex, error_msg):
    if not re.fullmatch(regex, str(value)):
        return [error_msg]
    return []


def check_min_length(value, min_length, error_msg):
    if not isinstance(value, str) or len(value) < min_length:
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


def validate_nhs_number_checksum(nhs_number):
    """
    Validate NHS number using Modulus 11 algorithm as per NHS Data Dictionary.
    https://www.datadictionary.nhs.uk/attributes/nhs_number.html
    
    Steps:
    1. Multiply each of the first nine digits by weighting factors (10,9,8,7,6,5,4,3,2)
    2. Add the results together
    3. Divide by 11 and get remainder
    4. Subtract remainder from 11 to get check digit
    5. If result is 11, check digit is 0. If result is 10, NHS number is invalid
    6. Compare calculated check digit with the 10th digit
    """
    if not isinstance(nhs_number, str) or len(nhs_number) != 10 or not nhs_number.isdigit():
        return False
    
    # Step 1: Multiply each of first 9 digits by weighting factors
    weights = [10, 9, 8, 7, 6, 5, 4, 3, 2]
    multiplications = []
    for digit, weight in zip(nhs_number[:9], weights):
        multiplications.append(int(digit) * weight)

    # Step 2: Add the results together
    total = sum(multiplications)
    
    # Step 3: Divide by 11 and get remainder
    remainder = total % 11
    
    # Step 4: Subtract remainder from 11 to get check digit
    calculated_check_digit = 11 - remainder
    
    # Step 5: Handle special cases
    if calculated_check_digit == 11:
        calculated_check_digit = 0
    elif calculated_check_digit == 10:
        return False  # Invalid NHS number
    
    # Step 6: Compare with actual 10th digit
    actual_check_digit = int(nhs_number[9])
    
    return calculated_check_digit == actual_check_digit
