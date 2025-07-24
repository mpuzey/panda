import pymongo
import tornado

from src.api.appointments.appointment_handler import AppointmentHandler
from src.api.appointments.appointments_handler import AppointmentsHandler
from src.api.patients.patient_handler import PatientHandler
from src.api.patients.patients_handler import PatientsHandler
from constants import HANDLER_FIELD_DATABASE_CLIENT
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

    return tornado.web.Application([
        # TODO: Move regex to constants.py
        (r'/api/patients/([0-9]+)', PatientHandler, {HANDLER_FIELD_DATABASE_CLIENT: db_client}),
        (r'/api/patients/', PatientsHandler,  {HANDLER_FIELD_DATABASE_CLIENT: db_client}),
        (r'/api/appointments/([a-f0-9\-]{36})', AppointmentHandler,  {HANDLER_FIELD_DATABASE_CLIENT: db_client}),
        (r'/api/appointments/', AppointmentsHandler,  {HANDLER_FIELD_DATABASE_CLIENT: db_client})
    ])


if __name__ == '__main__':
    start_server()