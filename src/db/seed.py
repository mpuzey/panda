import pymongo
import json
import os

ROOT_PATH = os.path.dirname(os.path.abspath(__file__)) + "/"
EXAMPLE_PATIENTS_FILENAME = "example_patients.json"
EXAMPLE_APPOINTMENTS_FILENAME = 'example_appointments.json'
MONGODB_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/')

client = pymongo.MongoClient(MONGODB_URI)
db = client["panda"]


def seed_appointments():
  collection = db["appointments"]
  with open(ROOT_PATH + EXAMPLE_APPOINTMENTS_FILENAME, 'r') as outfile:
    appointments = json.load(outfile)

  result = collection.insert_many(appointments)
  print(result)


def seed_patients():
  collection = db["patients"]

  with open(ROOT_PATH + EXAMPLE_PATIENTS_FILENAME, 'r') as outfile:
    patients = json.load(outfile)

  result = collection.insert_many(patients)
  print(result)


if __name__ == '__main__':
  seed_patients()
  seed_appointments()