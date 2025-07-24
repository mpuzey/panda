import pymongo
import tornado

from src.api.appointments.appointment_handler import AppointmentHandler
from src.api.appointments.appointments_handler import AppointmentsHandler
from src.api.patients.patient_handler import PatientHandler
from src.api.patients.patients_handler import PatientsHandler
from src.repository.repository_factory import RepositoryFactory, DatabaseType
from constants import (
    HANDLER_FIELD_PATIENT_REPOSITORY,
    HANDLER_FIELD_APPOINTMENT_REPOSITORY
)
from config import MONGODB_URI, PORT, HOST


def start_server():
    app = start_app()
    app.listen(PORT, address=HOST)
    tornado.ioloop.IOLoop.current().start()


def start_app():
    """ This function returns an Application instance loaded with the necessary request handlers
    for the app.
    """
    db_client = pymongo.MongoClient(MONGODB_URI)

    # Create repositories using the factory
    patient_repository = RepositoryFactory.create_patient_repository(
        DatabaseType.MONGODB,
        db_client
    )
    appointment_repository = RepositoryFactory.create_appointment_repository(
        DatabaseType.MONGODB,
        db_client
    )

    return tornado.web.Application([
        # TODO: Move regex to constants.py
        (r'/api/patients/([0-9]+)', PatientHandler, {HANDLER_FIELD_PATIENT_REPOSITORY: patient_repository}),
        (r'/api/patients/', PatientsHandler, {HANDLER_FIELD_PATIENT_REPOSITORY: patient_repository}),
        (r'/api/appointments/([a-f0-9\-]{36})', AppointmentHandler, {HANDLER_FIELD_APPOINTMENT_REPOSITORY: appointment_repository}),
        (r'/api/appointments/', AppointmentsHandler, {HANDLER_FIELD_APPOINTMENT_REPOSITORY: appointment_repository})
    ])


if __name__ == '__main__':
    start_server()