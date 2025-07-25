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
        valid_nhs_number = '9434765919'  # Valid NHS number with correct checksum
        self.test_patient_nhs_numbers.append(valid_nhs_number)

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


        response = self.fetch(f"/api/patients/{valid_nhs_number}")
        self.assertEqual(response.code, 200)
        body = json.loads(response.body)
        expected_patient = new_patient
        self.assertEqual(body, expected_patient)

    def test_post_patient_creates_patient(self):
        new_patient = {
            'nhs_number': '9876543210',  # Valid NHS number with correct checksum
            'name': 'Dr Glenn Clark',
            'date_of_birth': '1996-02-01',
            'postcode': 'N6 2FA'
        }
        self.test_patient_nhs_numbers.append(new_patient['nhs_number'])

        response = self.fetch(
            f'/api/patients/{new_patient["nhs_number"]}',
            method='POST',
            body=json.dumps(new_patient),
            headers={'Content-Type': 'application/json'}
        )

        self.assertEqual(response.code, 201)
        body = json.loads(response.body)

        expected_body = {'message': f'new patient added: {new_patient["nhs_number"]}'}
        self.assertEqual(body, expected_body)

    def test_post_patient_with_comprehensive_unicode_name(self):
        """Test GDPR compliance end to end: patient name with comprehensive diacritical marks and Unicode characters"""
        unicode_name = 'José María Françoéis Müller-Søren Dvořák 刘桂荣 जगन्नाथ'
        valid_nhs_number = '8234567896'
        self.test_patient_nhs_numbers.append(valid_nhs_number)

        patient_data = {
            'nhs_number': valid_nhs_number,
            'name': unicode_name,  # Contains: Spanish, French, German, Nordic, Czech, Chinese, Hindi
            'date_of_birth': '1990-01-01',
            'postcode': 'SW1A 1AA'
        }

        response = self.fetch(
            f'/api/patients/{valid_nhs_number}',
            method='POST',
            body=json.dumps(patient_data),
            headers={'Content-Type': 'application/json'}
        )

        self.assertEqual(response.code, 201)

        get_response = self.fetch(f'/api/patients/{valid_nhs_number}')
        self.assertEqual(get_response.code, 200)

        retrieved_data = json.loads(get_response.body)
        self.assertEqual(retrieved_data['name'], unicode_name,
                        "Unicode name must be stored exactly as provided (GDPR Article 16 compliance)")

    def test_put_patient_updates_patient(self):
        nhs_number = '1234567881'  # Valid NHS number with correct checksum
        self.test_patient_nhs_numbers.append(nhs_number)

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

    def test_put_patient_preserves_unicode_characters(self):
        """Test that updating patient data preserves Unicode characters (GDPR compliance)"""
        valid_nhs_number = '1859995799'
        self.test_patient_nhs_numbers.append(valid_nhs_number)

        original_patient = {
            'nhs_number': valid_nhs_number,
            'name': 'María José Hernández-González',
            'date_of_birth': '1980-03-15',
            'postcode': 'EC1A 1BB'
        }

        create_response = self.fetch(
            f'/api/patients/{valid_nhs_number}',
            method='POST',
            body=json.dumps(original_patient),
            headers={'Content-Type': 'application/json'}
        )
        self.assertEqual(create_response.code, 201)

        updated_patient = {
            'nhs_number': valid_nhs_number,
            'name': 'María José Fernández-Röñez',  # Updated with more accents
            'date_of_birth': '1980-03-15',
            'postcode': 'EC1A 1BB'
        }

        update_response = self.fetch(
            f'/api/patients/{valid_nhs_number}',
            method='PUT',
            body=json.dumps(updated_patient),
            headers={'Content-Type': 'application/json'}
        )
        self.assertEqual(update_response.code, 200)

        get_response = self.fetch(f'/api/patients/{valid_nhs_number}')
        retrieved_data = json.loads(get_response.body)
        self.assertEqual(retrieved_data['name'], 'María José Fernández-Röñez',
                        "Updated Unicode name must be preserved exactly (GDPR compliance)")



if __name__ == '__main__':
    tornado.testing.main()
