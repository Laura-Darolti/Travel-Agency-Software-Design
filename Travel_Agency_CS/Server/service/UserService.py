from Server.repository.UserRepository import UserRepository
from Server.service.AbsUserService import AbsUserService


class UserService(AbsUserService):
    def __init__(self):
        self.user_repository = UserRepository()

    def add_user(self, user_id, username, password, user_type):
        self.user_repository.add_user(user_id, username, password, user_type)

    def get_all_users(self):
        return self.user_repository.get_all_users()

    def update_user(self, user_id, field_values):
        self.user_repository.update_user(user_id, field_values)

    def delete_user(self, user_id):
        self.user_repository.delete_user(user_id)

    def check_credentials(self, username, password):
        return self.user_repository.check_credentials(username, password)

    def get_user_type(self, username):
        return self.user_repository.get_user_type(username)

    def get_users_by_type(self, user_type):
        return self.user_repository.get_users_by_type(user_type)
