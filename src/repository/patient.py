from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any


class PatientRepository(ABC):
    """Abstract repository interface for patient data access operations."""

    @abstractmethod
    def create(self, patient: Dict[str, Any]) -> bool:
        """Create a new patient record.

        Args:
            patient: Patient data dictionary

        Returns:
            bool: True if creation was successful, False otherwise
        """
        pass

    @abstractmethod
    def get_by_nhs_number(self, nhs_number: str) -> Optional[Dict[str, Any]]:
        """Get a patient by NHS number.

        Args:
            nhs_number: The patient's NHS number

        Returns:
            Patient data dictionary if found, None otherwise
        """
        pass

    @abstractmethod
    def update_by_nhs_number(self, nhs_number: str, patient_data: Dict[str, Any]) -> bool:
        """Update a patient by NHS number.

        Args:
            nhs_number: The patient's NHS number
            patient_data: Updated patient data

        Returns:
            bool: True if update was successful, False otherwise
        """
        pass

    @abstractmethod
    def delete_by_nhs_number(self, nhs_number: str) -> bool:
        """Delete a patient by NHS number.

        Args:
            nhs_number: The patient's NHS number

        Returns:
            bool: True if deletion was successful, False otherwise
        """
        pass

    @abstractmethod
    def get_all(self) -> List[Dict[str, Any]]:
        """Get all patients.

        Returns:
            List of patient data dictionaries
        """
        pass