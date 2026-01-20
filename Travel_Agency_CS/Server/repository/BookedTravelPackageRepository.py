from Server.Domain.BookedTravelPackage import BookedTravelPackage
from Server.repository.Repository import Repository


class BookedTravelPackageRepository:
    def __init__(self):
        self.repository = Repository(user='root', password='Aou65**lmn8080', host='localhost', database='PS_Database')

    def add_booked_travel_package(self, PackageId, ClientId):
        sql = "INSERT INTO BookedTravelPackage (PackageId, ClientId) VALUES (%s, %s)"
        params = (PackageId, ClientId)
        self.repository.execute_sql_command(sql, params)

    def get_all_booked_travel_packages(self):
        sql = "SELECT * FROM BookedTravelPackage"
        result_set = self.repository.fetch_data(sql)
        booked_packages = [BookedTravelPackage(row['PackageId'], row['ClientId']) for row in result_set]
        return booked_packages

    def update_booked_travel_package(self, package_id, field_values):
        sql = "UPDATE BookedTravelPackage SET "
        params = []

        for field, new_value in field_values.items():
            if new_value is not None:
                sql += f"{field} = %s, "
                params.append(new_value)

        sql = sql[:-2]

        sql += " WHERE PackageId = %s"
        params.append(package_id)

        self.repository.execute_sql_command(sql, params)

    def delete_booked_travel_package(self, package_id):
        sql = "DELETE FROM BookedTravelPackage WHERE PackageId = %s"
        params = (package_id,)
        self.repository.execute_sql_command(sql, params)
