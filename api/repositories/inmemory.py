from threading import Lock
from typing import Any

from api.entities.user import AddUser, User
from api.entities.task import AddTask, Task, UpdateTask
from api.protocols import Repository

Model = dict[str, Any]

class InMemoryRepository(Repository):
    def __init__(self) -> None:
        self.lock = Lock()
        self.tables: dict[str, list[Model]] = {
            'users': [],
            'tasks': []
        }
    
    def _next_id(self, table: str) -> int:
        data = self.tables[table]
        if(not data):
            return 0
        return data[-1]['id'] + 1
    
    # ============================== Users ============================== #
    def get_user_by(self, **params: Any) -> 'User | None':
        key, value = params.popitem()
        for user in self.tables['users']:
            if(user[key] == value):
                return User(**user)
        return None

    def add_user(self, model: AddUser) -> User:
        with self.lock:
            id = self._next_id('users')
            user = User(id, **model.to_dict)
            self.tables['users'].append(user.to_dict)
            return user
    
    def get_user_by_email(self, email: str) -> 'User | None':
        with self.lock:
            return self.get_user_by(email=email)
    
    def get_user_by_id(self, id: int) -> 'User | None':
        with self.lock:
            return self.get_user_by(id=id)
        
    def get_user_with_credentials(self, email: str, password: str) -> 'User | None':
        with self.lock:
            for user in self.tables['users']:
                if(user['email'] == email and user['password'] == password):
                    return User(**user)
            return None
    # =================================================================== #
    # ============================== Tasks ============================== #
    def add_task(self, model: AddTask) -> Task:
        with self.lock:
            id = self._next_id('tasks')
            task = Task(id, **model.to_dict)
            self.tables['tasks'].append(task.to_dict)
            return task

    def get_tasks(self, user_id: int) -> list[Task]:
        with self.lock:
            return [
                Task(**item)
                for item in self.tables['tasks']
                if(item['user_id'] == user_id)
            ]
        
    def get_task_by_user(self, task_id: int, user_id: int) -> 'Task | None':
        with self.lock:
            for task in self.tables['tasks']:
                if(task['id'] == task_id and task['user_id'] == user_id):
                    return Task(**task)
            return None
    
    def update_task(self, model: UpdateTask):
        with self.lock:
            for task in self.tables['tasks']:
                if(task['id'] == model.id):
                    task.update(model.to_dict)
    
    def delete_task(self, task_id: int):
        with self.lock:
            for task in self.tables['tasks'].copy():
                if(task['id'] == task_id):
                    self.tables['tasks'].remove(task)
        
    