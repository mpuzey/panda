import json
import uuid
import tornado.testing
from tornado.testing import AsyncHTTPTestCase
from main import start_app
from pymongo import MongoClient
from config import MONGODB_URI
from constants import MONGODB_DATABASE_NAME, MONGODB_COLLECTION_APPOINTMENTS


class AppointmentHandlerTests(AsyncHTTPTestCase):
    def get_app(self):
        return start_app()

    def setUp(self):
        super().setUp()
        self.test_appointment_ids = []

    def tearDown(self):
        # Hard delete test appointments directly from the DB
        client = MongoClient(MONGODB_URI)
        db = client[MONGODB_DATABASE_NAME]
        collection = db[MONGODB_COLLECTION_APPOINTMENTS]
        for appointment_id in self.test_appointment_ids:
            collection.delete_one({'id': appointment_id})
        client.close()
        super().tearDown()

    def test_get_appointment_valid_appointment_id(self):
        valid_uuid = "ac9729b5-5e11-42b4-87e2-6396b4faf1b9"
        self.test_appointment_ids.append(valid_uuid)
        # Create the appointment first
        new_appointment = {
            'id': valid_uuid,
            'patient': '9434765919',  # Valid NHS number with correct checksum
            'status': 'active',
            'time': '2024-08-30T11:30:00+01:00',
            'duration': '2h',
            'clinician': 'Glenn Palmer',
            'department': 'oncology',
            'postcode': 'HD36 0HQ'
        }
        create_response = self.fetch(
            f"/api/appointments/{valid_uuid}",
            method="POST",
            body=json.dumps(new_appointment),
            headers={'Content-Type': 'application/json'}
        )
        self.assertEqual(create_response.code, 201)

        # Now fetch and check
        response = self.fetch(f"/api/appointments/{valid_uuid}")
        self.assertEqual(response.code, 200)
        body = json.loads(response.body)
        expected_appointment = new_appointment
        self.assertEqual(body, expected_appointment)

    def test_get_appointment_invalid_uuid_format(self):
        invalid_uuid = '12345'
        response = self.fetch(f'/api/appointments/{invalid_uuid}')

        self.assertEqual(response.code, 404)

    def test_get_appointment_unregistered_uuid(self):
        unregistered_uuid = str(uuid.uuid4())
        response = self.fetch(f'/api/appointments/{unregistered_uuid}')

        self.assertIn(response.code, [200, 404])

    def test_post_appointment_creates_appointment(self):
        new_appointment = {
            'id': 'ac9729b5-5e11-42b4-87e2-6396b4faf1b1',
            'patient': '9876543210',  # Valid NHS number with correct checksum
            'status': 'active',
            'time': '2024-08-30T11:30:00+01:00',
            'duration': '2h',
            'clinician': 'Glenn Palmer',
            'department': 'oncology',
            'postcode': 'HD36 0HQ'
        }
        self.test_appointment_ids.append(new_appointment['id'])

        response = self.fetch(
            f'/api/appointments/ac9729b5-5e11-42b4-87e2-6396b4faf1b1',
            method='POST',
            body=json.dumps(new_appointment),
            headers={'Content-Type': 'application/json'}
        )

        self.assertEqual(response.code, 201)
        body = json.loads(response.body)

        expected_body = {'message': 'new appointment added: ac9729b5-5e11-42b4-87e2-6396b4faf1b1'}
        self.assertEqual(body, expected_body)

    def test_put_appointment_updates_appointment(self):
        new_appointment = {
            'id': 'ac9729b5-5e11-42b4-87e2-6396b4faf1b1',
            'patient': '9876543210',  # Valid NHS number with correct checksum
            'status': 'active',
            'time': '2024-08-30T11:30:00+01:00',
            'duration': '2h',
            'clinician': 'Glenn Close',  # <-- update
            'department': 'oncology',
            'postcode': 'HD36 0HQ'
        }
        self.test_appointment_ids.append(new_appointment['id'])

        response = self.fetch(
            f'/api/appointments/ac9729b5-5e11-42b4-87e2-6396b4faf1b1',
            method='PUT',
            body=json.dumps(new_appointment),
            headers={'Content-Type': 'application/json'}
        )

        self.assertEqual(response.code, 200)
        body = json.loads(response.body)

        expected_body = {'message': 'appointment updated: ac9729b5-5e11-42b4-87e2-6396b4faf1b1'}
        self.assertEqual(body, expected_body)

    def test_delete_appointment_cancels_appointment(self):
        """Test that DELETE request cancels an appointment."""
        appointment_id = 'ac9729b5-5e11-42b4-87e2-6396b4faf1b2'
        self.test_appointment_ids.append(appointment_id)

        # First create an appointment
        new_appointment = {
            'id': appointment_id,
            'patient': '1234567881',  # Valid NHS number with correct checksum
            'status': 'active',
            'time': '2024-08-30T11:30:00+01:00',
            'duration': '2h',
            'clinician': 'Glenn Palmer',
            'department': 'oncology',
            'postcode': 'HD36 0HQ'
        }

        create_response = self.fetch(
            f'/api/appointments/{appointment_id}',
            method='POST',
            body=json.dumps(new_appointment),
            headers={'Content-Type': 'application/json'}
        )
        self.assertEqual(create_response.code, 201)

        # Now cancel the appointment
        delete_response = self.fetch(
            f'/api/appointments/{appointment_id}',
            method='DELETE'
        )

        self.assertEqual(delete_response.code, 200)
        body = json.loads(delete_response.body)
        expected_body = {'message': f'appointment cancelled: {appointment_id}'}
        self.assertEqual(body, expected_body)

    def test_create_appointment_cancelled_appointment_cannot_be_reinstated(self):
        """Test that a cancelled appointment cannot be recreated via POST."""
        appointment_id = 'ac9729b5-5e11-42b4-87e2-6396b4faf1b3'
        self.test_appointment_ids.append(appointment_id)

        # First create an appointment
        new_appointment = {
            'id': appointment_id,
            'patient': '1234567881',  # Valid NHS number with correct checksum
            'status': 'active',
            'time': '2024-08-30T11:30:00+01:00',
            'duration': '2h',
            'clinician': 'Glenn Palmer',
            'department': 'oncology',
            'postcode': 'HD36 0HQ'
        }

        create_response = self.fetch(
            f'/api/appointments/{appointment_id}',
            method='POST',
            body=json.dumps(new_appointment),
            headers={'Content-Type': 'application/json'}
        )
        self.assertEqual(create_response.code, 201)

        # Cancel the appointment
        delete_response = self.fetch(
            f'/api/appointments/{appointment_id}',
            method='DELETE'
        )
        self.assertEqual(delete_response.code, 200)

        # Try to recreate the cancelled appointment
        recreate_appointment = {
            'id': appointment_id,
            'patient': '1234567881',  # Valid NHS number with correct checksum
            'status': 'active',
            'time': '2024-08-30T11:30:00+01:00',
            'duration': '2h',
            'clinician': 'Glenn Palmer',
            'department': 'oncology',
            'postcode': 'HD36 0HQ'
        }

        recreate_response = self.fetch(
            f'/api/appointments/{appointment_id}',
            method='POST',
            body=json.dumps(recreate_appointment),
            headers={'Content-Type': 'application/json'}
        )

        self.assertEqual(recreate_response.code, 400)
        body = json.loads(recreate_response.body)
        self.assertEqual(body['error'], 'could not update appointment')

    def test_update_appointment_cancelled_appointment_cannot_be_reinstated(self):
        """Test that a cancelled appointment cannot be reinstated via PUT."""
        appointment_id = 'ac9729b5-5e11-42b4-87e2-6396b4faf1b4'
        self.test_appointment_ids.append(appointment_id)

        # First create an appointment
        new_appointment = {
            'id': appointment_id,
            'patient': '4505577104',  # Valid NHS number with correct checksum
            'status': 'active',
            'time': '2024-08-30T11:30:00+01:00',
            'duration': '2h',
            'clinician': 'Glenn Palmer',
            'department': 'oncology',
            'postcode': 'HD36 0HQ'
        }

        create_response = self.fetch(
            f'/api/appointments/{appointment_id}',
            method='POST',
            body=json.dumps(new_appointment),
            headers={'Content-Type': 'application/json'}
        )
        self.assertEqual(create_response.code, 201)

        # Cancel the appointment
        delete_response = self.fetch(
            f'/api/appointments/{appointment_id}',
            method='DELETE'
        )
        self.assertEqual(delete_response.code, 200)

        # Try to update the cancelled appointment
        update_appointment = {
            'id': appointment_id,
            'patient': '4505577104',  # Valid NHS number with correct checksum
            'status': 'active',
            'time': '2024-08-30T11:30:00+01:00',
            'duration': '2h',
            'clinician': 'Glenn Close',  # Changed clinician
            'department': 'oncology',
            'postcode': 'HD36 0HQ'
        }

        update_response = self.fetch(
            f'/api/appointments/{appointment_id}',
            method='PUT',
            body=json.dumps(update_appointment),
            headers={'Content-Type': 'application/json'}
        )

        self.assertEqual(update_response.code, 400)
        body = json.loads(update_response.body)
        self.assertEqual(body['error'], 'could not update appointment')


if __name__ == '__main__':
    tornado.testing.main()
