from typing import Optional, List, Dict, Any
from src.repository.appointment import AppointmentRepository
from src.db.mongo import MongoDB
from constants import (
    MONGODB_COLLECTION_APPOINTMENTS,
    APPOINTMENT_FIELD_ID
)


class MongoAppointmentRepository(AppointmentRepository):
    """MongoDB implementation of the AppointmentRepository interface."""

    def __init__(self, mongo_client):
        """Initialize the repository with a MongoDB client.
        
        Args:
            mongo_client: MongoDB client instance
        """
        self.mongo_db = MongoDB(mongo_client, MONGODB_COLLECTION_APPOINTMENTS)

    def create(self, appointment: Dict[str, Any]) -> bool:
        """Create a new appointment record."""
        result = self.mongo_db.create(appointment)
        return result.acknowledged if result else False

    def get_by_id(self, appointment_id: str) -> Optional[Dict[str, Any]]:
        """Get an appointment by ID."""
        return self.mongo_db.get({APPOINTMENT_FIELD_ID: appointment_id})

    def update_by_id(self, appointment_id: str, appointment_data: Dict[str, Any]) -> bool:
        """Update an appointment by ID."""
        result = self.mongo_db.update({APPOINTMENT_FIELD_ID: appointment_id}, appointment_data)
        return result.acknowledged if result else False

    def delete_by_id(self, appointment_id: str) -> bool:
        """Delete an appointment by ID."""
        result = self.mongo_db.delete({APPOINTMENT_FIELD_ID: appointment_id})
        return result.deleted_count > 0 if result else False

    def get_all(self) -> List[Dict[str, Any]]:
        """Get all appointments."""
        return self.mongo_db.getAll() 