# PANDA - Patient Appointment Network Data Application

The Patient Appointment Network Data Application, or simply, - PANDA is a POC for a appointment booking services for NHS and private patients.  

## Setup instructions

Note that Docker is required to run a local instance of mongodb. The application itself can be run inside or outside of
Docker for ease of local development. 

### With Docker: 
Built on Docker Desktop 4.24.2 - requires 4.24.2 or later.
```
docker-compose up
``` 

### Native Panda setup - Mac OS:
```
brew install Python 3.9
pip3 install -r requirements.txt

./run.sh db
python3 main.py
```

## Using the API

### Fetching all patients
(alternatively, you run the integration tests, see "Running the integration tests")
```
curl http://localhost:8889/api/patients/
```

### Fetching a single patient
```
curl http://localhost:8889/api/patients/1373645350
```

### Creating a new patient
```
curl -X POST http://localhost:8889/api/patients/1373645351 -d '{"nhs_number": "1373645351", "name": "Dr M Puzey", "date_of_birth": "1996-02-01", "postcode": "N6 2FA"}'
```

### Updating patient details
```
curl -X PUT http://localhost:8889/api/patients/1373645351 -d '{"nhs_number": "1373645351", "name": "Dr M Close", "date_of_birth": "1996-02-01", "postcode": "N6 2FA"}'
```

### Deleting a patient
```
curl -X DELETE http://localhost:8889/api/patients/1373645350
```


### Fetching all appointments 
```
curl http://localhost:8889/api/appointments/
```

### Fetching a single appointment
```
curl http://localhost:8889/api/appointments/ac9729b5-5e11-42b4-87e2-6396b4faf1b9
```

### Creating an appointment 
```
curl -X POST http://localhost:8889/api/appointments/ac9729b5-5e11-42b4-87e2-6396b4faf1b0 -d '{"patient": "1373645351", "status": "attended", "time": "2018-01-21T16:30:00+00:00", "duration": "15m", "clinician": "Jason Holloway", "department": "oncology", "postcode": "UB56 7XQ", "id": "ac9729b5-5e11-42b4-87e2-6396b4faf1b0"}'
```

### Updating an appointment
```
curl -X PUT http://localhost:8889/api/appointments/ac9729b5-5e11-42b4-87e2-6396b4faf1b0 -d '{"patient": "1373645351", "status": "attended", "time": "2018-01-21T16:30:00+00:00", "duration": "15m", "clinician": "Jason Close", "department": "oncology", "postcode": "UB56 7XQ", "id": "ac9729b5-5e11-42b4-87e2-6396b4faf1b0"}'
```

### Cancelling an appointment
```
curl -X DELETE http://localhost:8889/api/appointments/ac9729b5-5e11-42b4-87e2-6396b4faf1b9
```

## Inspecting the db 
Assumes the db is already running andsee ded (see "Setup instructions"):
```
docker exec -it mongodb bash

mongosh
use panda
show colletions
db.patients.find()
db.appointments.find()
```

## Testing the API

### Running the unit tests

```
python3 -m unittest discover tests/api
```

### Running the integration tests
Note that mongodb must be running for these tests to pass (see "Native Panda setup - Mac OS)
```
python3 -m unittest discover tests/integration
```

## Requirements
Here is the list of requirements for this POC:
https://github.com/airelogic/tech-test-portal/tree/main/Patient-Appointment-Backend#application-requirements

The client has elucidated the following hard requirements for the MVP:
* It should be possible to add patients to and remove them from the PANDA. ✅ 
* It should be possible to check and update patient details in the PANDA. ❌
* It should be possible to add new appointments to the PANDA, and check and update appointment details. ❌ (update still missing?)
* The PANDA may need to be restarted for maintenance, and the data should be persisted. ✅ 
* The PANDA backend should communicate with the frontend via some sort of HTTP API. ✅ 
* The PANDA API does not need to handle authentication because it is used within a trusted environment. ✅ 
* Errors should be reported to the user. ✅ 

There are some additional requirements for the data:
* Appointments can be cancelled, but cancelled appointments cannot be reinstated.  ❌ - partially implemented
* Appointments should be considered 'missed' if they are not set to 'attended' by the end of the appointment. ❌
* Ensure that all NHS numbers are checksum validated. ❌
* Ensure that all postcodes can be coerced into the correct format. ✅ 

A separate team has been tasked with building the frontend for the application. You've spoken with this team to iron out the separation of responsibilities:

* They're quite flexible about what they can build, and willing to defer to your choices about implementation. ✅ 
* They're flexible about how they interact with the API, as long as you can provide guidance and they can get data in JSON format. ✅ 
* Due to time constraints, they will not be able to properly validate the inbound data in the frontend, but can propagate error responses returned by the backend. ✅ - validation implemented, some errors are not user friendly
* All timestamp passed between the backend and frontend must be timezone-aware. ✅ 

Additional Considerations
As you've worked with the client for a while, you have an awareness of some past issues and upcoming work that it might be worth taking into consideration:
* The client has been burned by vendor lock-in in the past, and prefers working with smaller frameworks. ✅ 
* The client highly values automated tests, particularly those which ensure their business logic is implemented correctly. ✅ ❌ - unit tests around validation but much many more are needed around business logic 
* The client is in negotiation with several database vendors, and is interested in being database-agnostic if possible. ❌ - mongo used for persistence for now, can be swapped out easily
* The client is somewhat concerned that missed appointments waste significant amounts of clinicians' time, and is interested in tracking the impact this has over time on a per-clinician and per-department basis. ❌
* The PANDA currently doesn't contain much data about clinicians, but will eventually track data about the specific organisations they currently work for and where they work from. ❌
* The client is interested in branching out into foreign markets, it would be useful if error messages could be localised. ❌
* The client would like to ensure that patient names can be represented correctly, in line with GDPR. ❌

## TODOs
There are a number of TODOs scattered throughout this project around further iterations of this implementation. These include,
but are not limited to, the following:  
* Further integration tests
* Terraform code around an AWS deployment (or similar) of the PANDA system
* Proper mod 10 checks around NHS number 
* Uplift to the async Tornado handlers and MongoDB Driver for scalability
 