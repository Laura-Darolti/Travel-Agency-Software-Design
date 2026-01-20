from abc import ABC
from tkinter import simpledialog
from Model.Observer import Observer

class ClientController(Observer):
        def __init__(self, view):
            super().__init__()
            self.view = view

        def display_sorted_packages_by_destination_and_period(self):
            model_package = self.view.model_package
            sorted_packages = model_package.package_repo.get_sorted_packages_by_destination_and_period()
            self.view.data = sorted_packages
            model_package.operation = "visualisation"
            print(self.view.data)

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
            destination = self.view.selected_dest
            packages = model_package.package_repo.search_by_dates(start_date, end_date)
            self.view.data = packages
            model_package.operation = "visualisation"

        def get_all_destinations(self):
            model_package = self.view.model_package
            destinations = model_package.package_repo.get_all_destinations()
            return destinations

        def login(self):
            self.view.model_package.operation = "login"

        def change_language(self, lang):
            self.view.model_package.operation = "language"
            self.view.model_package.language = lang

        def update(self):
            pass




