import pymongo
import json
import os
import constants
ROOT_PATH = os.path.dirname(os.path.abspath(__file__)) + "/"
MONGODB_URI = os.environ.get('MONGO_URI', constants.DEFAULT_MONGODB_URI)

client = pymongo.MongoClient(MONGODB_URI)
db = client[constants.MONGODB_DATABASE_NAME]


def seed_appointments():
  collection = db[constants.MONGODB_COLLECTION_APPOINTMENTS]
  with open(ROOT_PATH + constants.APPOINTMENTS_FILENAME, 'r') as outfile:
    appointments = json.load(outfile)

  result = collection.insert_many(appointments)
  print(result)


def seed_patients():
  collection = db[constants.MONGODB_COLLECTION_PATIENTS]

  with open(ROOT_PATH + constants.PATIENTS_FILENAME, 'r') as outfile:
    patients = json.load(outfile)

  result = collection.insert_many(patients)
  print(result)


if __name__ == '__main__':
  seed_patients()
  seed_appointments()
  client.close()