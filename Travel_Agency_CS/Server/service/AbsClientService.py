from abc import ABC, abstractmethod


class AbsClientService(ABC):

    @abstractmethod
    def add_client(self, client_id, first_name, last_name):
        pass

    @abstractmethod
    def get_all_clients(self):
        pass

    @abstractmethod
    def update_client(self, client_id, field_values):
        pass

    @abstractmethod
    def delete_client(self, client_id):
        pass
