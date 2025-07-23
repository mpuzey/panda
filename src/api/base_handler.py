""" This module holds the base handler for the application. """
import tornado.web
from constants import HEADER_ALLOW_ORIGIN, HEADER_ALLOW_HEADERS, HEADER_ALLOW_METHODS, HEADER_ALLOW_ORIGIN_VALUE, HEADER_ALLOW_HEADERS_VALUE, HEADER_ALLOW_METHODS_VALUE, HTTP_204_NO_CONTENT


class BaseHandler(tornado.web.RequestHandler):
    """ This tornado handler provides the default behaviour to other handlers in the application.
    This includes setting response headers and the configuring responses for the pre-flight options
    method. """
    def set_default_headers(self):
        """ This function sets headers necessary to respond to clients and allows cross-origin
        requests between the client page and API. """
        self.set_header(HEADER_ALLOW_ORIGIN, HEADER_ALLOW_ORIGIN_VALUE)
        self.set_header(HEADER_ALLOW_HEADERS, HEADER_ALLOW_HEADERS_VALUE)
        self.set_header(HEADER_ALLOW_METHODS, HEADER_ALLOW_METHODS_VALUE)

    def options(self):
        """ This function allows the application to respond to clients sending the pre-flight
        request ahead of the vanilla request (such as GET). """
        self.set_status(HTTP_204_NO_CONTENT)
        self.finish()