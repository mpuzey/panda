import unittest
from unittest.mock import Mock, MagicMock, patch
from src.service.appointment_service import AppointmentService
from constants import (
    ERR_COULD_NOT_CREATE_APPOINTMENT,
    ERR_COULD_NOT_UPDATE_APPOINTMENT,
    ERR_APPOINTMENT_NOT_FOUND,
    MSG_NEW_APPOINTMENT_ADDED,
    MSG_APPOINTMENT_UPDATED,
    MSG_APPOINTMENT_CANCELLED,
    HTTP_201_CREATED,
    HTTP_200_OK,
    APPOINTMENT_SERVICE_FIELD_ERROR,
    APPOINTMENT_SERVICE_FIELD_VALIDATION_ERRORS,
    APPOINTMENT_SERVICE_FIELD_STATUS,
    APPOINTMENT_SERVICE_FIELD_MESSAGE,
    APPOINTMENT_SERVICE_FIELD_APPOINTMENT
)


class TestAppointmentService(unittest.TestCase):
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
        self.mock_mongo_client = Mock()
        self.mock_mongo_database = Mock()

        # Mock the MongoDB class to return our mock database
        with patch('src.service.appointment_service.MongoDB') as mock_mongo_class:
            mock_mongo_class.return_value = self.mock_mongo_database
            self.appointment_service = AppointmentService(self.mock_mongo_client)

    def test_create_appointment_success(self):
        """Test successful appointment creation."""
        self.mock_mongo_database.create.return_value.acknowledged = True
        
        response = self.appointment_service.create_appointment(self.valid_appointment, '01542f70-929f-4c9a-b4fa-e672310d7e78')
        
        self.assertEqual(response[APPOINTMENT_SERVICE_FIELD_STATUS], HTTP_201_CREATED)
        self.assertEqual(response[APPOINTMENT_SERVICE_FIELD_MESSAGE], MSG_NEW_APPOINTMENT_ADDED.format('01542f70-929f-4c9a-b4fa-e672310d7e78'))
        self.mock_mongo_database.create.assert_called_once_with(self.valid_appointment)

    def test_create_appointment_validation_error(self):
        """Test appointment creation with validation errors."""
        invalid_appointment = self.valid_appointment.copy()
        invalid_appointment['status'] = 'invalid_status'
        
        response = self.appointment_service.create_appointment(invalid_appointment, '01542f70-929f-4c9a-b4fa-e672310d7e78')
        
        self.assertEqual(response[APPOINTMENT_SERVICE_FIELD_STATUS], 400)
        assert APPOINTMENT_SERVICE_FIELD_ERROR in response
        assert 'Invalid' in response[APPOINTMENT_SERVICE_FIELD_ERROR][0]

    def test_create_appointment_database_error(self):
        """Test appointment creation when database operation fails."""
        self.mock_mongo_database.create.return_value.acknowledged = False
        
        response = self.appointment_service.create_appointment(self.valid_appointment, '01542f70-929f-4c9a-b4fa-e672310d7e78')
        
        self.assertEqual(response['status'], 500)
        self.assertEqual(response['error'], ERR_COULD_NOT_CREATE_APPOINTMENT)

    def test_update_appointment_success(self):
        """Test successful appointment update."""
        self.mock_mongo_database.update.return_value.acknowledged = True
        
        response = self.appointment_service.update_appointment(self.valid_appointment, '01542f70-929f-4c9a-b4fa-e672310d7e78')
        
        self.assertEqual(response[APPOINTMENT_SERVICE_FIELD_STATUS], HTTP_200_OK)
        self.assertEqual(response[APPOINTMENT_SERVICE_FIELD_MESSAGE], MSG_APPOINTMENT_UPDATED.format('01542f70-929f-4c9a-b4fa-e672310d7e78'))
        self.mock_mongo_database.update.assert_called_once_with({'id': '01542f70-929f-4c9a-b4fa-e672310d7e78'}, self.valid_appointment)

    def test_update_appointment_validation_error(self):
        """Test appointment update with validation errors."""
        invalid_appointment = self.valid_appointment.copy()
        invalid_appointment['clinician'] = 'Dr'  # Too short
        
        response = self.appointment_service.update_appointment(invalid_appointment, '01542f70-929f-4c9a-b4fa-e672310d7e78')
        
        self.assertEqual(response[APPOINTMENT_SERVICE_FIELD_STATUS], 400)
        assert APPOINTMENT_SERVICE_FIELD_VALIDATION_ERRORS in response
        assert 'Invalid' in response[APPOINTMENT_SERVICE_FIELD_VALIDATION_ERRORS][0]

    def test_update_appointment_database_error(self):
        """Test appointment update when database operation fails."""
        self.mock_mongo_database.update.return_value.acknowledged = False
        
        response = self.appointment_service.update_appointment(self.valid_appointment, '01542f70-929f-4c9a-b4fa-e672310d7e78')
        
        self.assertEqual(response[APPOINTMENT_SERVICE_FIELD_STATUS], 500)
        self.assertEqual(response[APPOINTMENT_SERVICE_FIELD_ERROR], ERR_COULD_NOT_UPDATE_APPOINTMENT)

    def test_get_appointment_success(self):
        """Test successful appointment retrieval."""
        self.mock_mongo_database.get.return_value = self.valid_appointment
        
        response = self.appointment_service.get_appointment('01542f70-929f-4c9a-b4fa-e672310d7e78')
        
        self.assertEqual(response[APPOINTMENT_SERVICE_FIELD_STATUS], HTTP_200_OK)
        self.assertEqual(response[APPOINTMENT_SERVICE_FIELD_APPOINTMENT], {
            'patient': self.valid_appointment['patient'],
            'status': self.valid_appointment['status'],
            'time': self.valid_appointment['time'],
            'duration': self.valid_appointment['duration'],
            'clinician': self.valid_appointment['clinician'],
            'department': self.valid_appointment['department'],
            'postcode': self.valid_appointment['postcode'],
            'id': self.valid_appointment['id']
        })
        self.mock_mongo_database.get.assert_called_once_with({'id': '01542f70-929f-4c9a-b4fa-e672310d7e78'})

    def test_get_appointment_not_found(self):
        """Test appointment retrieval when appointment doesn't exist."""
        self.mock_mongo_database.get.return_value = None
        
        response = self.appointment_service.get_appointment('01542f70-929f-4c9a-b4fa-e672310d7e78')
        
        self.assertEqual(response[APPOINTMENT_SERVICE_FIELD_STATUS], 404)
        self.assertEqual(response[APPOINTMENT_SERVICE_FIELD_ERROR], ERR_APPOINTMENT_NOT_FOUND)

    def test_delete_appointment_success(self):
        """Test successful appointment deletion."""
        self.mock_mongo_database.delete.return_value.deleted_count = 1
        
        response = self.appointment_service.delete_appointment('01542f70-929f-4c9a-b4fa-e672310d7e78')
        
        self.assertEqual(response['status'], HTTP_200_OK)
        self.assertEqual(response['message'], MSG_APPOINTMENT_CANCELLED.format('01542f70-929f-4c9a-b4fa-e672310d7e78'))
        self.mock_mongo_database.delete.assert_called_once_with({'id': '01542f70-929f-4c9a-b4fa-e672310d7e78'})

    def test_delete_appointment_not_found(self):
        """Test appointment deletion when appointment doesn't exist."""
        self.mock_mongo_database.delete.return_value.deleted_count = 0
        
        response = self.appointment_service.delete_appointment('01542f70-929f-4c9a-b4fa-e672310d7e78')
        
        self.assertEqual(response['status'], 404)
        self.assertEqual(response['error'], ERR_APPOINTMENT_NOT_FOUND)

    def test_get_all_appointments_success(self):
        """Test successful retrieval of all appointments."""
        mock_appointments = [
            {
                'patient': '1953262716',
                'status': 'active',
                'time': '2025-06-04T16:30:00+01:00',
                'duration': '1h',
                'clinician': 'Bethany Rice-Hammond',
                'department': 'oncology',
                'postcode': 'IM2N 4LG',
                'id': '01542f70-929f-4c9a-b4fa-e672310d7e78'
            },
            {
                'patient': '1953262717',
                'status': 'attended',
                'time': '2025-06-05T10:00:00+01:00',
                'duration': '30m',
                'clinician': 'Dr Smith',
                'department': 'cardiology',
                'postcode': 'SW1A 1AA',
                'id': '01542f70-929f-4c9a-b4fa-e672310d7e79'
            }
        ]
        self.mock_mongo_database.getAll.return_value = mock_appointments
        
        response = self.appointment_service.get_all_appointments()
        
        self.assertEqual(response['status'], HTTP_200_OK)
        self.assertEqual(response['appointments'], mock_appointments)
        self.mock_mongo_database.getAll.assert_called_once()

    def test_get_all_appointments_empty(self):
        """Test retrieval of all appointments when no appointments exist."""
        self.mock_mongo_database.getAll.return_value = []
        
        response = self.appointment_service.get_all_appointments()
        
        self.assertEqual(response['status'], HTTP_200_OK)
        self.assertEqual(response['appointments'], [])
        self.mock_mongo_database.getAll.assert_called_once()


if __name__ == '__main__':
    unittest.main() 