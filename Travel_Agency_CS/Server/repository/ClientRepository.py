from Server.repository.Repository import Repository
from Server.Domain.Client import Client

class ClientRepository:
    def __init__(self):
        self.repository = Repository(user='root', password='Aou65**lmn8080', host='localhost', database='PS_Database')

    def add_client(self, ClientId, FirstName, LastName):
        sql = "INSERT INTO Client (ClientId, FirstName, LastName) VALUES (%s, %s, %s)"
        params = (ClientId, FirstName, LastName)
        self.repository.execute_sql_command(sql, params)

    def get_all_clients(self):
        sql = "SELECT * FROM Client"
        result_set = self.repository.fetch_data(sql)
        clients = [Client(row['ClientId'], row['FirstName'], row['LastName']) for row in result_set]
        return clients

    def update_client(self, client_id, field_values):
        sql = "UPDATE Client SET "
        params = []

        for field, new_value in field_values.items():
            if new_value is not None:
                sql += f"{field} = %s, "
                params.append(new_value)

        sql = sql[:-2]

        sql += " WHERE ClientId = %s"
        params.append(client_id)

        self.repository.execute_sql_command(sql, params)

    def delete_client(self, client_id):
        sql = "DELETE FROM Client WHERE ClientId = %s"
        params = (client_id,)
        self.repository.execute_sql_command(sql, params)
