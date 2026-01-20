from Model.AbstractObserver import AbstractObserver
from Model.Repository.ClientRepository import ClientRepository


# from Model.Language import Language

class ModelClients(AbstractObserver):
    def __init__(self):
        super().__init__()
        self._operation = []
        self.language = "english"
        self.cl_repo = ClientRepository()
        self.operation = ""

    @property
    def operation(self):
        return self._operation

    @operation.setter
    def operation(self, value):
        self._operation = value
        self.notify_observers()
