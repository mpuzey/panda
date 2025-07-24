from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any


class AppointmentRepository(ABC):
    """Abstract repository interface for appointment data access operations."""

    @abstractmethod
    def create(self, appointment: Dict[str, Any]) -> bool:
        """Create a new appointment record.
        
        Args:
            appointment: Appointment data dictionary
            
        Returns:
            bool: True if creation was successful, False otherwise
        """
        pass

    @abstractmethod
    def get_by_id(self, appointment_id: str) -> Optional[Dict[str, Any]]:
        """Get an appointment by ID.
        
        Args:
            appointment_id: The appointment ID
            
        Returns:
            Appointment data dictionary if found, None otherwise
        """
        pass

    @abstractmethod
    def update_by_id(self, appointment_id: str, appointment_data: Dict[str, Any]) -> bool:
        """Update an appointment by ID.
        
        Args:
            appointment_id: The appointment ID
            appointment_data: Updated appointment data
            
        Returns:
            bool: True if update was successful, False otherwise
        """
        pass

    @abstractmethod
    def delete_by_id(self, appointment_id: str) -> bool:
        """Delete an appointment by ID.
        
        Args:
            appointment_id: The appointment ID
            
        Returns:
            bool: True if deletion was successful, False otherwise
        """
        pass

    @abstractmethod
    def get_all(self) -> List[Dict[str, Any]]:
        """Get all appointments.
        
        Returns:
            List of appointment data dictionaries
        """
        pass 