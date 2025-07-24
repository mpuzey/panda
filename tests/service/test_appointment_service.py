import unittest
from unittest.mock import Mock
from src.service.appointment_service import AppointmentService
from src.service.results import ResultType
from constants import (
    ERR_COULD_NOT_CREATE_APPOINTMENT,
    ERR_COULD_NOT_UPDATE_APPOINTMENT,
    ERR_APPOINTMENT_NOT_FOUND,
    MSG_NEW_APPOINTMENT_ADDED,
    MSG_APPOINTMENT_UPDATED,
    MSG_APPOINTMENT_CANCELLED,
    STATUS_CANCELLED,
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
        # Create a mock repository instead of mocking MongoDB directly
        self.mock_appointment_repository = Mock()
        self.appointment_service = AppointmentService(self.mock_appointment_repository)

    def test_create_appointment_success(self):
        """Test successful appointment creation."""
        # Mock that appointment doesn't exist and creation succeeds
        self.mock_appointment_repository.get_by_id.return_value = None
        self.mock_appointment_repository.create.return_value = True
        
        response = self.appointment_service.create_appointment(self.valid_appointment, '01542f70-929f-4c9a-b4fa-e672310d7e78')
        
        self.assertEqual(response.result_type, ResultType.SUCCESS)
        self.assertEqual(response.message, MSG_NEW_APPOINTMENT_ADDED.format('01542f70-929f-4c9a-b4fa-e672310d7e78'))
        self.mock_appointment_repository.create.assert_called_once_with(self.valid_appointment)

    def test_create_appointment_validation_error(self):
        """Test appointment creation with validation errors."""
        invalid_appointment = self.valid_appointment.copy()
        invalid_appointment['status'] = 'invalid_status'
        
        response = self.appointment_service.create_appointment(invalid_appointment, '01542f70-929f-4c9a-b4fa-e672310d7e78')
        
        self.assertEqual(response.result_type, ResultType.VALIDATION_ERROR)
        assert 'Invalid' in response.errors[0]

    def test_create_appointment_database_error(self):
        """Test appointment creation with database error."""
        # Mock that appointment doesn't exist but creation fails
        self.mock_appointment_repository.get_by_id.return_value = None
        self.mock_appointment_repository.create.return_value = False
        
        response = self.appointment_service.create_appointment(self.valid_appointment, '01542f70-929f-4c9a-b4fa-e672310d7e78')
        
        self.assertEqual(response.result_type, ResultType.DATABASE_ERROR)
        self.assertIn(ERR_COULD_NOT_CREATE_APPOINTMENT, response.errors)

    def test_create_appointment_already_exists_active(self):
        """Test appointment creation when appointment already exists and is active."""
        existing_appointment = self.valid_appointment.copy()
        existing_appointment['status'] = 'active'
        self.mock_appointment_repository.get_by_id.return_value = existing_appointment

        response = self.appointment_service.create_appointment(self.valid_appointment, '01542f70-929f-4c9a-b4fa-e672310d7e78')

        self.assertEqual(response.result_type, ResultType.BUSINESS_ERROR)
        self.assertIn(ERR_COULD_NOT_CREATE_APPOINTMENT, response.errors)

    def test_create_appointment_cancelled_appointment_cannot_be_reinstated(self):
        """Test a cancelled appointment cannot be recreated."""
        cancelled_appointment = self.valid_appointment.copy()
        cancelled_appointment['status'] = STATUS_CANCELLED
        self.mock_appointment_repository.get_by_id.return_value = cancelled_appointment

        response = self.appointment_service.create_appointment(self.valid_appointment, '01542f70-929f-4c9a-b4fa-e672310d7e78')

        self.assertEqual(response.result_type, ResultType.BUSINESS_ERROR)
        self.assertEqual(response.errors[0], ERR_COULD_NOT_UPDATE_APPOINTMENT)
        self.mock_appointment_repository.create.assert_not_called()

    def test_update_appointment_success(self):
        """Test successful appointment update."""
        # Mock appointment exists and is not cancelled
        self.mock_appointment_repository.get_by_id.return_value = self.valid_appointment
        self.mock_appointment_repository.update_by_id.return_value = True
        
        response = self.appointment_service.update_appointment(self.valid_appointment, '01542f70-929f-4c9a-b4fa-e672310d7e78')
        
        self.assertEqual(response.result_type, ResultType.SUCCESS)
        self.assertEqual(response.message, MSG_APPOINTMENT_UPDATED.format('01542f70-929f-4c9a-b4fa-e672310d7e78'))

    def test_update_appointment_validation_error(self):
        """Test appointment update with validation errors."""
        invalid_appointment = self.valid_appointment.copy()
        invalid_appointment['status'] = 'invalid_status'
        
        response = self.appointment_service.update_appointment(invalid_appointment, '01542f70-929f-4c9a-b4fa-e672310d7e78')
        
        self.assertEqual(response.result_type, ResultType.VALIDATION_ERROR)

    def test_update_appointment_cancelled_appointment_cannot_be_reinstated(self):
        """Test that a cancelled appointment cannot be reinstated with an update."""
        cancelled_appointment = self.valid_appointment.copy()
        cancelled_appointment['status'] = STATUS_CANCELLED
        self.mock_appointment_repository.get_by_id.return_value = cancelled_appointment

        response = self.appointment_service.update_appointment(self.valid_appointment, '01542f70-929f-4c9a-b4fa-e672310d7e78')

        self.assertEqual(response.result_type, ResultType.BUSINESS_ERROR)
        self.assertEqual(response.errors[0], ERR_COULD_NOT_UPDATE_APPOINTMENT)
        self.mock_appointment_repository.update_by_id.assert_not_called()

    def test_get_appointment_success(self):
        """Test successful appointment retrieval."""
        self.mock_appointment_repository.get_by_id.return_value = self.valid_appointment
        
        response = self.appointment_service.get_appointment('01542f70-929f-4c9a-b4fa-e672310d7e78')
        
        self.assertEqual(response.result_type, ResultType.SUCCESS)
        self.assertEqual(response.data['id'], '01542f70-929f-4c9a-b4fa-e672310d7e78')

    def test_get_appointment_not_found(self):
        """Test appointment retrieval when appointment not found."""
        self.mock_appointment_repository.get_by_id.return_value = None
        
        response = self.appointment_service.get_appointment('01542f70-929f-4c9a-b4fa-e672310d7e78')
        
        self.assertEqual(response.result_type, ResultType.NOT_FOUND)
        self.assertIn(ERR_APPOINTMENT_NOT_FOUND, response.errors)

    def test_delete_appointment_success(self):
        """Test successful appointment deletion (cancellation)."""
        self.mock_appointment_repository.update_by_id.return_value = True
        
        response = self.appointment_service.delete_appointment('01542f70-929f-4c9a-b4fa-e672310d7e78')
        
        self.assertEqual(response.result_type, ResultType.SUCCESS)
        self.assertEqual(response.message, MSG_APPOINTMENT_CANCELLED.format('01542f70-929f-4c9a-b4fa-e672310d7e78'))

    def test_delete_appointment_not_found(self):
        """Test appointment deletion when appointment not found."""
        self.mock_appointment_repository.update_by_id.return_value = False
        
        response = self.appointment_service.delete_appointment('01542f70-929f-4c9a-b4fa-e672310d7e78')
        
        self.assertEqual(response.result_type, ResultType.NOT_FOUND)
        self.assertIn(ERR_APPOINTMENT_NOT_FOUND, response.errors)

    def test_get_all_appointments_success(self):
        """Test successful retrieval of all appointments."""
        mock_appointments = [self.valid_appointment, self.valid_appointment.copy()]
        self.mock_appointment_repository.get_all.return_value = mock_appointments
        
        response = self.appointment_service.get_all_appointments()
        
        self.assertEqual(response.result_type, ResultType.SUCCESS)
        self.assertEqual(len(response.data), 2)
        self.mock_appointment_repository.get_all.assert_called_once()


if __name__ == '__main__':
    unittest.main() 