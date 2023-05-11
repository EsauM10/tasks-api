from typing import Any
from api.exceptions import NotFoundException, UnauthorizedException
from api.helpers import (
    error, internal_server_error, not_found, success, unauthorized
)
from api.protocols import Authentication, Controller, HttpRequest, HttpResponse, Repository
from api.services import get_subject, verify_if_user_exists

class GetTasksController(Controller):
    def __init__(self, auth: Authentication, repository: Repository) -> None:
        self.auth = auth
        self.repository = repository

    def get_tasks(self, user_id: int) -> list[dict[str, Any]]:
        return [
            task.to_dict 
            for task in self.repository.get_tasks(user_id)
        ]

    def handle(self, request: HttpRequest) -> HttpResponse:
        try:
            user_id = get_subject(self.auth, request)
            verify_if_user_exists(user_id, self.repository)
            tasks = self.get_tasks(user_id)
            return success({'data': tasks})
        
        except NotFoundException as ex:
            return not_found(error(f'{ex}'))
        except UnauthorizedException as ex:
            return unauthorized(error(f'{ex}'))
        except Exception as ex:
            return internal_server_error(error(f'{ex}'))