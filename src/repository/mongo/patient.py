from typing import Optional, List, Dict, Any
from src.repository.patient import PatientRepository
from src.db.mongo import MongoDB
from constants import (
    MONGODB_COLLECTION_PATIENTS,
    PATIENT_FIELD_NHS_NUMBER,
)


class MongoPatientRepository(PatientRepository):
    """MongoDB implementation of the PatientRepository interface."""

    def __init__(self, mongo_client):
        """Initialize the repository with a MongoDB client.

        Args:
            mongo_client: MongoDB client instance
        """
        self.mongo_db = MongoDB(mongo_client, MONGODB_COLLECTION_PATIENTS)

    def create(self, patient: Dict[str, Any]) -> bool:
        """Create a new patient record."""
        result = self.mongo_db.create(patient)
        return result.acknowledged if result else False

    def get_by_nhs_number(self, nhs_number: str) -> Optional[Dict[str, Any]]:
        """Get a patient by NHS number."""
        return self.mongo_db.get({PATIENT_FIELD_NHS_NUMBER: nhs_number})

    def update_by_nhs_number(self, nhs_number: str, patient_data: Dict[str, Any]) -> bool:
        """Update a patient by NHS number."""
        result = self.mongo_db.update({PATIENT_FIELD_NHS_NUMBER: nhs_number}, patient_data)
        return result.acknowledged if result else False

    def delete_by_nhs_number(self, nhs_number: str) -> bool:
        """Delete a patient by NHS number."""
        result = self.mongo_db.delete({PATIENT_FIELD_NHS_NUMBER: nhs_number})
        return result.deleted_count > 0 if result else False

    def get_all(self) -> List[Dict[str, Any]]:
        """Get all patients."""
        return self.mongo_db.getAll()