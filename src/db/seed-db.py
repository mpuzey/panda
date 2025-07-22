import pymongo
import json

from constants import ROOT_PATH, EXAMPLE_APPOINTMENTS_FILENAME, EXAMPLE_PATIENTS_FILENAME

client = pymongo.MongoClient("mongodb://localhost:27017/")
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