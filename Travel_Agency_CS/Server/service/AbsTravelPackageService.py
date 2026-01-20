from abc import ABC, abstractmethod
from typing import List
from Server.Domain.TravelPackage import TravelPackage


class AbsTravelPackageService(ABC):
    @abstractmethod
    def add_package(self, package_id: int, destination: str, price: float, start_date: str, end_date: str):
        pass

    @abstractmethod
    def update_package(self, package_id: int, new_destination: str, new_price: float, new_start_date: str,
                       new_end_date: str):
        pass

    @abstractmethod
    def delete_package(self, package_id: int):
        pass

    @abstractmethod
    def get_sorted_packages_by_destination_and_period(self) -> List[TravelPackage]:
        pass

    @abstractmethod
    def search_by_destination(self, destination: str) -> List[TravelPackage]:
        pass

    @abstractmethod
    def search_by_price(self, min_price: float, max_price: float) -> List[TravelPackage]:
        pass

    @abstractmethod
    def search_by_dates(self, start_date: str = None, end_date: str = None) -> List[TravelPackage]:
        pass

    @abstractmethod
    def get_all_destinations(self) -> List[str]:
        pass

    @abstractmethod
    def get_all_prices(self) -> List[float]:
        pass

    @abstractmethod
    def get_all_start_dates(self) -> List[str]:
        pass

    @abstractmethod
    def get_all_end_dates(self) -> List[str]:
        pass
