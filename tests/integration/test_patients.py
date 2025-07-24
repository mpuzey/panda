import json
import tornado.testing
from tornado.testing import AsyncHTTPTestCase
from main import start_app
from pymongo import MongoClient
from config import MONGODB_URI
from constants import MONGODB_DATABASE_NAME, MONGODB_COLLECTION_PATIENTS


class PatientHandlerTests(AsyncHTTPTestCase):
    def get_app(self):
        return start_app()

    def setUp(self):
        super().setUp()
        self.test_patient_nhs_numbers = []

    def tearDown(self):
        client = MongoClient(MONGODB_URI)
        db = client[MONGODB_DATABASE_NAME]
        collection = db[MONGODB_COLLECTION_PATIENTS]
        for nhs_number in self.test_patient_nhs_numbers:
            collection.delete_one({'nhs_number': nhs_number})
        client.close()
        super().tearDown()

    def test_get_patient_valid_nhs_number(self):
        valid_nhs_number = '1373645350'
        self.test_patient_nhs_numbers.append(valid_nhs_number)
        # Create the patient first
        new_patient = {
            'nhs_number': valid_nhs_number,
            'name': 'Dr Glenn Clark',
            'date_of_birth': '1996-02-01',
            'postcode': 'N6 2FA'
        }
        create_response = self.fetch(
            f'/api/patients/{valid_nhs_number}',
            method='POST',
            body=json.dumps(new_patient),
            headers={'Content-Type': 'application/json'}
        )
        self.assertEqual(create_response.code, 201)

        response = self.fetch(f'/api/patients/{valid_nhs_number}')
        self.assertEqual(response.code, 200)
        body = json.loads(response.body)

        expected_patient = new_patient
        self.assertEqual(body, expected_patient)

    def test_post_patient_creates_patient(self):
        new_patient = {
            'nhs_number': '1373645351',
            'name': 'Dr Glenn Clark',
            'date_of_birth': '1996-02-01',
            'postcode': 'N6 2FA'
        }
        self.test_patient_nhs_numbers.append(new_patient['nhs_number'])

        response = self.fetch(
            f'/api/patients/1373645351',
            method='POST',
            body=json.dumps(new_patient),
            headers={'Content-Type': 'application/json'}
        )

        self.assertEqual(response.code, 201)
        body = json.loads(response.body)

        expected_body = {'message': 'new patient added: 1373645351'}
        self.assertEqual(body, expected_body)

    def test_put_patient_updates_patient(self):
        nhs_number = '1373645351'
        self.test_patient_nhs_numbers.append(nhs_number)
        # Create the patient first
        new_patient = {
            'nhs_number': nhs_number,
            'name': 'Dr Glenn Clark',
            'date_of_birth': '1996-02-01',
            'postcode': 'N6 2FA'
        }
        create_response = self.fetch(
            f'/api/patients/{nhs_number}',
            method='POST',
            body=json.dumps(new_patient),
            headers={'Content-Type': 'application/json'}
        )
        self.assertEqual(create_response.code, 201)

        # Now update
        updated_patient = {
            'nhs_number': nhs_number,
            'name': 'Dr Glenn Tipton',  # <-- update
            'date_of_birth': '1996-02-01',
            'postcode': 'N6 2FA'
        }

        response = self.fetch(
            f'/api/patients/{nhs_number}',
            method='PUT',
            body=json.dumps(updated_patient),
            headers={'Content-Type': 'application/json'}
        )

        self.assertEqual(response.code, 200)
        body = json.loads(response.body)

        expected_body = {'message': f'patient updated: {nhs_number}'}
        self.assertEqual(body, expected_body)

    # TODO: add integration tests around delete


if __name__ == '__main__':
    tornado.testing.main()
