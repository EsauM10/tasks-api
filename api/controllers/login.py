from api.exceptions import BadRequestException, UnauthorizedException
from api.helpers import (
    bad_request, error, internal_server_error, success, unauthorized
)
from api.entities.user import User
from api.protocols import Authentication, Controller, HttpRequest, HttpResponse, Repository
from api.services import validate_required_params


class LoginController(Controller):
    def __init__(self, auth: Authentication, repository: Repository) -> None:
        self.auth = auth
        self.repository = repository
    
    def get_user_with_credentials(self, email: str, password: str) -> User:
        user = self.repository.get_user_with_credentials(email, password)
        if(user is None):
            raise UnauthorizedException('Invalid email or password')
        return user

    def handle(self, request: HttpRequest) -> HttpResponse:
        try:
            validate_required_params(request, params=['email', 'password'])
            email    = str(request.body['email'])
            password = str(request.body['password'])
            user     = self.get_user_with_credentials(email, password)
            token    = self.auth.generate_token(payload={
                'sub': user.id,
                'name': user.name
            })
            return success({'token': token})

        except BadRequestException as ex:
            return bad_request(error(f'{ex}'))
        except UnauthorizedException as ex:
            return unauthorized(error(f'{ex}'))
        except Exception as ex:
            return internal_server_error(error(f'{ex}'))