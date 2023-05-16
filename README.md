# Tasks API
API with authentication to create personal tasks

## TODO
* Implement a relational repository (e.g. PostgreSQL or MySQL)
* Add a password encrypter
* Add an email validator
* Sanitize all inputs to avoid code injection attacks

## Install
Clone this repository, change the directory to ```~/tasks-api``` and run:
```
pip install -r requirements.txt
```
and then run:
```
python app.py
```

## Endpoints
| **HTTP Method** |    **/**    |                                 JSON                                 |
|:---------------:|:-----------:|:--------------------------------------------------------------------:|
|       POST      |   /signup   | {"name": "Paul", "email": "paul@email.com", "password": "paul12345"} |
|       POST      |    /login   |        {"email": "paul@email.com", "password": "paul12345"}          |
|       POST      |    /tasks   |           {"text": "Study English", "date": "16/05/2022"}            |
|       GET       |    /tasks   |                               None                                   |
|       PUT       | /tasks/{id} |    {"text": "Study English", "date": "16/05/2022", "done": true}     |
|      DELETE     | /tasks/{id} |                               None                                   |
