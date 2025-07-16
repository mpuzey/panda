import json

import tornado

from api.appointments_handler import AppointmentsHandler
from constants import ROOT_PATH
from api.patients_handler import PatientsHandler


def start_server():
    app = start_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()


def start_app():
    """ This function returns an Application instance loaded with the necessary request handlers
    for the app.
    """

    return tornado.web.Application([
        # (r'/public/(.*)', tornado.web.StaticFileHandler, {'path': PUBLIC_ROOT}),
        (r'/patients/', PatientsHandler),
        (r'/appointments/', AppointmentsHandler)
    ])


if __name__ == '__main__':
    start_server()