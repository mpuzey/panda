""" This module constitutes as the single point of configuration for the application and pulls
# the necessary environment variables required to run the application. Such as secrets. """
import os

API_KEY = os.environ.get('API_KEY')