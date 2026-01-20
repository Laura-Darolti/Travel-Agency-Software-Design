#from Model.AbstractObserver import AbstractObserver
from Model.Observer import Observer
from Model.Repository.UserRepository import UserRepository


class LoginController(Observer):
    def __init__(self, view):
        super().__init__()
        self.view = view

    def login(self):
        username = self.view.get_username()
        password = self.view.get_password()
        print(username,password)

        if not username or not password:
            self.view.display_error()
            return
        model_users=self.view.model_users
        user_type = model_users.user_repo.get_user_type(username)
        print(user_type)

        if model_users.user_repo.check_credentials(username, password):
            print(username, password)
            model_users.operation = user_type[0].get('Type', '')
            print(model_users.operation)
        else:
            self.view.display_error()


    def update(self):
        pass