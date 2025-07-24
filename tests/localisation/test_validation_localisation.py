import unittest
from unittest.mock import Mock, patch
from src.service.validation_utils import check_required_fields, check_regex, check_min_length, check_date_format
from src.service.patient_validation import validate as validate_patient
from src.service.appointment_validation import validate as validate_appointment


class TestValidationlocalisation(unittest.TestCase):
    """Test localisation integration with validation functions."""

    def test_check_required_fields_returns_localisation_format(self):
        """Test that check_required_fields returns the new localisation format."""
        data = {'name': 'John', 'age': None}  # missing 'age'
        required_fields = ['name', 'age', 'email']
        
        errors = check_required_fields(data, required_fields)
        
        expected = [
            {'key': 'missing_required_field', 'params': {'field': 'age'}},
            {'key': 'missing_required_field', 'params': {'field': 'email'}}
        ]
        self.assertEqual(errors, expected)

    def test_check_regex_returns_localisation_format(self):
        """Test that check_regex returns the new localisation format."""
        errors = check_regex('invalid', r'^\d+$', 'invalid_number', field='test_field')
        
        expected = [{'key': 'invalid_number', 'params': {'field': 'test_field'}}]
        self.assertEqual(errors, expected)

    def test_check_regex_success_returns_empty(self):
        """Test that check_regex returns empty list for valid input."""
        errors = check_regex('123', r'^\d+$', 'invalid_number', field='test_field')
        self.assertEqual(errors, [])

    def test_check_min_length_returns_localisation_format(self):
        """Test that check_min_length returns the new localisation format."""
        errors = check_min_length('ab', 3, 'invalid_name')
        
        expected = [{'key': 'invalid_name', 'params': {}}]
        self.assertEqual(errors, expected)

    def test_check_min_length_success_returns_empty(self):
        """Test that check_min_length returns empty list for valid input."""
        errors = check_min_length('abc', 3, 'invalid_name')
        self.assertEqual(errors, [])

    def test_check_date_format_returns_localisation_format(self):
        """Test that check_date_format returns the new localisation format."""
        errors = check_date_format('invalid-date', '%Y-%m-%d', 'invalid_date_format', field='date_of_birth')
        
        expected = [{'key': 'invalid_date_format', 'params': {'field': 'date_of_birth'}}]
        self.assertEqual(errors, expected)

    def test_check_date_format_future_date_returns_localisation_format(self):
        """Test that check_date_format returns localisation format for future dates."""
        errors = check_date_format('3000-01-01', '%Y-%m-%d', 'invalid_date_format', 'invalid_date_of_birth', field='date_of_birth')
        
        expected = [{'key': 'invalid_date_of_birth', 'params': {'field': 'date_of_birth'}}]
        self.assertEqual(errors, expected)

    def test_check_date_format_success_returns_empty(self):
        """Test that check_date_format returns empty list for valid input."""
        errors = check_date_format('1990-01-01', '%Y-%m-%d', 'invalid_date_format', field='date_of_birth')
        self.assertEqual(errors, [])


class TestPatientValidationlocalisation(unittest.TestCase):
    """Test localisation integration with patient validation."""

    def test_patient_validation_returns_localisation_format(self):
        """Test that patient validation returns the new localisation format."""
        invalid_patient = {
            'nhs_number': 'invalid',
            'name': 'ab',  # too short
            'date_of_birth': 'invalid-date',
            'postcode': 'invalid'
        }
        
        errors = validate_patient(invalid_patient)
        
        # Verify that errors are in the new format
        self.assertIsInstance(errors, list)
        for error in errors:
            self.assertIsInstance(error, dict)
            self.assertIn('key', error)
            self.assertIn('params', error)

    def test_patient_validation_missing_fields(self):
        """Test patient validation with missing fields."""
        invalid_patient = {}
        
        errors = validate_patient(invalid_patient)
        
        # Should have missing field errors
        missing_field_errors = [e for e in errors if e['key'] == 'missing_required_field']
        self.assertEqual(len(missing_field_errors), 4)  # 4 required fields
        
        # Check that field names are in params
        field_names = {e['params']['field'] for e in missing_field_errors}
        expected_fields = {'nhs_number', 'name', 'date_of_birth', 'postcode'}
        self.assertEqual(field_names, expected_fields)

    def test_patient_validation_invalid_nhs_number(self):
        """Test patient validation with invalid NHS number."""
        invalid_patient = {
            'nhs_number': 'abc123',
            'name': 'John Doe',
            'date_of_birth': '1990-01-01',
            'postcode': 'N6 2FA'
        }
        
        errors = validate_patient(invalid_patient)
        
        # Should have NHS number error
        nhs_errors = [e for e in errors if e['key'] == 'invalid_nhs_number']
        self.assertEqual(len(nhs_errors), 1)

    def test_patient_validation_valid_patient(self):
        """Test patient validation with valid patient data."""
        valid_patient = {
            'nhs_number': '9434765919',  # Valid NHS number
            'name': 'John Doe',
            'date_of_birth': '1990-01-01',
            'postcode': 'N6 2FA'
        }
        
        errors = validate_patient(valid_patient)
        self.assertEqual(errors, [])


