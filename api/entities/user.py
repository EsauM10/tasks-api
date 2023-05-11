from typing import Any


class User:
    def __init__(self, id: int, name: str, email: str, password: str) -> None:
        self.id = id
        self.name = name
        self.email = email
        self.password = password

    @property
    def to_dict(self) -> dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'password': self.password
        }
    
class AddUser:
    def __init__(self, name: str, email: str, password: str) -> None:
        self.name = name
        self.email = email
        self.password = password

    @property
    def to_dict(self) -> dict[str, Any]:
        return {
            'name': self.name,
            'email': self.email,
            'password': self.password
        }