from abc import ABC, abstractmethod
from typing import Any

class HttpRequest:
    def __init__(self, 
        body: dict[str, Any], 
        headers: dict[str, str]
    ):
        self.body = body
        self.headers = headers
    

class HttpResponse:
    def __init__(self, status_code: int, body: dict[str, Any]) -> None:
        self.status_code = status_code
        self.body = body
        self.headers = {}
    
    @property
    def is_ok(self) -> bool:
        return self.status_code in [200, 201]
    

class Controller(ABC):
    @abstractmethod
    def handle(self, request: HttpRequest) -> HttpResponse:
        pass