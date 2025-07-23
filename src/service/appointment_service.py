from src.db.mongo import MongoDB

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
    APPOINTMENT_SERVICE_FIELD_APPOINTMENT,
    MONGODB_COLLECTION_APPOINTMENTS,
    APPOINTMENT_FIELD_ID,
    APPOINTMENT_SERVICE_FIELD_APPOINTMENTS,
)
from src.service.appointment_validation import validate


class AppointmentService:

    def __init__(self, mongo_database_client):
        self.mongo_database = MongoDB(mongo_database_client, MONGODB_COLLECTION_APPOINTMENTS)

    def create_appointment(self, appointment, appointment_id):
        """Create a new appointment with validation."""
        errors = validate(appointment)
        if errors:
            return {APPOINTMENT_SERVICE_FIELD_STATUS: 400, APPOINTMENT_SERVICE_FIELD_ERROR: errors}

        result = self.mongo_database.create(appointment)
        if not result.acknowledged:
            return {APPOINTMENT_SERVICE_FIELD_STATUS: 500, APPOINTMENT_SERVICE_FIELD_ERROR: ERR_COULD_NOT_CREATE_APPOINTMENT}

        return {
            APPOINTMENT_SERVICE_FIELD_STATUS: HTTP_201_CREATED,
            APPOINTMENT_SERVICE_FIELD_MESSAGE: MSG_NEW_APPOINTMENT_ADDED.format(appointment_id)
        }

    def update_appointment(self, appointment, appointment_id):
        """Update an existing appointment with validation."""
        errors = validate(appointment)
        if errors:
            return {APPOINTMENT_SERVICE_FIELD_STATUS: 400, APPOINTMENT_SERVICE_FIELD_VALIDATION_ERRORS: errors}

        result = self.mongo_database.update({APPOINTMENT_FIELD_ID: appointment_id}, appointment)
        if not result.acknowledged:
            return {APPOINTMENT_SERVICE_FIELD_STATUS: 500, APPOINTMENT_SERVICE_FIELD_ERROR: ERR_COULD_NOT_UPDATE_APPOINTMENT}

        return {
            APPOINTMENT_SERVICE_FIELD_STATUS: HTTP_200_OK,
            APPOINTMENT_SERVICE_FIELD_MESSAGE: MSG_APPOINTMENT_UPDATED.format(appointment_id)
        }

    def get_appointment(self, appointment_id):
        """Get an appointment by ID."""
        result = self.mongo_database.get({APPOINTMENT_FIELD_ID: appointment_id})
        if not result:
            return {APPOINTMENT_SERVICE_FIELD_STATUS: 404, APPOINTMENT_SERVICE_FIELD_ERROR: ERR_APPOINTMENT_NOT_FOUND}

        return {
            APPOINTMENT_SERVICE_FIELD_STATUS: HTTP_200_OK,
            APPOINTMENT_SERVICE_FIELD_APPOINTMENT: {
                # TODO: add constants for fields for both PANDA response and result fields
                'patient': result.get('patient'),
                'status': result.get('status'),
                'time': result.get('time'),
                'duration': result.get('duration'),
                'clinician': result.get('clinician'),
                'department': result.get('department'),
                'postcode': result.get('postcode'),
                'id': result.get('id')
            }
        }

    def delete_appointment(self, appointment_id):
        """Delete an appointment by ID."""
        result = self.mongo_database.delete({APPOINTMENT_FIELD_ID: appointment_id})
        if not result.deleted_count:
            return {APPOINTMENT_SERVICE_FIELD_STATUS: 404, APPOINTMENT_SERVICE_FIELD_ERROR: ERR_APPOINTMENT_NOT_FOUND}

        return {
            APPOINTMENT_SERVICE_FIELD_STATUS: HTTP_200_OK,
            APPOINTMENT_SERVICE_FIELD_MESSAGE: MSG_APPOINTMENT_CANCELLED.format(appointment_id)
        }

    def get_all_appointments(self):
        """Get all appointments."""
        appointments = self.mongo_database.getAll()
        return {
            APPOINTMENT_SERVICE_FIELD_STATUS: HTTP_200_OK,
            APPOINTMENT_SERVICE_FIELD_APPOINTMENTS: appointments
        }
