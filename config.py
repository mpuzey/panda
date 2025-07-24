""" This module constitutes as the single point of configuration for the application and pulls
# the necessary environment variables required to run the application. Such as secrets. """
import os

PORT = int(os.environ.get('PORT', '8888'))
MONGODB_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/')
HOST = os.environ.get('HOST', '0.0.0.0')