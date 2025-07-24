from src.repository.appointment import AppointmentRepository
from src.service.results import ServiceResult, ResultType

from constants import (
    APPOINTMENT_FIELD_CLINICIAN,
    APPOINTMENT_FIELD_DEPARTMENT,
    APPOINTMENT_FIELD_DURATION,
    APPOINTMENT_FIELD_PATIENT,
    APPOINTMENT_FIELD_POSTCODE,
    APPOINTMENT_FIELD_TIME,
    APPOINTMENT_FIELD_STATUS,
    ERR_COULD_NOT_CREATE_APPOINTMENT,
    ERR_COULD_NOT_UPDATE_APPOINTMENT,
    ERR_APPOINTMENT_NOT_FOUND,
    MSG_NEW_APPOINTMENT_ADDED,
    MSG_APPOINTMENT_UPDATED,
    MSG_APPOINTMENT_CANCELLED,
    APPOINTMENT_FIELD_ID,
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
            return ServiceResult(ResultType.VALIDATION_ERROR, errors=errors)

        # Check if appointment already exists
        existing_appointment = self.get_appointment(appointment_id)
        if existing_appointment.result_type == ResultType.SUCCESS:
            # Appointment exists, check if it's cancelled
            status = existing_appointment.data.get(APPOINTMENT_FIELD_STATUS)
            if status == STATUS_CANCELLED:
                return ServiceResult(ResultType.BUSINESS_ERROR, errors=[ERR_COULD_NOT_UPDATE_APPOINTMENT])
            else:
                return ServiceResult(ResultType.BUSINESS_ERROR, errors=[ERR_COULD_NOT_CREATE_APPOINTMENT])

        success = self.appointment_repository.create(appointment)
        if not success:
            return ServiceResult(ResultType.DATABASE_ERROR, errors=[ERR_COULD_NOT_CREATE_APPOINTMENT])

        return ServiceResult(
            ResultType.SUCCESS,
            message=MSG_NEW_APPOINTMENT_ADDED.format(appointment_id)
        )

    def update_appointment(self, appointment, appointment_id):
        """Update an existing appointment with validation."""
        errors = validate(appointment)
        if errors:
            return ServiceResult(ResultType.VALIDATION_ERROR, errors=errors)

        get_service_result = self.prevent_cancelled_appointment_from_being_updated(appointment_id)
        if get_service_result.result_type == ResultType.BUSINESS_ERROR:
            return get_service_result

        success = self.appointment_repository.update_by_id(appointment_id, appointment)
        if not success:
            return ServiceResult(ResultType.DATABASE_ERROR, errors=[ERR_COULD_NOT_UPDATE_APPOINTMENT])

        return ServiceResult(
            ResultType.SUCCESS,
            message=MSG_APPOINTMENT_UPDATED.format(appointment_id)
        )

    def get_appointment(self, appointment_id):
        """Get an appointment by ID."""
        appointment_data = self.appointment_repository.get_by_id(appointment_id)
        if not appointment_data:
            return ServiceResult(ResultType.NOT_FOUND, errors=[ERR_APPOINTMENT_NOT_FOUND])

        return ServiceResult(
            ResultType.SUCCESS,
            # TODO: Convert BSON to JSON (move to mongo layer)
            data={
                APPOINTMENT_FIELD_PATIENT: appointment_data.get(APPOINTMENT_FIELD_PATIENT),
                APPOINTMENT_FIELD_STATUS: appointment_data.get(APPOINTMENT_FIELD_STATUS),
                APPOINTMENT_FIELD_TIME: appointment_data.get(APPOINTMENT_FIELD_TIME),
                APPOINTMENT_FIELD_DURATION: appointment_data.get(APPOINTMENT_FIELD_DURATION),
                APPOINTMENT_FIELD_CLINICIAN: appointment_data.get(APPOINTMENT_FIELD_CLINICIAN),
                APPOINTMENT_FIELD_DEPARTMENT: appointment_data.get(APPOINTMENT_FIELD_DEPARTMENT),
                APPOINTMENT_FIELD_POSTCODE: appointment_data.get(APPOINTMENT_FIELD_POSTCODE),
                APPOINTMENT_FIELD_ID: appointment_data.get(APPOINTMENT_FIELD_ID)
            }
        )

    def delete_appointment(self, appointment_id):
        """Delete an appointment by ID."""
        cancelled_appointment = {APPOINTMENT_FIELD_STATUS: STATUS_CANCELLED}
        success = self.appointment_repository.update_by_id(appointment_id, cancelled_appointment)
        if not success:
            return ServiceResult(ResultType.NOT_FOUND, errors=[ERR_APPOINTMENT_NOT_FOUND])

        return ServiceResult(
            ResultType.SUCCESS,
            message=MSG_APPOINTMENT_CANCELLED.format(appointment_id)
        )

    def get_all_appointments(self):
        """Get all appointments."""
        appointments = self.appointment_repository.get_all()
        return ServiceResult(ResultType.SUCCESS, data=appointments)

    def prevent_cancelled_appointment_from_being_updated(self, appointment_id):
        """Prevent a cancelled appointment from being updated."""
        get_result = self.get_appointment(appointment_id)
        if get_result.result_type == ResultType.SUCCESS:
            status = get_result.data.get(APPOINTMENT_FIELD_STATUS)
            if status == STATUS_CANCELLED:
                return ServiceResult(ResultType.BUSINESS_ERROR, errors=[ERR_COULD_NOT_UPDATE_APPOINTMENT])
        return ServiceResult(ResultType.SUCCESS)
