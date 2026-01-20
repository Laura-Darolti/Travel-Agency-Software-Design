from tkinter import simpledialog

from Model.Observer import Observer


class AdministratorController(Observer):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(AdministratorController, cls).__new__(cls)
        return cls._instance

    def __init__(self, view):
        if not hasattr(self, 'initialized'):
            super().__init__()
            self.view = view
            self.initialized = True

    def display_sorted_packages_by_destination_and_period(self):
        model_package = self.view.model_package
        sorted_packages = model_package.package_repo.get_sorted_packages_by_destination_and_period()
        self.view.data = sorted_packages
        model_package.operation = "visualisation"

    def search_packages_by_destination(self, destination):
        model_package = self.view.model_package
        if destination:
            packages = model_package.package_repo.search_by_destination(destination)
            self.view.data = packages
        model_package.operation = "visualisation"

    def search_packages_by_price(self, price1, price2):
        model_package = self.view.model_package
        if price1 and price2:
            packages = model_package.package_repo.search_by_price(price1, price2)
            self.view.data = packages
        model_package.operation = "visualisation"

    def search_packages_by_dates(self, start_date, end_date):
        model_package = self.view.model_package
        destination = self.view.destination_var.get()
        packages = model_package.package_repo.search_by_dates(start_date, end_date, destination)
        self.view.data = packages
        model_package.operation = "visualisation"

    #############   Administrator   ####################

    def add_user(self, user_id, username, password, type):
        model_users = self.view.model_users
        model_users.user_repo.add_user(user_id, username, password, type)

    def update_user(self, selected_user_id, fields):
        model_users = self.view.model_users
        model_users.user_repo.update_user(selected_user_id, fields)

    def delete_selected_user(self):
        model_users = self.view.model_users
        userid = self.view.get_clicked_row_id()
        model_users.user_repo.delete_user(userid)

    def display_users(self):
        model_users = self.view.model_users
        users = model_users.user_repo.get_all_users()
        self.view.data = users
        model_users.operation = "visualisation"

    def filter_users_by_type(self, user_type):
        model_users = self.view.model_users
        users = model_users.user_repo.get_users_by_type(user_type)
        self.view.data = users
        model_users.operation = "visualisation"

    def change_language(self, lang):
        self.view.model_package.operation = "language"
        self.view.model_package.language = lang

    def update(self):
        pass
