
from Server.repository.TravelPackageRepository import TravelPackageRepository
from Server.service.AbsTravelPackageService import AbsTravelPackageService


class TravelPackageService(AbsTravelPackageService):
    def __init__(self):
        self.travel_package_repository = TravelPackageRepository()

    def add_package(self, package_id, destination, price, start_date, end_date):
        self.travel_package_repository.add_package(package_id, destination, price, start_date, end_date)

    def update_package(self, package_id, new_destination, new_price, new_start_date, new_end_date):
        self.travel_package_repository.update_package(package_id, new_destination, new_price, new_start_date,
                                                      new_end_date)

    def delete_package(self, package_id):
        self.travel_package_repository.delete_package(package_id)

    def get_sorted_packages_by_destination_and_period(self):
        return self.travel_package_repository.get_sorted_packages_by_destination_and_period()

    def search_by_destination(self, destination):
        return self.travel_package_repository.search_by_destination(destination)

    def search_by_price(self, min_price, max_price):
        return self.travel_package_repository.search_by_price(min_price, max_price)

    def search_by_dates(self, start_date=None, end_date=None):
        return self.travel_package_repository.search_by_dates(start_date, end_date)

    def get_all_destinations(self):
        return self.travel_package_repository.get_all_destinations()

    def get_all_prices(self):
        return self.travel_package_repository.get_all_prices()

    def get_all_start_dates(self):
        return self.travel_package_repository.get_all_start_dates()

    def get_all_end_dates(self):
        return self.travel_package_repository.get_all_end_dates()
