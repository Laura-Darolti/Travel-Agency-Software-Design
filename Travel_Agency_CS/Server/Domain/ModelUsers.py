from Server.Domain.AbstractObserver import AbstractObserver
from Server.repository.UserRepository import UserRepository



class ModelUsers(AbstractObserver):
    def __init__(self):
        super().__init__()
        self._operation = []
        self.language = "english"
        self.user_repo = UserRepository()
        self.operation = "login"

    @property
    def operation(self):
        return self._operation

    @operation.setter
    def operation(self, value):
        self._operation = value
        self.notify_observers()
