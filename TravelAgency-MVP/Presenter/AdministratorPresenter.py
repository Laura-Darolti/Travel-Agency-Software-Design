from tkinter import simpledialog
from Model.Repository.TravelPackageRepository import TravelPackageRepository
from Model.Repository.UserRepository import UserRepository
from View import AbstractAdministratorView


class AdministratorPresenter:
    def __init__(self, view):
        self.travel_package_repository = TravelPackageRepository()
        self.user_repository = UserRepository()
        self.view: AbstractAdministratorView = view

    def display_sorted_packages_by_destination_and_period(self):
        sorted_packages = self.travel_package_repository.get_sorted_packages_by_destination_and_period()
        self.view.reset_table()
        for package in sorted_packages:
            self.view.display_package(package)

    def search_packages_by_destination(self, destination):
        if destination:
            packages = self.travel_package_repository.search_by_destination(destination)
            self.view.reset_table()
            for package in packages:
                self.view.display_package(package)

    def search_packages_by_price(self, price1, price2):
        if price1 and price2:
            packages = self.travel_package_repository.search_by_price(price1,price2)
            self.view.reset_table()
            for package in packages:
                self.view.display_package(package)

    def search_packages_by_dates(self, start_date, end_date):
        destination = self.view.destination_var.get()
        packages = self.travel_package_repository.search_by_dates(start_date, end_date, destination)
        self.view.reset_table()
        for package in packages:
            self.view.display_package(package)

#############   Administrator   ####################


    def add_user(self, user_id,username,password,type):
        self.user_repository.add_user(user_id, username,password,type)

    def update_user(self,selected_user_id,fields ):
        self.user_repository.update_user(selected_user_id,fields)

    def delete_selected_user(self):
        userid = self.view.get_clicked_row_id()
        self.user_repository.delete_user(userid)

    def display_users(self):
        users = self.user_repository.get_all_users()
        self.view.reset_table()
        for user in users:
            self.view.display_package(user)