from abc import ABC


class AbsUserService(ABC):
    def __init__(self):
        pass

    def add_user(self, user_id, username, password, user_type):
        pass

    def get_all_users(self):
        pass

    def update_user(self, user_id, field_values):
        pass

    def delete_user(self, user_id):
        pass

    def check_credentials(self, username, password):
        pass

    def get_user_type(self, username):
        pass

    def get_users_by_type(self, user_type):
        pass
