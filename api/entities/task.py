from datetime import datetime
from typing import Any

from api.environment import Environment


class Task:
    def __init__(self, id: int, text: str, date: str, done: bool, user_id: int) -> None:
        self.id = id
        self.text = text
        self.__date = date
        self.done = done
        self.user_id = user_id

    @property
    def date(self) -> datetime:
        return datetime.strptime(self.__date, Environment.DATE_FORMAT)

    @property
    def to_dict(self) -> dict[str, Any]:
        return {
            'id': self.id,
            'text': self.text,
            'date': self.__date,
            'done': self.done,
            'user_id': self.user_id
        }

class AddTask:
    def __init__(self, text: str, date: str, user_id: int) -> None:
        self.text = text
        self.date = date
        self.done = False
        self.user_id = user_id

    @property
    def to_dict(self) -> dict[str, Any]:
        return {
            'text': self.text,
            'date': self.date,
            'done': self.done,
            'user_id': self.user_id
        }
    
class UpdateTask:
    def __init__(self, id: int, text: str, date: str, done: bool) -> None:
        self.id   = id
        self.text = text
        self.date = date
        self.done = done
    
    @property
    def to_dict(self) -> dict[str, Any]:
        return {
            'text': self.text,
            'date': self.date,
            'done': self.done
        }