from Model.AbstractObserver import AbstractObserver
from Model.Repository.BookedTravelPackageRepository import BookedTravelPackageRepository


# from Model.Language import Language

class ModelBookedPackage(AbstractObserver):
    def __init__(self):
        super().__init__()
        self._operation = []
        self.language = "english"
        self.booked_repo = BookedTravelPackageRepository()
        self.operation = ""

    @property
    def operation(self):
        return self._operation

    @operation.setter
    def operation(self, value):
        self._operation = value
        self.notify_observers()
