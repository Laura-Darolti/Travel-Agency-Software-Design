from Model.Repository.Repository import Repository
from Model.User import User

from Model.User import User

class UserRepository:
    def __init__(self):
        self.repository = Repository(user='root', password='Aou65**lmn8080', host='localhost', database='PS_Database')

    def add_user(self, UserId, username, password, type):
        sql = "INSERT INTO User (UserID, Username, Password, Type) VALUES (%s, %s,%s, %s)"
        params = (UserId,username, password, type)
        self.repository.execute_sql_command(sql, params)

    def get_all_users(self):
        sql = "SELECT * FROM User"
        result_set = self.repository.fetch_data(sql)
        users = [User(row['UserId'], row['Username'], row['Password'], row['Type']) for row in result_set]
        return users

    def update_user(self, userid, field_values):
        sql = "UPDATE User SET "
        params = []

        for field, new_value in field_values.items():
            if new_value is not None:
                sql += f"{field} = %s, "
                params.append(new_value)


        sql = sql[:-2]

        sql += " WHERE UserId = %s"
        params.append(userid)
        print (sql)
        print(params)
        self.repository.execute_sql_command(sql, params)

    def delete_user(self, id):
        sql = "DELETE FROM User WHERE UserId = %s"
        params = (id,)
        self.repository.execute_sql_command(sql, params)


    def check_credentials(self, username, password):
        sql = "SELECT Password FROM User WHERE Username = %s"
        params = (username,)
        result_set = self.repository.fetch_data(sql, params)

        if result_set:
            stored_password = result_set[0]['Password']
            return stored_password == password
        else:
            return False
    def get_user_type(self,username):
        sql="SELECT Type From User Where Username= %s"
        params=(username,)
        result=self.repository.fetch_data(sql,params)
        return result
