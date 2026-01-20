from tkinter import simpledialog
from Model.Repository.UserRepository import UserRepository
from View.AbstractLoginView import AbstractLoginView


class LoginPresenter:
    def __init__(self, view):
        self.user_repository = UserRepository()
        self.view: AbstractLoginView = view

    def login_user(self):
        username = self.view.get_username()
        password = self.view.get_password()

        if not username or not password:
            self.view.display_error()
            return

        user_type = self.user_repository.get_user_type(username)
        print (user_type)
        if self.user_repository.check_credentials(username, password):
            self.view.logged_in(user_type[0]['Type'])
        else:
            self.view.display_error()
