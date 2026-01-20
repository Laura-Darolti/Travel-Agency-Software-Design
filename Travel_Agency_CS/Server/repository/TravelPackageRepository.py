from Server.Domain.TravelPackage import TravelPackage
from Server.repository.Repository import Repository


class TravelPackageRepository:
    def __init__(self):
        self.repository = Repository(user='root', password='Aou65**lmn8080', host='localhost', database='PS_Database')

    def add_package(self, package_id, destination, price, start_date, end_date):
        sql = "INSERT INTO TravelPackage (PackageId, Destination, Price, StartDate, EndDate) VALUES (%s, %s, %s, %s, %s)"
        params = (package_id, destination, price, start_date, end_date)
        self.repository.execute_sql_command(sql, params)

    def update_package(self, package_id, new_destination, new_price, new_start_date, new_end_date):
        sql = "UPDATE TravelPackage SET Destination = %s, Price = %s, StartDate = %s, EndDate = %s WHERE PackageId = %s"
        params = (new_destination, new_price, new_start_date, new_end_date, package_id)
        self.repository.execute_sql_command(sql, params)

    def delete_package(self, package_id):
        sql = "DELETE FROM TravelPackage WHERE PackageId = %s"
        params = (package_id,)
        self.repository.execute_sql_command(sql, params)

    def get_sorted_packages_by_destination_and_period(self):
        sql = "SELECT * FROM TravelPackage ORDER BY Destination, StartDate, EndDate"
        result_set = self.repository.fetch_data(sql)
        sorted_packages = [
            TravelPackage(row['PackageId'], row['Destination'], row['Price'], row['StartDate'], row['EndDate']) for row
            in result_set]
        return sorted_packages

    def search_by_destination(self, destination):
        sql = "SELECT * FROM TravelPackage WHERE Destination = %s"
        params = (destination,)
        result_set = self.repository.fetch_data(sql, params)
        packages = [
            TravelPackage(row['PackageId'], row['Destination'], row['Price'], row['StartDate'], row['EndDate']) for row
            in result_set]
        return packages

    def search_by_price(self, min_price, max_price):
        sql = "SELECT * FROM TravelPackage WHERE Price BETWEEN %s AND %s"
        params = (min_price, max_price)
        result_set = self.repository.fetch_data(sql, params)
        packages = [
            TravelPackage(row['PackageId'], row['Destination'], row['Price'], row['StartDate'], row['EndDate']) for row
            in result_set]
        return packages

    def search_by_dates(self, start_date=None, end_date=None):
        sql = "SELECT * FROM TravelPackage"
        params=()

        if start_date:
            sql += " WHERE StartDate >= %s"
            params+=(start_date,)
        if end_date:
            sql += " AND EndDate <= %s"
            params+=(end_date,)
        print(sql, params)
        result_set = self.repository.fetch_data(sql, params)
        print (result_set)
        packages = [
            TravelPackage(row['PackageId'], row['Destination'], row['Price'], row['StartDate'], row['EndDate']) for row
            in result_set]
        return packages
    def get_all_destinations(self):
        sql = "SELECT DISTINCT Destination FROM TravelPackage"
        result_set = self.repository.fetch_data(sql)
        destinations = [row['Destination'] for row in result_set]
        return destinations

    def get_all_prices(self):
        sql = "SELECT DISTINCT Price FROM TravelPackage"
        result_set = self.repository.fetch_data(sql)
        prices = [row['Price'] for row in result_set]
        return prices

    def get_all_start_dates(self):
        sql = "SELECT DISTINCT StartDate FROM TravelPackage"
        result_set = self.repository.fetch_data(sql)
        start_dates = [row['StartDate'] for row in result_set]
        return start_dates

    def get_all_end_dates(self):
        sql = "SELECT DISTINCT EndDate FROM TravelPackage"
        result_set = self.repository.fetch_data(sql)
        end_dates = [row['EndDate'] for row in result_set]
        return end_dates