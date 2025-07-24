from enum import Enum
from typing import Protocol
from src.repository.appointment import AppointmentRepository
from src.repository.patient import PatientRepository
from src.repository.mongo.appointment import MongoAppointmentRepository
from src.repository.mongo.patient import MongoPatientRepository


class DatabaseType(Enum):
    """Enumeration of supported database types."""
    MONGODB = "mongo"
    # Future database types can be added here
    # POSTGRESQL = "postgresql"
    # MYSQL = "mysql"


class DatabaseClient(Protocol):
    """Protocol for database client implementations."""
    pass


class RepositoryFactory:
    """Factory class for creating repository instances based on database type."""

    @staticmethod
    def create_patient_repository(
        database_type: DatabaseType, 
        database_client: DatabaseClient
    ) -> PatientRepository:
        """Create a patient repository instance.
        
        Args:
            database_type: The type of database to create repository for
            database_client: The database client instance
            
        Returns:
            PatientRepository: Repository instance for patient data access
            
        Raises:
            ValueError: If database type is not supported
        """
        if database_type == DatabaseType.MONGODB:
            return MongoPatientRepository(database_client)
        
        # Future database implementations can be added here
        # elif database_type == DatabaseType.POSTGRESQL:
        #     return PostgreSQLPatientRepository(database_client)
        
        raise ValueError(f"Unsupported database type: {database_type}")

    @staticmethod
    def create_appointment_repository(
        database_type: DatabaseType, 
        database_client: DatabaseClient
    ) -> AppointmentRepository:
        """Create an appointment repository instance.
        
        Args:
            database_type: The type of database to create repository for
            database_client: The database client instance
            
        Returns:
            AppointmentRepository: Repository instance for appointment data access
            
        Raises:
            ValueError: If database type is not supported
        """
        if database_type == DatabaseType.MONGODB:
            return MongoAppointmentRepository(database_client)
        
        # Future database implementations can be added here
        # elif database_type == DatabaseType.POSTGRESQL:
        #     return PostgreSQLAppointmentRepository(database_client)
        
        raise ValueError(f"Unsupported database type: {database_type}")

    @classmethod
    def create_repositories(
        cls, 
        database_type: DatabaseType, 
        database_client: DatabaseClient
    ) -> tuple[PatientRepository, AppointmentRepository]:
        """Create both patient and appointment repositories.
        
        Args:
            database_type: The type of database to create repositories for
            database_client: The database client instance
            
        Returns:
            tuple: (PatientRepository, AppointmentRepository) instances
        """
        patient_repo = cls.create_patient_repository(database_type, database_client)
        appointment_repo = cls.create_appointment_repository(database_type, database_client)
        return patient_repo, appointment_repo
