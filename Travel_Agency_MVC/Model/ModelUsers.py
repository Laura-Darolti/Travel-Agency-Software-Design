from Model.AbstractObserver import AbstractObserver
from Model.Repository.UserRepository import UserRepository


# from Model.Language import Language

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
