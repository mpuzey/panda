import pymongo
import tornado

from src.api.appointments.appointment_handler import AppointmentHandler
from src.api.appointments.appointments_handler import AppointmentsHandler
from src.api.patients.patient_handler import PatientHandler
from src.api.patients.patients_handler import PatientsHandler


def start_server():
    app = start_app()
    app.listen(8889, address='0.0.0.0')
    tornado.ioloop.IOLoop.current().start()


def start_app():
    """ This function returns an Application instance loaded with the necessary request handlers
    for the app.
    """
    db_client = pymongo.MongoClient("mongodb://localhost:27017/")

    return tornado.web.Application([
        (r'/api/patients/([0-9]+)', PatientHandler, {'db_client': db_client}),
        # (r'/api/patients/', PatientsHandler,  {'db_client': db_client}),
        (r'/api/appointments/([a-f0-9\-]{36})', AppointmentHandler,  {'db_client': db_client}),
        # (r'/api/appointments/', AppointmentsHandler,  {'db_client': db_client})
    ])


if __name__ == '__main__':
    start_server()