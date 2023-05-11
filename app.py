from datetime import timedelta

from flask import Flask, jsonify, request
from flask.wrappers import Request as FlaskRequest

from api.controllers import (
    AddTaskController, DeleteTaskController, GetTasksController,
    LoginController, SignUpController, UpdateTaskController
)
from api.environment import Environment
from api.services import parse_flask_request
from api.repositories import InMemoryRepository
from api.protocols import Controller
from api.utils.auth import JWTAuthentication

app  = Flask(__name__)
auth = JWTAuthentication(
    secret=Environment.SECRET_KEY,
    token_expiration=timedelta(days=Environment.TOKEN_EXPIRATION)
)
repository = InMemoryRepository()


def make_response(controller: Controller, request: FlaskRequest):
    response = controller.handle(parse_flask_request(request))
    return jsonify(response.body), response.status_code


@app.route('/signup', methods=['POST'])
def sign_up():
    controller = SignUpController(auth, repository)
    return make_response(controller, request)


@app.route('/login', methods=['POST'])
def login():
    controller = LoginController(auth, repository)
    return make_response(controller, request)


@app.route('/tasks', methods=['POST'])
def add_task():
    controller = AddTaskController(auth, repository)
    return make_response(controller, request)


@app.route('/tasks', methods=['GET'])
def get_tasks():
    controller = GetTasksController(auth, repository)
    return make_response(controller, request)


@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id: int):
    controller = UpdateTaskController(task_id, auth, repository)
    return make_response(controller, request)


@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id: int):
    controller = DeleteTaskController(task_id, auth, repository)
    return make_response(controller, request)


if(__name__ == '__main__'):
    app.run(host='localhost', port=5000, debug=True)
