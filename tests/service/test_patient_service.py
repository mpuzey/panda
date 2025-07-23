import unittest
from unittest.mock import Mock, MagicMock, patch
from src.service.patient_service import PatientService
from constants import (
    ERR_COULD_NOT_CREATE_PATIENT,
    ERR_COULD_NOT_UPDATE_PATIENT,
    ERR_PATIENT_NOT_FOUND,
    MSG_NEW_PATIENT_ADDED,
    MSG_PATIENT_UPDATED,
    MSG_PATIENT_DELETED,
    HTTP_201_CREATED,
    HTTP_200_OK,
    PATIENT_SERVICE_FIELD_STATUS,
    PATIENT_SERVICE_FIELD_ERROR,
    PATIENT_SERVICE_FIELD_MESSAGE,
    PATIENT_SERVICE_FIELD_PATIENT,
    PATIENT_SERVICE_FIELD_PATIENTS,
    PATIENT_SERVICE_FIELD_VALIDATION_ERRORS
)


class TestPatientService(unittest.TestCase):
    def setUp(self):
        self.valid_patient = {
            'nhs_number': '1373645350',
            'name': 'Dr Glenn Clark',
            'date_of_birth': '1996-02-01',
            'postcode': 'N6 2FA'
        }
        self.mock_mongo_client = Mock()
        self.mock_mongo_database = Mock()

        # Mock the MongoDB class to return our mock database
        with patch('src.service.patient_service.MongoDB') as mock_mongo_class:
            mock_mongo_class.return_value = self.mock_mongo_database
            self.patient_service = PatientService(self.mock_mongo_client)

    def test_create_patient_success(self):
        """Test successful patient creation."""
        self.mock_mongo_database.create.return_value.acknowledged = True
        
        response = self.patient_service.create_patient(self.valid_patient, '1373645350')
        
        self.assertEqual(response[PATIENT_SERVICE_FIELD_STATUS], HTTP_201_CREATED)
        self.assertEqual(response[PATIENT_SERVICE_FIELD_MESSAGE], MSG_NEW_PATIENT_ADDED.format('1373645350'))
        self.mock_mongo_database.create.assert_called_once_with(self.valid_patient)

    def test_create_patient_validation_error(self):
        """Test patient creation with validation errors."""
        invalid_patient = self.valid_patient.copy()
        invalid_patient['nhs_number'] = 'invalid'
        
        response = self.patient_service.create_patient(invalid_patient, '1373645350')
        
        self.assertEqual(response[PATIENT_SERVICE_FIELD_STATUS], 400)
        assert PATIENT_SERVICE_FIELD_VALIDATION_ERRORS in response
        assert 'Invalid NHS number' in response[PATIENT_SERVICE_FIELD_VALIDATION_ERRORS][0]

    def test_create_patient_database_error(self):
        """Test patient creation when database operation fails."""
        self.mock_mongo_database.create.return_value.acknowledged = False
        
        response = self.patient_service.create_patient(self.valid_patient, '1373645350')
        
        self.assertEqual(response[PATIENT_SERVICE_FIELD_STATUS], 500)
        self.assertEqual(response[PATIENT_SERVICE_FIELD_ERROR], ERR_COULD_NOT_CREATE_PATIENT)

    def test_update_patient_success(self):
        """Test successful patient update."""
        self.mock_mongo_database.update.return_value.acknowledged = True
        
        response = self.patient_service.update_patient(self.valid_patient, '1373645350')
        
        self.assertEqual(response[PATIENT_SERVICE_FIELD_STATUS], HTTP_200_OK)
        self.assertEqual(response[PATIENT_SERVICE_FIELD_MESSAGE], MSG_PATIENT_UPDATED.format('1373645350'))
        self.mock_mongo_database.update.assert_called_once_with({'nhs_number': '1373645350'}, self.valid_patient)

    def test_update_patient_validation_error(self):
        """Test patient update with validation errors."""
        invalid_patient = self.valid_patient.copy()
        invalid_patient['name'] = 'AB'  # Too short
        
        response = self.patient_service.update_patient(invalid_patient, '1373645350')
        
        self.assertEqual(response[PATIENT_SERVICE_FIELD_STATUS], 400)
        assert PATIENT_SERVICE_FIELD_VALIDATION_ERRORS in response
        assert 'Invalid name' in response[PATIENT_SERVICE_FIELD_VALIDATION_ERRORS][0]

    def test_update_patient_database_error(self):
        """Test patient update when database operation fails."""
        self.mock_mongo_database.update.return_value.acknowledged = False
        
        response = self.patient_service.update_patient(self.valid_patient, '1373645350')
        
        self.assertEqual(response[PATIENT_SERVICE_FIELD_STATUS], 500)
        self.assertEqual(response[PATIENT_SERVICE_FIELD_ERROR], ERR_COULD_NOT_UPDATE_PATIENT)

    def test_get_patient_success(self):
        """Test successful patient retrieval."""
        self.mock_mongo_database.get.return_value = self.valid_patient
        
        response = self.patient_service.get_patient('1373645350')
        
        self.assertEqual(response[PATIENT_SERVICE_FIELD_STATUS], HTTP_200_OK)
        self.assertEqual(response[PATIENT_SERVICE_FIELD_PATIENT], self.valid_patient)
        self.mock_mongo_database.get.assert_called_once_with({'nhs_number': '1373645350'})

    def test_get_patient_not_found(self):
        """Test patient retrieval when patient doesn't exist."""
        self.mock_mongo_database.get.return_value = None
        
        response = self.patient_service.get_patient('1373645350')
        
        self.assertEqual(response[PATIENT_SERVICE_FIELD_STATUS], 404)
        self.assertEqual(response[PATIENT_SERVICE_FIELD_ERROR], ERR_PATIENT_NOT_FOUND)

    def test_delete_patient_success(self):
        """Test successful patient deletion."""
        self.mock_mongo_database.delete.return_value.deleted_count = 1
        
        response = self.patient_service.delete_patient('1373645350')
        
        self.assertEqual(response[PATIENT_SERVICE_FIELD_STATUS], HTTP_200_OK)
        self.assertEqual(response[PATIENT_SERVICE_FIELD_MESSAGE], MSG_PATIENT_DELETED.format('1373645350'))
        self.mock_mongo_database.delete.assert_called_once_with({'nhs_number': '1373645350'})

    def test_delete_patient_not_found(self):
        """Test patient deletion when patient doesn't exist."""
        self.mock_mongo_database.delete.return_value.deleted_count = 0
        
        response = self.patient_service.delete_patient('1373645350')
        
        self.assertEqual(response[PATIENT_SERVICE_FIELD_STATUS], 500)
        self.assertEqual(response[PATIENT_SERVICE_FIELD_ERROR], ERR_PATIENT_NOT_FOUND)

    def test_get_all_patients_success(self):
        """Test successful retrieval of all patients."""
        mock_patients = [
            {
                'nhs_number': '1373645350',
                'name': 'Dr Glenn Clark',
                'date_of_birth': '1996-02-01',
                'postcode': 'N6 2FA'
            },
            {
                'nhs_number': '1373645351',
                'name': 'Dr M Puzey',
                'date_of_birth': '1985-03-15',
                'postcode': 'SW1A 1AA'
            }
        ]
        self.mock_mongo_database.getAll.return_value = mock_patients
        
        response = self.patient_service.get_all_patients()
        
        self.assertEqual(response[PATIENT_SERVICE_FIELD_STATUS], HTTP_200_OK)
        self.assertEqual(response[PATIENT_SERVICE_FIELD_PATIENTS], mock_patients)
        self.mock_mongo_database.getAll.assert_called_once()

    def test_get_all_patients_empty(self):
        """Test retrieval of all patients when no patients exist."""
        self.mock_mongo_database.getAll.return_value = []
        
        response = self.patient_service.get_all_patients()
        
        self.assertEqual(response[PATIENT_SERVICE_FIELD_STATUS], HTTP_200_OK)
        self.assertEqual(response[PATIENT_SERVICE_FIELD_PATIENTS], [])
        self.mock_mongo_database.getAll.assert_called_once()


if __name__ == '__main__':
    unittest.main() 