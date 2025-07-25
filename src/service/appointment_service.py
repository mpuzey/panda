from src.repository.appointment import AppointmentRepository
from src.service.results import ServiceResponse, ResponseType

from constants import (
    APPOINTMENT_FIELD_STATUS,
    ERR_COULD_NOT_CREATE_APPOINTMENT,
    ERR_COULD_NOT_UPDATE_APPOINTMENT,
    ERR_APPOINTMENT_NOT_FOUND,
    MSG_NEW_APPOINTMENT_ADDED,
    MSG_APPOINTMENT_UPDATED,
    MSG_APPOINTMENT_CANCELLED,
    STATUS_CANCELLED,
)
from src.service.appointment_validation import validate


class AppointmentService:

    def __init__(self, appointment_repository: AppointmentRepository):
        """Initialize AppointmentService with an appointment repository.

        Args:
            appointment_repository: Repository instance for appointment data access
        """
        self.appointment_repository = appointment_repository

    def create_appointment(self, appointment, appointment_id):
        """Create a new appointment with validation."""
        errors = validate(appointment)
        if errors:
            return ServiceResponse(ResponseType.VALIDATION_ERROR, errors=errors)

        # Check if appointment already exists
        existing_appointment = self.get_appointment(appointment_id)
        if existing_appointment.response_type == ResponseType.SUCCESS:
            # Appointment exists, check if it's cancelled
            status = existing_appointment.data.get(APPOINTMENT_FIELD_STATUS)
            if status == STATUS_CANCELLED:
                return ServiceResponse(ResponseType.BUSINESS_ERROR, errors=[ERR_COULD_NOT_UPDATE_APPOINTMENT])
            else:
                return ServiceResponse(ResponseType.BUSINESS_ERROR, errors=[ERR_COULD_NOT_CREATE_APPOINTMENT])

        success = self.appointment_repository.create(appointment)
        if not success:
            return ServiceResponse(ResponseType.DATABASE_ERROR, errors=[ERR_COULD_NOT_CREATE_APPOINTMENT])

        return ServiceResponse(
            ResponseType.SUCCESS,
            message=MSG_NEW_APPOINTMENT_ADDED.format(appointment_id)
        )

    def update_appointment(self, appointment, appointment_id):
        """Update an existing appointment with validation."""
        errors = validate(appointment)
        if errors:
            return ServiceResponse(ResponseType.VALIDATION_ERROR, errors=errors)

        get_service_response = self.prevent_cancelled_appointment_from_being_updated(appointment_id)
        if get_service_response.response_type == ResponseType.BUSINESS_ERROR:
            return get_service_response

        success = self.appointment_repository.update_by_id(appointment_id, appointment)
        if not success:
            return ServiceResponse(ResponseType.DATABASE_ERROR, errors=[ERR_COULD_NOT_UPDATE_APPOINTMENT])

        return ServiceResponse(
            ResponseType.SUCCESS,
            message=MSG_APPOINTMENT_UPDATED.format(appointment_id)
        )

    def get_appointment(self, appointment_id):
        """Get an appointment by ID."""
        appointment_data = self.appointment_repository.get_by_id(appointment_id)
        if not appointment_data:
            return ServiceResponse(ResponseType.NOT_FOUND, errors=[ERR_APPOINTMENT_NOT_FOUND])

        return ServiceResponse(ResponseType.SUCCESS, data=appointment_data)

    def delete_appointment(self, appointment_id):
        """Delete an appointment by ID."""
        cancelled_appointment = {APPOINTMENT_FIELD_STATUS: STATUS_CANCELLED}
        success = self.appointment_repository.update_by_id(appointment_id, cancelled_appointment)
        if not success:
            return ServiceResponse(ResponseType.NOT_FOUND, errors=[ERR_APPOINTMENT_NOT_FOUND])

        return ServiceResponse(
            ResponseType.SUCCESS,
            message=MSG_APPOINTMENT_CANCELLED.format(appointment_id)
        )

    def get_all_appointments(self):
        """Get all appointments."""
        appointments = self.appointment_repository.get_all()
        return ServiceResponse(ResponseType.SUCCESS, data=appointments)

    def prevent_cancelled_appointment_from_being_updated(self, appointment_id):
        """Prevent a cancelled appointment from being updated."""
        get_response = self.get_appointment(appointment_id)
        if get_response.response_type == ResponseType.SUCCESS:
            status = get_response.data.get(APPOINTMENT_FIELD_STATUS)
            if status == STATUS_CANCELLED:
                return ServiceResponse(ResponseType.BUSINESS_ERROR, errors=[ERR_COULD_NOT_UPDATE_APPOINTMENT])
        return ServiceResponse(ResponseType.SUCCESS)
