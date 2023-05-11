from datetime import datetime
from api.environment import Environment
from api.exceptions import (
    BadRequestException, NotFoundException, UnauthorizedException
)
from api.helpers import (
    bad_request, created, error, internal_server_error, not_found, unauthorized, 
)
from api.entities.task import AddTask
from api.protocols import Authentication, Controller, HttpRequest, HttpResponse, Repository
from api.services import get_subject, validate_required_params, verify_if_user_exists

class AddTaskController(Controller):
    def __init__(self, auth: Authentication, repository: Repository) -> None:
        self.auth = auth
        self.repository = repository

    def validate_date(self, date: str) -> str:
        format = Environment.DATE_FORMAT
        try:
            return datetime.strptime(date, format).strftime(format)
        except Exception as ex:
            raise BadRequestException(f'{ex}')
    
    def verify_if_user_exists(self, user_id: int):
        user = self.repository.get_user_by_id(user_id)
        if(user is None):
            raise NotFoundException('User not found')

    def handle(self, request: HttpRequest) -> HttpResponse:
        try:
            user_id = get_subject(self.auth, request)
            validate_required_params(request, params=['text', 'date'])
          
            model= AddTask(
                text=str(request.body['text']),
                date=self.validate_date(request.body['date']),
                user_id=user_id
            )
            verify_if_user_exists(model.user_id, self.repository)
            task = self.repository.add_task(model)
            return created({'data': task.to_dict})
        
        except BadRequestException as ex:
            return bad_request(error(f'{ex}'))
        except NotFoundException as ex:
            return not_found(error(f'{ex}'))
        except UnauthorizedException as ex:
            return unauthorized(error(f'{ex}'))
        except Exception as ex:
            return internal_server_error(error(f'{ex}'))
        