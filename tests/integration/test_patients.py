import json
import tornado.testing
from tornado.testing import AsyncHTTPTestCase
from main import start_app


class PatientHandlerTests(AsyncHTTPTestCase):
    def get_app(self):
        return start_app()

    def test_get_patient_valid_nhs_number(self):
        valid_nhs_number = '1373645350'
        response = self.fetch(f'/api/patients/{valid_nhs_number}')

        self.assertEqual(response.code, 200)
        body = json.loads(response.body)

        expected_patient = {
            'nhs_number': '1373645350',
            'name': 'Dr Glenn Clark',
            'date_of_birth': '1996-02-01',
            'postcode': 'N6 2FA'
        }
        self.assertEqual(body, expected_patient)

    def test_post_appointment_creates_appointment(self):
        new_patient = {
            'nhs_number': '1373645350',
            'name': 'Dr Glenn Clark',
            'date_of_birth': '1996-02-01',
            'postcode': 'N6 2FA'
        }

        response = self.fetch(
            f'/api/patients/1373645350',
            method='POST',
            body=json.dumps(new_patient),
            headers={'Content-Type': 'application/json'}
        )

        self.assertEqual(response.code, 201)
        body = json.loads(response.body)

        expected_body = {'message': 'new patient added:1373645350'}
        self.assertEqual(body, expected_body)

    # TODO: add integration tests around delete and update


if __name__ == '__main__':
    tornado.testing.main()
