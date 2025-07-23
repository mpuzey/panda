from src.db.mongo import MongoDB
from src.service.result_types import ServiceResult, ResultType

from constants import (
    ERR_COULD_NOT_CREATE_APPOINTMENT,
    ERR_COULD_NOT_UPDATE_APPOINTMENT,
    ERR_APPOINTMENT_NOT_FOUND,
    MSG_NEW_APPOINTMENT_ADDED,
    MSG_APPOINTMENT_UPDATED,
    MSG_APPOINTMENT_CANCELLED,
    MONGODB_COLLECTION_APPOINTMENTS,
    APPOINTMENT_FIELD_ID,
)
from src.service.appointment_validation import validate


class AppointmentService:

    def __init__(self, mongo_database_client):
        self.mongo_database = MongoDB(mongo_database_client, MONGODB_COLLECTION_APPOINTMENTS)

    def create_appointment(self, appointment, appointment_id):
        """Create a new appointment with validation."""
        errors = validate(appointment)
        if errors:
            return ServiceResult(ResultType.VALIDATION_ERROR, errors=errors)

        result = self.mongo_database.create(appointment)
        if not result.acknowledged:
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

        result = self.mongo_database.update({APPOINTMENT_FIELD_ID: appointment_id}, appointment)
        if not result.acknowledged:
            return ServiceResult(ResultType.DATABASE_ERROR, errors=[ERR_COULD_NOT_UPDATE_APPOINTMENT])

        return ServiceResult(
            ResultType.SUCCESS,
            message=MSG_APPOINTMENT_UPDATED.format(appointment_id)
        )

    def get_appointment(self, appointment_id):
        """Get an appointment by ID."""
        result = self.mongo_database.get({APPOINTMENT_FIELD_ID: appointment_id})
        if not result:
            return ServiceResult(ResultType.NOT_FOUND, errors=[ERR_APPOINTMENT_NOT_FOUND])

        return ServiceResult(
            ResultType.SUCCESS,
            data={
                'patient': result.get('patient'),
                'status': result.get('status'),
                'time': result.get('time'),
                'duration': result.get('duration'),
                'clinician': result.get('clinician'),
                'department': result.get('department'),
                'postcode': result.get('postcode'),
                'id': result.get('id')
            }
        )

    def delete_appointment(self, appointment_id):
        """Delete an appointment by ID."""
        result = self.mongo_database.delete({APPOINTMENT_FIELD_ID: appointment_id})
        if not result.deleted_count:
            return ServiceResult(ResultType.NOT_FOUND, errors=[ERR_APPOINTMENT_NOT_FOUND])

        return ServiceResult(
            ResultType.SUCCESS,
            message=MSG_APPOINTMENT_CANCELLED.format(appointment_id)
        )

    def get_all_appointments(self):
        """Get all appointments."""
        appointments = self.mongo_database.getAll()
        return ServiceResult(ResultType.SUCCESS, data=appointments)
