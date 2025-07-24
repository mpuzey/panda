import unittest
from unittest.mock import Mock
from src.service.patient_service import PatientService
from src.service.results import ResponseType
from constants import (
    ERR_COULD_NOT_CREATE_PATIENT,
    ERR_COULD_NOT_UPDATE_PATIENT,
    ERR_PATIENT_NOT_FOUND,
    MSG_NEW_PATIENT_ADDED,
    MSG_PATIENT_UPDATED,
    MSG_PATIENT_DELETED,
)


class TestPatientService(unittest.TestCase):
    def setUp(self):
        self.valid_patient = {
            'nhs_number': '1373645350',
            'name': 'Dr Glenn Clark',
            'date_of_birth': '1996-02-01',
            'postcode': 'N6 2FA'
        }
        # Create a mock repository instead of mocking MongoDB directly
        self.mock_patient_repository = Mock()
        self.patient_service = PatientService(self.mock_patient_repository)

    def test_create_patient_success(self):
        """Test successful patient creation."""
        self.mock_patient_repository.create.return_value = True
        
        response = self.patient_service.create_patient(self.valid_patient, '1373645350')
        
        self.assertEqual(response.response_type, ResponseType.SUCCESS)
        self.assertEqual(response.message, MSG_NEW_PATIENT_ADDED.format('1373645350'))
        self.mock_patient_repository.create.assert_called_once_with(self.valid_patient)

    def test_create_patient_validation_error(self):
        """Test patient creation with validation errors."""
        invalid_patient = self.valid_patient.copy()
        invalid_patient['nhs_number'] = 'invalid'
        
        response = self.patient_service.create_patient(invalid_patient, '1373645350')
        
        self.assertEqual(response.response_type, ResponseType.VALIDATION_ERROR)
        assert 'Invalid NHS number' in response.errors[0]

    def test_create_patient_database_error(self):
        """Test patient creation with database error."""
        self.mock_patient_repository.create.return_value = False
        
        response = self.patient_service.create_patient(self.valid_patient, '1373645350')
        
        self.assertEqual(response.response_type, ResponseType.DATABASE_ERROR)
        self.assertIn(ERR_COULD_NOT_CREATE_PATIENT, response.errors)

    def test_update_patient_success(self):
        """Test successful patient update."""
        self.mock_patient_repository.update_by_nhs_number.return_value = True
        
        response = self.patient_service.update_patient(self.valid_patient, '1373645350')
        
        self.assertEqual(response.response_type, ResponseType.SUCCESS)
        self.assertEqual(response.message, MSG_PATIENT_UPDATED.format('1373645350'))
        self.mock_patient_repository.update_by_nhs_number.assert_called_once_with('1373645350', self.valid_patient)

    def test_update_patient_validation_error(self):
        """Test patient update with validation errors."""
        invalid_patient = self.valid_patient.copy()
        invalid_patient['nhs_number'] = 'invalid'
        
        response = self.patient_service.update_patient(invalid_patient, '1373645350')
        
        self.assertEqual(response.response_type, ResponseType.VALIDATION_ERROR)
        assert 'Invalid NHS number' in response.errors[0]

    def test_update_patient_database_error(self):
        """Test patient update with database error."""
        self.mock_patient_repository.update_by_nhs_number.return_value = False
        
        response = self.patient_service.update_patient(self.valid_patient, '1373645350')
        
        self.assertEqual(response.response_type, ResponseType.DATABASE_ERROR)
        self.assertIn(ERR_COULD_NOT_UPDATE_PATIENT, response.errors)

    def test_get_patient_success(self):
        """Test successful patient retrieval."""
        self.mock_patient_repository.get_by_nhs_number.return_value = self.valid_patient
        
        response = self.patient_service.get_patient('1373645350')
        
        self.assertEqual(response.response_type, ResponseType.SUCCESS)
        self.assertEqual(response.data['nhs_number'], '1373645350')
        self.assertEqual(response.data['name'], 'Dr Glenn Clark')
        self.mock_patient_repository.get_by_nhs_number.assert_called_once_with('1373645350')

    def test_get_patient_not_found(self):
        """Test patient retrieval when patient not found."""
        self.mock_patient_repository.get_by_nhs_number.return_value = None
        
        response = self.patient_service.get_patient('1373645350')
        
        self.assertEqual(response.response_type, ResponseType.NOT_FOUND)
        self.assertIn(ERR_PATIENT_NOT_FOUND, response.errors)

    def test_delete_patient_success(self):
        """Test successful patient deletion."""
        self.mock_patient_repository.delete_by_nhs_number.return_value = True
        
        response = self.patient_service.delete_patient('1373645350')
        
        self.assertEqual(response.response_type, ResponseType.SUCCESS)
        self.assertEqual(response.message, MSG_PATIENT_DELETED.format('1373645350'))
        self.mock_patient_repository.delete_by_nhs_number.assert_called_once_with('1373645350')

    def test_delete_patient_not_found(self):
        """Test patient deletion when patient not found."""
        self.mock_patient_repository.delete_by_nhs_number.return_value = False
        
        response = self.patient_service.delete_patient('1373645350')
        
        self.assertEqual(response.response_type, ResponseType.NOT_FOUND)
        self.assertIn(ERR_PATIENT_NOT_FOUND, response.errors)

    def test_get_all_patients_success(self):
        """Test successful retrieval of all patients."""
        mock_patients = [self.valid_patient, self.valid_patient.copy()]
        self.mock_patient_repository.get_all.return_value = mock_patients
        
        response = self.patient_service.get_all_patients()
        
        self.assertEqual(response.response_type, ResponseType.SUCCESS)
        self.assertEqual(len(response.data), 2)
        self.mock_patient_repository.get_all.assert_called_once()


if __name__ == '__main__':
    unittest.main() 