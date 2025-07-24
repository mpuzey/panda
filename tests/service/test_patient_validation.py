import unittest
from src.service.patient_validation import validate
from src.service.validation_utils import validate_nhs_number_checksum
from constants import READABLE_DATE_FORMAT


class TestValidatePatientData(unittest.TestCase):

    def setUp(self):
        self.valid_patient = {
            'nhs_number': '9434765919',  # Valid NHS number with correct checksum
            'name': 'Dr Glenn Clark',
            'date_of_birth': '1996-02-01',
            'postcode': 'N6 2FA'
        }

    def test_valid_patient(self):
        errors = validate(self.valid_patient)
        self.assertEqual(errors, [])

    def test_missing_fields(self):
        for field in self.valid_patient:
            with self.subTest(field=field):
                data = self.valid_patient.copy()
                del data[field]
                errors = validate(data)
                assert f'Missing required field: {field}' in errors

    def test_none_fields(self):
        for field in self.valid_patient:
            with self.subTest(field=field):
                data = self.valid_patient.copy()
                data[field] = None
                errors = validate(data)
                assert any('Missing required field' in e or 'Invalid' in e for e in errors)

    def test_valid_nhs_numbers_with_checksum(self):
        """Test NHS numbers with valid checksums"""
        valid_nhs_numbers = [
            '9434765919',  # Check digit 9
            '9876543210',  # Check digit 0 
            '1234567881',  # Check digit 1
            '4505577104',  # Check digit 4
        ]
        for nhs_number in valid_nhs_numbers:
            with self.subTest(nhs_number=nhs_number):
                data = self.valid_patient.copy()
                data['nhs_number'] = nhs_number
                errors = validate(data)
                self.assertEqual(errors, [])

    def test_invalid_nhs_number_format(self):
        """Test NHS numbers with invalid format"""
        invalid_numbers = ['abc123', '123', '12345678901', '000000000']
        for nhs_number in invalid_numbers:
            with self.subTest(nhs_number=nhs_number):
                data = self.valid_patient.copy()
                data['nhs_number'] = nhs_number
                errors = validate(data)
                assert 'Invalid NHS number. Must be a 10-digit number' in errors

    def test_invalid_nhs_number_checksum(self):
        """Test NHS numbers with invalid checksums"""
        invalid_checksum_numbers = [
            '9434765918',  # Should be 9, not 8
            '9876543211',  # Should be 0, not 1
            '1234567880',  # Should be 1, not 0
            '4505577103',  # Should be 4, not 3
        ]
        for nhs_number in invalid_checksum_numbers:
            with self.subTest(nhs_number=nhs_number):
                data = self.valid_patient.copy()
                data['nhs_number'] = nhs_number
                errors = validate(data)
                assert 'Invalid NHS number checksum' in errors

    def test_nhs_number_checksum_algorithm_edge_cases(self):
        """Test edge cases for NHS number checksum validation"""
        test_cases = [
            ('0000000000', True),   # All zeros - mathematically valid (check digit = 0)
            ('9434765919', True),   # Known valid case
            ('9434765918', False),  # Same as above but wrong check digit (should be 9, not 8)
            ('1000000001', True),   # Simple case: 1*10=10, 10%11=10, 11-10=1, check digit=1 ✓
            ('1000000002', False),  # Same as above but wrong check digit (should be 1, not 2)
        ]
        
        for nhs_number, expected_valid in test_cases:
            with self.subTest(nhs_number=nhs_number):
                result = validate_nhs_number_checksum(nhs_number)
                self.assertEqual(result, expected_valid)

    def test_invalid_name(self):
        invalid_names = [
            ('', 'Missing required field: name'),
            ('Ze', 'Invalid name. Must be a non-empty string of at least 3 characters'),
            (None, 'Missing required field: name'),
        ]
        for name, expected_error in invalid_names:
            with self.subTest(name=name):
                data = self.valid_patient.copy()
                data['name'] = name
                errors = validate(data)
                assert expected_error in errors

    def test_invalid_date_of_birth(self):
        invalid_dobs = [
            ('01/02/1996', f'Invalid date format for date_of_birth. Expected "{READABLE_DATE_FORMAT}"'),
            ('1996-13-01', f'Invalid date format for date_of_birth. Expected "{READABLE_DATE_FORMAT}"'),
            ('future-date', f'Invalid date format for date_of_birth. Expected "{READABLE_DATE_FORMAT}"'),
            ('3000-01-01', 'Invalid date of birth. Cannot be in the future'),
            ('', 'Missing required field: date_of_birth'),
            (None, 'Missing required field: date_of_birth'),
        ]
        for date_of_birth, expected_error in invalid_dobs:
            with self.subTest(date_of_birth=date_of_birth):
                data = self.valid_patient.copy()
                data['date_of_birth'] = date_of_birth
                errors = validate(data)
                assert expected_error in errors

    def test_invalid_postcode(self):
        invalid_postcodes = ['12345', 'ABC123', 'N6-2FA', 'N62FAAA']
        for postcode in invalid_postcodes:
            with self.subTest(postcode=postcode):
                data = self.valid_patient.copy()
                data['postcode'] = postcode
                errors = validate(data)
                assert 'Invalid UK postcode format' in errors

    def test_valid_postcode_formats(self):
        valid_postcodes = ['EC1A 1BB', 'W1A 0AX', 'M1 1AE', 'B33 8TH', 'CR2 6XH', 'DN55 1PT', 'n6 2fa', 'N62FA']
        for postcode in valid_postcodes:
            with self.subTest(postcode=postcode):
                data = self.valid_patient.copy()
                data['postcode'] = postcode
                errors = validate(data)
                self.assertEqual(errors, [])


if __name__ == '__main__':
    unittest.main()