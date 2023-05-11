from abc import ABC, abstractmethod

from api.entities.user import AddUser, User
from api.entities.task import AddTask, Task, UpdateTask


class Repository(ABC):
    @abstractmethod
    def add_user(self, model: AddUser) -> User:
        pass
    
    @abstractmethod
    def get_user_by_email(self, email: str) -> 'User | None':
        pass
    
    @abstractmethod
    def get_user_by_id(self, id: int) -> 'User | None':
        pass
    
    @abstractmethod
    def get_user_with_credentials(self, email: str, password: str) -> 'User | None':
        pass
        
    
    @abstractmethod
    def add_task(self, model: AddTask) -> Task:
        pass
    
    @abstractmethod
    def get_tasks(self, user_id: int) -> list[Task]:
        pass
    
    @abstractmethod
    def get_task_by_user(self, task_id: int, user_id: int) -> 'Task | None':
        pass

    @abstractmethod
    def update_task(self, model: UpdateTask):
        pass

    @abstractmethod
    def delete_task(self, task_id: int):
        pass

    