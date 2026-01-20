from tkinter import simpledialog
from Model.Repository.TravelPackageRepository import TravelPackageRepository
from View.AbstractClientView import AbstractClientView


class ClientPresenter:
    def __init__(self,view):
        self.travel_package_repository = TravelPackageRepository()
        self.view: AbstractClientView = view

    def display_sorted_packages_by_destination_and_period(self):
        sorted_packages = self.travel_package_repository.get_sorted_packages_by_destination_and_period()
        for package in sorted_packages:
            self.view.display_package(package)

    def search_packages_by_destination(self, destination):
        if destination:
            packages = self.travel_package_repository.search_by_destination(destination)
            self.view.reset_table()
            for package in packages:
                self.view.display_package(package)

    def search_packages_by_price(self,price1,price2):
        if price1 and price2:
            packages = self.travel_package_repository.search_by_price(price1,price2)
            self.view.reset_table()
            for package in packages:
                self.view.display_package(package)

    def search_packages_by_dates(self, start_date, end_date):
        destination = self.view.selected_dest
        packages = self.travel_package_repository.search_by_dates(start_date, end_date)
        self.view.reset_table()
        for package in packages:
            self.view.display_package(package)

    def get_all_destinations(self):
        destinations=self.travel_package_repository.get_all_destinations()
        return destinations

