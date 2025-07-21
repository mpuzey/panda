# PANDA

### Install instructions

Native setup - Mac OS: 
```
brew install Python 3.9
pip3 install -r requirements.txt
```

# TODO: Add Dockerfile and install 
With Docker: 
```

```

### Fetching all patients
```
curl http://localhost:8889/api/patients/
```

### Fetching a single patient
```
curl http://localhost:8889/api/patients/<nhs_number>
```
e.g.
```
curl http://localhost:8889/api/patients/1373645350
```

### Create a new patient
```
 curl -X POST http://localhost:8889/api/patients/1373645351 -d '{"nhs_number": "1373645351", "name": "Dr M Puzey", "date_of_birth": "1996-02-01", "postcode": "N6 2FA"}'
```

### Delete a patient

###


### Fetching all appointments 
```
curl http://localhost:8889/api/appointments/
```

### Fetching a single patient
```
curl http://localhost:8889/api/appointments/ac9729b5-5e11-42b4-87e2-6396b4faf1b9
```

### Running the unit tests

TODO: Why does this not work as in the IDE?
```
python -m unittest discover .
```

### Running the integration tests
```

```

### Requirements
https://github.com/airelogic/tech-test-portal/tree/main/Patient-Appointment-Backend#application-requirements
 