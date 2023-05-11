from datetime import datetime, timedelta
from typing import Any
import jwt

from api.exceptions import UnauthorizedException
from api.protocols import Authentication

class JWTAuthentication(Authentication):
    def __init__(self, secret: str, token_expiration: timedelta) -> None:
        self.secret = secret
        self.token_expiration = token_expiration

    def get_expiration_date(self) -> datetime:
        return datetime.now() + self.token_expiration

    def generate_token(self, payload: dict[str, Any]) -> str:
       payload['exp'] = self.get_expiration_date().timestamp()
       return jwt.encode(payload, self.secret, algorithm='HS256')
    
    def validate_token(self, token: str) -> dict[str, Any]:
        try:
            token = token.replace('Bearer ', '')
            return jwt.decode(token, self.secret, algorithms=['HS256'])
         
        except Exception as ex:
            raise UnauthorizedException(f'{ex}')