class TestAppointmentValidationlocalisation(unittest.TestCase):
    """Test localisation integration with appointment validation."""

    def test_appointment_validation_returns_localisation_format(self):
        """Test that appointment validation returns the new localisation format."""
        invalid_appointment = {
            'patient': 'invalid',
            'status': 'invalid_status',
            'time': 'invalid-time',
            'duration': 'invalid-duration',
            'clinician': 'ab',  # too short
            'department': '',  # empty
            'postcode': 'invalid',
            'id': 'invalid-uuid'
        }
        
        errors = validate_appointment(invalid_appointment)
        
        # Verify that errors are in the new format
        self.assertIsInstance(errors, list)
        for error in errors:
            self.assertIsInstance(error, dict)
            self.assertIn('key', error)
            self.assertIn('params', error)

    def test_appointment_validation_missing_fields(self):
        """Test appointment validation with missing fields."""
        invalid_appointment = {}
        
        errors = validate_appointment(invalid_appointment)
        
        # Should have missing field errors
        missing_field_errors = [e for e in errors if e['key'] == 'missing_required_field']
        self.assertEqual(len(missing_field_errors), 8)  # 8 required fields

    def test_appointment_validation_invalid_uuid(self):
        """Test appointment validation with invalid UUID."""
        valid_appointment = {
            'patient': '9434765919',
            'status': 'active',
            'time': '2025-06-04T16:30:00+01:00',
            'duration': '1h',
            'clinician': 'Dr. Smith',
            'department': 'oncology',
            'postcode': 'IM2N 4LG',
            'id': 'invalid-uuid'
        }
        
        errors = validate_appointment(valid_appointment)
        
        # Should have UUID error with field information
        uuid_errors = [e for e in errors if e['key'] == 'invalid_uuid']
        self.assertEqual(len(uuid_errors), 1)
        self.assertEqual(uuid_errors[0]['params']['field'], 'id')

    def test_appointment_validation_invalid_time(self):
        """Test appointment validation with invalid time format."""
        valid_appointment = {
            'patient': '9434765919',
            'status': 'active',
            'time': 'invalid-time-format',
            'duration': '1h',
            'clinician': 'Dr. Smith',
            'department': 'oncology',
            'postcode': 'IM2N 4LG',
            'id': '01542f70-929f-4c9a-b4fa-e672310d7e78'
        }
        
        errors = validate_appointment(valid_appointment)
        
        # Should have time error with field information
        time_errors = [e for e in errors if e['key'] == 'invalid_iso8601_time']
        self.assertEqual(len(time_errors), 1)
        self.assertEqual(time_errors[0]['params']['field'], 'time')

    def test_appointment_validation_valid_appointment(self):
        """Test appointment validation with valid appointment data."""
        valid_appointment = {
            'patient': '9434765919',
            'status': 'active',
            'time': '2025-06-04T16:30:00+01:00',
            'duration': '1h',
            'clinician': 'Dr. Smith',
            'department': 'oncology',
            'postcode': 'IM2N 4LG',
            'id': '01542f70-929f-4c9a-b4fa-e672310d7e78'
        }
        
        errors = validate_appointment(valid_appointment)
        self.assertEqual(errors, [])


if __name__ == '__main__':
    unittest.main() 