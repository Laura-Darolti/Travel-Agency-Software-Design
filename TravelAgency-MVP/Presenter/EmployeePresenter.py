from tkinter import simpledialog

from Model.Repository.ClientRepository import ClientRepository
from Model.Repository.TravelPackageRepository import TravelPackageRepository
from View import AbstractEmployeeView


class EmployeePresenter:
    def __init__(self, view):
        self.travel_package_repository = TravelPackageRepository()
        self.client_repository = ClientRepository()
        self.view: AbstractEmployeeView = view

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
                ##########  employee  #####################
    def add_package(self, package_id, destination, price, start_date, end_date):
        self.travel_package_repository.add_package(package_id, destination, price, start_date, end_date)

    def update_package(self, selected_package_id, destination, price, start_date, end_date):
        self.travel_package_repository.update_package(selected_package_id,destination,price,start_date,end_date)

    def delete_selected_package(self):
        id= self.view.get_clicked_row_id()
        self.travel_package_repository.delete_package(id)


    ########  CRUD CLIENTI  ################
    def display_clients(self):
        clients = self.client_repository.get_all_clients()
        self.view.reset_table()
        for client in clients:
            self.view.display_package(client)

    def add_client(self, client_id,first_name, last_name):
        self.client_repository.add_client(client_id,first_name,last_name)

    def update_client(self, selected_client_id, fields):
        self.client_repository.update_client(selected_client_id, fields)

    def delete_client(self):
        client_id = self.view.get_clicked_row_id()
        self.client_repository.delete_client(client_id)

