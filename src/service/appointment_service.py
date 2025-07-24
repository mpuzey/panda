from re import A
from telnetlib import STATUS
from src.db.mongo import MongoDB
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
    MONGODB_COLLECTION_APPOINTMENTS,
    APPOINTMENT_FIELD_ID,   
    STATUS_CANCELLED,
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
        
        get_result = self.get_appointment(appointment_id)
        status = get_result.data.get(APPOINTMENT_FIELD_STATUS)
        if get_result.result_type == ResultType.SUCCESS and status == STATUS_CANCELLED:
            return ServiceResult(ResultType.BUSINESS_ERROR, errors=[ERR_COULD_NOT_UPDATE_APPOINTMENT])

        monogdb_response = self.mongo_database.update({APPOINTMENT_FIELD_ID: appointment_id}, appointment)
        if not monogdb_response.acknowledged:
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
            # Convert BSON to JSON (move to mongo layer)
            data={
                APPOINTMENT_FIELD_PATIENT: result.get(APPOINTMENT_FIELD_PATIENT),
                APPOINTMENT_FIELD_STATUS: result.get(APPOINTMENT_FIELD_STATUS),
                APPOINTMENT_FIELD_TIME: result.get(APPOINTMENT_FIELD_TIME),
                APPOINTMENT_FIELD_DURATION: result.get(APPOINTMENT_FIELD_DURATION),
                APPOINTMENT_FIELD_CLINICIAN: result.get(APPOINTMENT_FIELD_CLINICIAN),
                APPOINTMENT_FIELD_DEPARTMENT: result.get(APPOINTMENT_FIELD_DEPARTMENT),
                APPOINTMENT_FIELD_POSTCODE: result.get(APPOINTMENT_FIELD_POSTCODE),
                APPOINTMENT_FIELD_ID: result.get(APPOINTMENT_FIELD_ID)
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
