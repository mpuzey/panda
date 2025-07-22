""" This module constitutes as the single point of configuration for the application and pulls
# the necessary environment variables required to run the application. Such as secrets. """
import os

PORT = int(os.environ.get('PORT', '8889'))
MONGODB_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/')
