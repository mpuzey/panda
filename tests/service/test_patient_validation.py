import unittest
from src.service.patient_validation import validate
from constants import READABLE_DATE_FORMAT


class TestValidatePatientData(unittest.TestCase):

    def setUp(self):
        self.valid_patient = {
            'nhs_number': '1373645350',
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

    def test_invalid_nhs_number(self):
        invalid_numbers = ['abc123', '123', '12345678901', '000000000']
        for nhs_number in invalid_numbers:
            with self.subTest(nhs_number=nhs_number):
                data = self.valid_patient.copy()
                data['nhs_number'] = nhs_number
                errors = validate(data)
                assert 'Invalid NHS number. Must be a 10-digit number' in errors

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