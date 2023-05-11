from api.exceptions import NotFoundException, UnauthorizedException
from api.helpers import (
    error, internal_server_error, not_found, success, unauthorized
)
from api.protocols.auth import Authentication
from api.protocols.repository import Repository
from api.protocols.rest import Controller, HttpRequest, HttpResponse
from api.services import get_subject, verify_if_task_exists, verify_if_user_exists


class DeleteTaskController(Controller):
    def __init__(self, task_id: int, auth: Authentication, repository: Repository) -> None:
        self.task_id = task_id
        self.auth    = auth
        self.repository = repository
    

    def handle(self, request: HttpRequest) -> HttpResponse:
        try:
            user_id = get_subject(self.auth, request)
            verify_if_user_exists(user_id, self.repository)
            verify_if_task_exists(self.task_id, user_id, self.repository)
            self.repository.delete_task(self.task_id)

            return success({'data': f'Task {self.task_id} deleted'})
        except NotFoundException as ex:
            return not_found(error(f'{ex}'))
        except UnauthorizedException as ex:
            return unauthorized(error(f'{ex}'))
        except Exception as ex:
            return internal_server_error(error(f'{ex}'))