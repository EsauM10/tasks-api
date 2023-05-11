from abc import ABC, abstractmethod
from typing import Any


class Authentication(ABC):
    @abstractmethod
    def generate_token(self, payload: dict[str, Any]) -> str:
        pass

    @abstractmethod
    def validate_token(self, token: str) -> dict[str, Any]:
        pass