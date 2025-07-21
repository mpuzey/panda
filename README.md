# PANDA - Patient Appointment Network Data Application

The Patient Appointment Network Data Application, or simply, - PANDA is a POC for a appointment booking services for NHS and private patients.  

### Setup instructions

Note that Docker is required to run a local instance of mongodb. The application itself can be run inside or outside of
Docker for ease of local development. 

### With Docker only: 
```
./scripts/run.sh all
python3 ./scripts/seed-db.py
``` 

### Native setup - Mac OS: 
TODO: complete instructions for setup without dockerised app 
```
brew install Python 3.9
pip3 install -r requirements.txt
python3 main.py
```

### Fetching all patients
```
curl http://localhost:8889/api/patients/
```

### Fetching a single patient
```
curl http://localhost:8889/api/patients/1373645350
```

### Create a new patient
```
curl -X POST http://localhost:8889/api/patients/1373645351 -d '{"nhs_number": "1373645351", "name": "Dr M Puzey", "date_of_birth": "1996-02-01", "postcode": "N6 2FA"}'
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

```

### Deleting an appointment
```
curl -X DELETE http://localhost:8889/api/appointments/ac9729b5-5e11-42b4-87e2-6396b4faf1b9
```


### Inspecting the db 
Assumes the db is already running and seeded (see Setup instructions):
```
docker exec -it mongodb bash

mongosh
use panda
show colletions
db.patients.find()
db.appointments.find()
```

### Running the unit tests

```
python3 -m unittest discover tests/api
```

### Running the integration tests
```

```

### Requirements
Here is the list of requirements for this POC:
https://github.com/airelogic/tech-test-portal/tree/main/Patient-Appointment-Backend#application-requirements

### TODOs
There are a number of TODOs scattered throughout this project around further iterations of this implementation. These include,
but are not limited to, the following:  
* Further integration tests
* Terraform code around an AWS deployment of the PANDA system
* Proper mod 10 checks around NHS number 
* 
 