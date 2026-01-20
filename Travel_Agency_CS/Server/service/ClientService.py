from Server.repository.ClientRepository import ClientRepository
from Server.service.AbsClientService import AbsClientService


class ClientService(AbsClientService):
    def __init__(self):
        self.client_repository = ClientRepository()

    def add_client(self, client_id, first_name, last_name):
        self.client_repository.add_client(client_id, first_name, last_name)

    def get_all_clients(self):
        return self.client_repository.get_all_clients()

    def update_client(self, client_id, field_values):
        self.client_repository.update_client(client_id, field_values)

    def delete_client(self, client_id):
        self.client_repository.delete_client(client_id)
