from constants import (
    ERR_COULD_NOT_CREATE_APPOINTMENT, 
    ERR_COULD_NOT_UPDATE_APPOINTMENT, 
    ERR_APPOINTMENT_NOT_FOUND,
    MSG_NEW_APPOINTMENT_ADDED, 
    MSG_APPOINTMENT_UPDATED, 
    MSG_APPOINTMENT_CANCELLED,
    HTTP_201_CREATED,
    HTTP_200_OK
)
from src.service.appointment_validation import validate


class AppointmentService:

    def __init__(self, mongo_database):
        self.mongo_database = mongo_database

    def create_appointment(self, appointment, appointment_id):
        """Create a new appointment with validation."""
        errors = validate(appointment)
        if errors:
            return {'status': 400, 'errors': errors}

        result = self.mongo_database.create(appointment)
        if not result.acknowledged:
            return {'status': 500, 'error': ERR_COULD_NOT_CREATE_APPOINTMENT}

        return {
            'status': HTTP_201_CREATED,
            'message': MSG_NEW_APPOINTMENT_ADDED.format(appointment_id)
        }

    def update_appointment(self, appointment, appointment_id):
        """Update an existing appointment with validation."""
        errors = validate(appointment)
        if errors:
            return {'status': 400, 'errors': errors}

        result = self.mongo_database.update({'id': appointment_id}, appointment)
        if not result.acknowledged:
            return {'status': 500, 'error': ERR_COULD_NOT_UPDATE_APPOINTMENT}

        return {
            'status': HTTP_200_OK,
            'message': MSG_APPOINTMENT_UPDATED.format(appointment_id)
        }

    def get_appointment(self, appointment_id):
        """Get an appointment by ID."""
        result = self.mongo_database.get({'id': appointment_id})
        if not result:
            return {'status': 404, 'error': ERR_APPOINTMENT_NOT_FOUND}

        return {
            'status': HTTP_200_OK,
            'appointment': {
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
        result = self.mongo_database.delete({'id': appointment_id})
        if not result.deleted_count:
            return {'status': 404, 'error': ERR_APPOINTMENT_NOT_FOUND}

        return {
            'status': HTTP_200_OK,
            'message': MSG_APPOINTMENT_CANCELLED.format(appointment_id)
        }

    def get_all_appointments(self):
        """Get all appointments."""
        appointments = self.mongo_database.getAll()
        return {
            'status': HTTP_200_OK,
            'appointments': appointments
        } 