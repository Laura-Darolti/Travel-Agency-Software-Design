from tkinter import simpledialog

from Model.Observer import Observer
# from View import EmployeeView
import matplotlib.pyplot as plt
from datetime import datetime
from collections import Counter
import matplotlib.colors as mcolors


class EmployeeController(Observer):
    def __init__(self, view):
        super().__init__()
        self.view = view

    def display_sorted_packages_by_destination_and_period(self):
        model_package = self.view.model_package
        sorted_packages = model_package.package_repo.get_sorted_packages_by_destination_and_period()
        self.view.reset_table()
        for package in sorted_packages:
            self.view.display_package(package)

    def search_packages_by_destination(self, destination):
        model_package = self.view.model_package
        if destination:
            packages = model_package.package_repo.search_by_destination(destination)
            self.view.reset_table()
            for package in packages:
                self.view.display_package(package)

    def search_packages_by_price(self, price1, price2):
        model_package = self.view.model_package
        if price1 and price2:
            packages = model_package.package_repo.search_by_price(price1, price2)
            self.view.reset_table()
            for package in packages:
                self.view.display_package(package)

    def search_packages_by_dates(self, start_date, end_date):
        model_package = self.view.model_package
        destination = self.view.destination_var.get()
        packages = model_package.package_repo.search_by_dates(start_date, end_date, destination)
        self.view.reset_table()
        for package in packages:
            self.view.display_package(package)
            ##########  employee  #####################

    def add_package(self, package_id, destination, price, start_date, end_date):
        model_package = self.view.model_package
        model_package.package_repo.add_package(package_id, destination, price, start_date, end_date)

    def update_package(self, selected_package_id, destination, price, start_date, end_date):
        model_package = self.view.model_package
        model_package.package_repo.update_package(selected_package_id, destination, price, start_date, end_date)

    def delete_selected_package(self):
        model_package = self.view.model_package
        id = self.view.get_clicked_row_id()
        model_package.package_repo.delete_package(id)

    ########  CRUD CLIENTI  ################
    def display_clients(self):
        model_client = self.view.model_clients
        clients = model_client.cl_repo.get_all_clients()
        self.view.reset_table()
        for client in clients:
            self.view.display_package(client)

    def add_client(self, client_id, first_name, last_name):
        model_client = self.view.model_clients
        model_client.cl_repo.add_client(client_id, first_name, last_name)

    def update_client(self, selected_client_id, fields):
        model_client = self.view.model_clients
        model_client.cl_repo.update_client(selected_client_id, fields)

    def delete_client(self):
        model_client = self.view.model_clients
        client_id = self.view.get_clicked_row_id()
        model_client.cl_repo.delete_client(client_id)

    def book_package(self, package_id, client_id):
        model_booked = self.view.model_booked
        model_booked.booked_repo.add_booked_travel_package(package_id, client_id)

    def change_language(self, lang):
        self.view.model_package.operation = "language"
        self.view.model_package.language = lang

    def save_as(self, format):
        self.view.model_package.selected_format = format
        self.view.model_package.operation = "save"

    def set_operation_statistics(self):
        self.view.model_package.operation = "statistics"

    def generate_statistics(self):
        model_package = self.view.model_package
        data = model_package.package_repo.get_sorted_packages_by_destination_and_period()

        destinations = [package.Destination for package in data]
        destination_counts = {dest: destinations.count(dest) for dest in set(destinations)}

        pastel_colors = [mcolors.to_rgba(c, alpha=0.6) for c in list(mcolors.TABLEAU_COLORS.values())]

        figure, ax = plt.subplots(1, 3, figsize=(18, 6))

        ax[0].pie(destination_counts.values(), labels=destination_counts.keys(), autopct='%1.1f%%',
                  colors=pastel_colors)
        ax[0].set_title('Travel Packages by Destination')

        packages_sorted_by_price = sorted(data, key=lambda x: x.Price)

        package_names = [p.Destination for p in packages_sorted_by_price]
        package_prices = [p.Price for p in packages_sorted_by_price]

        ax[1].bar(package_names, package_prices, color='pink')
        ax[1].set_title('Packages by Price')
        ax[1].set_xlabel('Packages')
        ax[1].set_ylabel('Price')
        ax[1].tick_params(axis='x', rotation=90)

        packages_sorted_by_date = sorted(data, key=lambda x: x.StartDate)
        start_dates = [p.StartDate.strftime('%B') for p in packages_sorted_by_date]
        month_counts = Counter(start_dates)

        wedges, texts, autotexts = ax[2].pie(month_counts.values(), labels=month_counts.keys(), autopct='%1.1f%%',
                                             wedgeprops=dict(width=0.4), colors=pastel_colors)
        for autotext in autotexts:
            autotext.set_color('black')
        ax[2].set_title('Upcoming Travel Packages by Start Month')

        plt.tight_layout()
        return figure

    def update(self):
        pass
