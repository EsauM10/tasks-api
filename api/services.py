from flask.wrappers import Request as FlaskRequest
from typing import Any

from api.exceptions import BadRequestException, NotFoundException, UnauthorizedException
from api.protocols.auth import Authentication
from api.protocols.repository import Repository
from api.protocols.rest import HttpRequest


def validate_required_params(request: HttpRequest, params: list[str]):
    for param in params:
        if(request.body.get(param) is None):
            raise BadRequestException(f'Missing param {param}')
        
def validate_token(auth: Authentication, request: HttpRequest) -> dict[str, Any]:
    token = request.headers.get('Authorization')
    if(token is None):
        raise UnauthorizedException('Missing access token')
    return auth.validate_token(token)

def get_subject(auth: Authentication, request: HttpRequest) -> int:
    return int(validate_token(auth, request)['sub'])


def verify_if_user_exists(user_id: int, repository: Repository):
    user = repository.get_user_by_id(user_id)
    if(user is None):
        raise NotFoundException('User not found')
    
def verify_if_task_exists(task_id: int, user_id: int, repository: Repository):
    task = repository.get_task_by_user(task_id, user_id) 
    if(task is None):
        raise NotFoundException(f'Task {task_id} not found')

def parse_flask_request(request: FlaskRequest) -> HttpRequest: 
    headers = dict(request.headers.items())
    try:
        if(request.json is not None):
            return HttpRequest(body=request.json, headers=headers)
    except: pass
    return HttpRequest(body={}, headers=headers) 