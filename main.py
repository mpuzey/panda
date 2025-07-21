import tornado

from api.appointments.appointment_handler import AppointmentHandler
from api.appointments.appointments_handler import AppointmentsHandler
from api.patients.patient_handler import PatientHandler
from api.patients.patients_handler import PatientsHandler


def start_server():
    app = start_app()
    app.listen(8889)
    tornado.ioloop.IOLoop.current().start()


def start_app():
    """ This function returns an Application instance loaded with the necessary request handlers
    for the app.
    """

    return tornado.web.Application([
        (r'/api/patients/([0-9]+)', PatientHandler),
        (r'/api/patients/', PatientsHandler),
        (r'/api/appointments/([a-f0-9\-]{36})', AppointmentHandler),
        (r'/api/appointments/', AppointmentsHandler)
    ])


if __name__ == '__main__':
    start_server()