from abc import ABC


class AbstractLoginView(ABC):

    def get_username(self):
        pass


    def get_password(self):
        pass


    def display_error(self):
        pass


    def logged_in(self, user_type):
        pass