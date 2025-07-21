import json
import uuid
import tornado.testing
from tornado.testing import AsyncHTTPTestCase
from main import start_app


class AppointmentHandlerTests(AsyncHTTPTestCase):
    def get_app(self):
        return start_app()

    def test_get_appointment_valid_appointment_id(self):
        valid_uuid = "ac9729b5-5e11-42b4-87e2-6396b4faf1b9"
        response = self.fetch(f"/api/appointments/{valid_uuid}")

        self.assertEqual(response.code, 200)
        body = json.loads(response.body)

        expected_appointment = {
            'patient': '0443743460',
            'status': 'active',
            'time': '2024-08-30T11:30:00+01:00',
            'duration': '2h',
            'clinician': 'Glenn Palmer',
            'department': 'oncology',
            'postcode': 'HD36 0HQ',
            'id': 'ac9729b5-5e11-42b4-87e2-6396b4faf1b9'
        }
        self.assertEqual(body, expected_appointment)

    def test_get_appointment_invalid_uuid_format(self):
        invalid_uuid = '12345'
        response = self.fetch(f'/api/appointments/{invalid_uuid}')

        self.assertEqual(response.code, 404)

    def test_get_appointment_unregistered_uuid(self):
        unregistered_uuid = str(uuid.uuid4())
        response = self.fetch(f'/api/appointments/{unregistered_uuid}')

        self.assertIn(response.code, [200, 404])

    # TODO: add integration tests around post and delete


if __name__ == '__main__':
    tornado.testing.main()
