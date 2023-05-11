from api.exceptions import BadRequestException, NotFoundException, UnauthorizedException
from api.helpers import (
    bad_request, error, internal_server_error, not_found, success, unauthorized
)
from api.entities.task import UpdateTask
from api.protocols.auth import Authentication
from api.protocols.repository import Repository
from api.protocols.rest import Controller, HttpRequest, HttpResponse
from api.services import get_subject, validate_required_params, verify_if_task_exists, verify_if_user_exists


class UpdateTaskController(Controller):
    def __init__(self, task_id: int, auth: Authentication, repository: Repository) -> None:
        self.task_id = task_id
        self.auth    = auth
        self.repository = repository
    
    def validate_task(self, request: HttpRequest) -> UpdateTask:
        validate_required_params(request, params=['text', 'date', 'done'])
        return UpdateTask(
            id=self.task_id,
            text=str(request.body['text']),
            date=str(request.body['date']),
            done=bool(request.body['done']),
        )
    
    def handle(self, request: HttpRequest) -> HttpResponse:
        try:
            user_id = get_subject(self.auth, request)
            model = self.validate_task(request)
            verify_if_user_exists(user_id, self.repository)
            verify_if_task_exists(model.id, user_id, self.repository)
            self.repository.update_task(model)

            return success({'data': model.to_dict})
        
        except BadRequestException as ex:
            return bad_request(error(f'{ex}'))
        except NotFoundException as ex:
            return not_found(error(f'{ex}'))
        except UnauthorizedException as ex:
            return unauthorized(error(f'{ex}'))
        except Exception as ex:
            return internal_server_error(error(f'{ex}'))