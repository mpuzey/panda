import unittest
from unittest.mock import Mock, MagicMock, patch
from src.service.appointment_service import AppointmentService
from src.service.results import ResultType
from constants import (
    ERR_COULD_NOT_CREATE_APPOINTMENT,
    ERR_COULD_NOT_UPDATE_APPOINTMENT,
    ERR_APPOINTMENT_NOT_FOUND,
    MSG_NEW_APPOINTMENT_ADDED,
    MSG_APPOINTMENT_UPDATED,
    MSG_APPOINTMENT_CANCELLED,
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
        
        self.assertEqual(response.result_type, ResultType.SUCCESS)
        self.assertEqual(response.message, MSG_NEW_APPOINTMENT_ADDED.format('01542f70-929f-4c9a-b4fa-e672310d7e78'))
        self.mock_mongo_database.create.assert_called_once_with(self.valid_appointment)

    def test_create_appointment_validation_error(self):
        """Test appointment creation with validation errors."""
        invalid_appointment = self.valid_appointment.copy()
        invalid_appointment['status'] = 'invalid_status'
        
        response = self.appointment_service.create_appointment(invalid_appointment, '01542f70-929f-4c9a-b4fa-e672310d7e78')
        
        self.assertEqual(response.result_type, ResultType.VALIDATION_ERROR)
        assert 'Invalid' in response.errors[0]

    def test_create_appointment_database_error(self):
        """Test appointment creation when database operation fails."""
        self.mock_mongo_database.create.return_value.acknowledged = False
        
        response = self.appointment_service.create_appointment(self.valid_appointment, '01542f70-929f-4c9a-b4fa-e672310d7e78')
        
        self.assertEqual(response.result_type, ResultType.DATABASE_ERROR)
        self.assertEqual(response.errors[0], ERR_COULD_NOT_CREATE_APPOINTMENT)

    def test_create_appointment_cancelled_appointment_cannot_be_reinstated(self):
        """Test a cancelled appointment cannot be recreated."""
        cancelled_appointment = self.valid_appointment
        cancelled_appointment['status'] = 'cancelled'
        self.mock_mongo_database.get.return_value = cancelled_appointment
        self.mock_mongo_database.update.return_value.acknowledged = True
        response = self.appointment_service.create_appointment(self.valid_appointment, '01542f70-929f-4c9a-b4fa-e672310d7e78')

        self.assertEqual(response.result_type, ResultType.BUSINESS_ERROR)
        self.assertEqual(response.errors[0], ERR_COULD_NOT_UPDATE_APPOINTMENT)
        self.mock_mongo_database.update.assert_not_called()

    def test_update_appointment_success(self):
        """Test successful appointment update."""
        self.mock_mongo_database.update.return_value.acknowledged = True
        
        response = self.appointment_service.update_appointment(self.valid_appointment, '01542f70-929f-4c9a-b4fa-e672310d7e78')
        
        self.assertEqual(response.result_type, ResultType.SUCCESS)
        self.assertEqual(response.message, MSG_APPOINTMENT_UPDATED.format('01542f70-929f-4c9a-b4fa-e672310d7e78'))
        self.mock_mongo_database.update.assert_called_once_with({'id': '01542f70-929f-4c9a-b4fa-e672310d7e78'}, self.valid_appointment)

    def test_update_appointment_validation_error(self):
        """Test appointment update with validation errors."""
        invalid_appointment = self.valid_appointment.copy()
        invalid_appointment['status'] = 'invalid_status'
        
        response = self.appointment_service.update_appointment(invalid_appointment, '01542f70-929f-4c9a-b4fa-e672310d7e78')
        
        self.assertEqual(response.result_type, ResultType.VALIDATION_ERROR)
        assert 'Invalid' in response.errors[0]

    def test_update_appointment_database_error(self):
        """Test appointment update when database operation fails."""
        self.mock_mongo_database.update.return_value.acknowledged = False
        
        response = self.appointment_service.update_appointment(self.valid_appointment, '01542f70-929f-4c9a-b4fa-e672310d7e78')
        
        self.assertEqual(response.result_type, ResultType.DATABASE_ERROR)
        self.assertEqual(response.errors[0], ERR_COULD_NOT_UPDATE_APPOINTMENT)

    def test_update_appointment_cancelled_appointment_cannot_be_reinstated(self):
        """Test that a cancelled appointment cannot be reinstated with an update."""

        cancelled_appointment = self.valid_appointment
        cancelled_appointment['status'] = 'cancelled'
        self.mock_mongo_database.get.return_value = cancelled_appointment
        self.mock_mongo_database.update.return_value.acknowledged = True

        response = self.appointment_service.update_appointment(self.valid_appointment,
                                                               '01542f70-929f-4c9a-b4fa-e672310d7e78')

        self.assertEqual(response.result_type, ResultType.BUSINESS_ERROR)
        self.assertEqual(response.errors[0], ERR_COULD_NOT_UPDATE_APPOINTMENT)
        self.mock_mongo_database.update.assert_not_called()

    def test_get_appointment_success(self):
        """Test successful appointment retrieval."""
        self.mock_mongo_database.get.return_value = self.valid_appointment
        
        response = self.appointment_service.get_appointment('01542f70-929f-4c9a-b4fa-e672310d7e78')
        
        self.assertEqual(response.result_type, ResultType.SUCCESS)
        self.assertEqual(response.data, {
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
        
        self.assertEqual(response.result_type, ResultType.NOT_FOUND)
        self.assertEqual(response.errors[0], ERR_APPOINTMENT_NOT_FOUND)

    def test_delete_appointment_success(self):
        """Test successful appointment deletion."""
        self.mock_mongo_database.delete.return_value.deleted_count = 1
        
        response = self.appointment_service.delete_appointment('01542f70-929f-4c9a-b4fa-e672310d7e78')
        
        self.assertEqual(response.result_type, ResultType.SUCCESS)
        self.assertEqual(response.message, MSG_APPOINTMENT_CANCELLED.format('01542f70-929f-4c9a-b4fa-e672310d7e78'))
        self.mock_mongo_database.delete.assert_called_once_with({'id': '01542f70-929f-4c9a-b4fa-e672310d7e78'})

    def test_delete_appointment_not_found(self):
        """Test appointment deletion when appointment doesn't exist."""
        self.mock_mongo_database.delete.return_value.deleted_count = 0
        
        response = self.appointment_service.delete_appointment('01542f70-929f-4c9a-b4fa-e672310d7e78')
        
        self.assertEqual(response.result_type, ResultType.NOT_FOUND)
        self.assertEqual(response.errors[0], ERR_APPOINTMENT_NOT_FOUND)

    def test_get_all_appointments_success(self):
        """Test successful retrieval of all appointments."""
        mock_appointments = [self.valid_appointment]
        self.mock_mongo_database.getAll.return_value = mock_appointments
        
        response = self.appointment_service.get_all_appointments()
        
        self.assertEqual(response.result_type, ResultType.SUCCESS)
        self.assertEqual(response.data, mock_appointments)
        self.mock_mongo_database.getAll.assert_called_once()


if __name__ == '__main__':
    unittest.main() 