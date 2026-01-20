from Model.AbstractObserver import AbstractObserver
from Model.Repository.TravelPackageRepository import TravelPackageRepository
from Model.Repository.UserRepository import UserRepository


class ModelTravelPackage(AbstractObserver):
    def __init__(self):
        super().__init__()
        self._operation = []
        self._language = 'en'
        self.package_repo = TravelPackageRepository()
        self.operation = ""
        self.selected_format = ""

    @property
    def operation(self):
        return self._operation

    @property
    def language(self):
        return self._language

    @operation.setter
    def operation(self, value):
        self._operation = value
        self.notify_observers()

    @language.setter
    def language(self, new_language):
        self._language = new_language
        self.notify_observers()
