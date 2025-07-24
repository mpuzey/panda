""" This module holds the base handler for the application. """
import tornado.web
from constants import HEADER_ALLOW_ORIGIN, HEADER_ALLOW_HEADERS, HEADER_ALLOW_METHODS, HEADER_ALLOW_ORIGIN_VALUE, HEADER_ALLOW_HEADERS_VALUE, HEADER_ALLOW_METHODS_VALUE, HTTP_204_NO_CONTENT
from src.localisation.localisation_service import get_localisation_service


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

    def get_user_language(self):
        """Detect user's preferred language from Accept-Language header."""
        accept_language = self.request.headers.get('Accept-Language')
        localisation_service = get_localisation_service()
        return localisation_service.detect_language(accept_language)

    def translate_message(self, message_key, **kwargs):
        """Translate a message key to the user's preferred language."""
        language = self.get_user_language()
        localisation_service = get_localisation_service()
        return localisation_service.translate(message_key, language, **kwargs)

    def translate_errors(self, errors):
        """Translate a list of error objects or message keys."""
        translated_errors = []
        for error in errors:
            if isinstance(error, dict) and 'key' in error:
                # New format: {'key': 'message_key', 'params': {...}}
                key = error['key']
                params = error.get('params', {})
                translated_errors.append(self.translate_message(key, **params))
            elif isinstance(error, str):
                # Legacy string format or message key
                translated_errors.append(self.translate_message(error))
            else:
                # Fallback for unexpected formats
                translated_errors.append(str(error))
        return translated_errors