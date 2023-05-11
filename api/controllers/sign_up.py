from api.exceptions import BadRequestException, ConflictException
from api.helpers import bad_request, conflict, created, error, internal_server_error
from api.entities.user import AddUser
from api.protocols import Authentication, Controller, HttpRequest, HttpResponse, Repository
from api.services import validate_required_params

class SignUpController(Controller):
    def __init__(self, auth: Authentication, repository: Repository) -> None:
        self.auth = auth
        self.repository = repository
    
    def validate_user(self, request: HttpRequest) -> AddUser:
        validate_required_params(request, params=['name', 'email', 'password'])
        return AddUser(
            name=str(request.body['name']),
            email=str(request.body['email']),
            password=str(request.body['password']) 
        )
    
    def verify_if_email_exists(self, model: AddUser):
        user = self.repository.get_user_by_email(model.email)
        if(user is not None):
            raise ConflictException('This email address already exists')
        
    def handle(self, request: HttpRequest) -> HttpResponse:
        try:
            model = self.validate_user(request)
            self.verify_if_email_exists(model)
            user  = self.repository.add_user(model)
            token = self.auth.generate_token(payload={
                'sub': user.id,
                'name': user.name
            })
            return created({'token': token})
        
        except BadRequestException as ex:
            return bad_request(error(f'{ex}'))
        except ConflictException as ex:
            return conflict(error(f'{ex}'))
        except Exception as ex:
            return internal_server_error(error(f'{ex}'))
