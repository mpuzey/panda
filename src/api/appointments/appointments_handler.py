from src.api.base_handler import BaseHandler
from src.service.appointment_service import AppointmentService
from constants import (
    PANDA_RESPONSE_FIELD_APPOINTMENTS,
    HTTP_200_OK
)


class AppointmentsHandler(BaseHandler):
    def initialize(self, appointment_repository):
        """Initialize handler with injected appointment repository.

        Args:
            appointment_repository: Repository instance for appointment data access
        """
        self.appointment_service = AppointmentService(appointment_repository)

    def get(self):
        """Get all appointments."""
        service_response = self.appointment_service.get_all_appointments()

        self.set_status(HTTP_200_OK)
        self.write({PANDA_RESPONSE_FIELD_APPOINTMENTS: service_response.data})

