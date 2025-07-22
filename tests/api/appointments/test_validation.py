import unittest
from src.api.appointments.validation import validate


class TestValidation(unittest.TestCase):
    def setUp(self):
        self.valid_appointment = {
            'patient': '1953262716',
            'status': 'active',
            'time': '2025-06-04T16:30:00+01:00',
            'duration': '1h',
            'clinician': 'Bethany Rice-Hammond',
            'department': 'oncology',
            'postcode': 'IM2N 4LG',
            'id': '01542f70-929f-4c9a-b4fa-e672310d7e78'
        }

    def test_valid_appointment(self):
        errors = validate(self.valid_appointment)
        self.assertEqual(errors, [])

    def test_missing_fields(self):
        appointment = self.valid_appointment.copy()
        del appointment['status']
        del appointment['time']
        errors = validate(appointment)
        assert 'Missing required field: status' in errors
        assert 'Missing required field: time' in errors

    def test_none_fields(self):
        appointment = self.valid_appointment.copy()
        appointment['patient'] = None
        appointment['duration'] = None
        errors = validate(appointment)
        assert 'Missing required field: patient' in errors
        assert 'Missing required field: duration' in errors

    def test_invalid_uuid(self):
        appointment = self.valid_appointment.copy()
        appointment['id'] = 'invalid-uuid'
        errors = validate(appointment)
        assert 'Invalid UUID format for \'id\'' in errors

    def test_invalid_time_format(self):
        appointment = self.valid_appointment.copy()
        appointment['time'] = '06/04/2025 16:30'
        errors = validate(appointment)
        assert 'Invalid ISO 8601 datetime format for \'time\'' in errors

    def test_invalid_duration(self):
        appointment = self.valid_appointment.copy()
        appointment['duration'] = '60minutes'
        errors = validate(appointment)
        assert 'Invalid format for \'duration\' (expected formats like \'1h\' or \'30m\')' in errors

    def test_invalid_status(self):
        appointment = self.valid_appointment.copy()
        appointment['status'] = 'closed'
        errors = validate(appointment)
        assert 'Invalid \'status\' value. Allowed: \'active\', \'attended\', \'cancelled\', \'missed\'' in errors

    def test_invalid_postcode(self):
        appointment = self.valid_appointment.copy()
        appointment['postcode'] = '12345'
        errors = validate(appointment)
        assert 'Invalid UK postcode format' in errors

    def test_valid_postcodes(self):
        valid_postcodes = [
            'EC1A 1BB',
            'W1A 0AX',
            'M1 1AE',
            'B33 8TH',
            'CR2 6XH',
            'DN55 1PT',
            'im2n 4lg',  # lowercase, should pass
            'IM2N4LG',  # no space, should still pass
        ]
        for pc in valid_postcodes:
            with self.subTest(postcode=pc):
                appointment = self.valid_appointment.copy()
                appointment['postcode'] = pc
                errors = validate(appointment)
                assert not errors

    def test_invalid_postcodes(self):
        invalid_postcodes = [
            '123456',  # numeric only
            'ABCDE',  # too short, no digits
            'W1A-0AX',  # invalid separator
            'ZZZZ ZZZ',  # all letters
            'AB1 123',  # ends in numbers, invalid
            'IM2N4',  # incomplete
            'IM2N 4LGG',  # too long
        ]
        for pc in invalid_postcodes:
            with self.subTest(postcode=pc):
                appointment = self.valid_appointment.copy()
                appointment['postcode'] = pc
                errors = validate(appointment)
                assert 'Invalid UK postcode format' in errors

    def test_invalid_appointment_id(self):
        appointment = self.valid_appointment.copy()
        appointment['patient'] = 'ABC123'
        errors = validate(appointment)
        assert 'Invalid \'patient\' ID. Expected 10-digit number' in errors

    def test_short_clinician_name(self):
        appointment = self.valid_appointment.copy()
        appointment['clinician'] = 'Dr'
        errors = validate(appointment)
        assert 'Invalid \'clinician\' value' in errors


if __name__ == '__main__':
    unittest.main()
