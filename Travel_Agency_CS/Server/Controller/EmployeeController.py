from flask import Flask, jsonify, request
from Server.service.TravelPackageService import TravelPackageService
from Server.service.ClientService import ClientService


class EmployeeController:
    def __init__(self, app):
        self.app = app
        self.travel_package_service = TravelPackageService()
        self.client_service = ClientService()
        self.setup_routes()

    def setup_routes(self):
        self.app.add_url_rule('/api/employee/add-client', 'employee_add_client', self.add_client, methods=['POST'])
        self.app.add_url_rule('/api/employee/update-client', 'employee_update_client', self.update_client,
                              methods=['PUT'])
        self.app.add_url_rule('/api/employee/delete-client', 'employee_delete_client', self.delete_client,
                              methods=['DELETE'])
        self.app.add_url_rule('/api/employee/clients', 'employee_clients', self.display_clients, methods=['GET'])
        # Package routes
        self.app.add_url_rule('/api/employee/add-package', 'employee_add_package', self.add_package, methods=['POST'])
        self.app.add_url_rule('/api/employee/update-package', 'employee_update_package', self.update_package,
                              methods=['PUT'])
        self.app.add_url_rule('/api/employee/delete-package', 'employee_delete_package', self.delete_package,
                              methods=['DELETE'])

    def display_sorted_packages_by_destination_and_period(self):
        sorted_packages = self.travel_package_service.get_sorted_packages_by_destination_and_period()
        packages_data = [{'id': package.PackageId, 'destination': package.Destination, 'price': package.Price,
                          'start_date': package.StartDate, 'end_date': package.EndDate} for package in sorted_packages]
        return jsonify(packages_data), 200

    def search_packages_by_destination(self):
        data = request.json
        destination = data.get('destination')
        if destination:
            packages = self.travel_package_service.search_by_destination(destination)
            packages_data = [{'id': package.PackageId, 'destination': package.Destination, 'price': package.Price,
                              'start_date': package.StartDate, 'end_date': package.EndDate} for package in packages]
            return jsonify(packages_data), 200
        return jsonify({"status": "error", "message": "Destination not provided"}), 400

    def search_packages_by_price(self):
        data = request.json
        price_range = data.get('price_range')
        if price_range:
            try:
                price1, price2 = map(int, price_range.split('-'))
                packages = self.travel_package_service.search_by_price(price1, price2)
                packages_data = [{'id': package.PackageId, 'destination': package.Destination, 'price': package.Price,
                                  'start_date': package.StartDate, 'end_date': package.EndDate} for package in packages]
                return jsonify(packages_data), 200
            except ValueError:
                return jsonify({"status": "error", "message": "Invalid price range format"}), 400
        return jsonify({"status": "error", "message": "Price range not provided"}), 400

    def search_packages_by_dates(self):
        data = request.json
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        if start_date and end_date:
            packages = self.travel_package_service.search_by_dates(start_date, end_date)
            packages_data = [{'id': package.PackageId, 'destination': package.Destination, 'price': package.Price,
                              'start_date': package.StartDate, 'end_date': package.EndDate} for package in packages]
            return jsonify(packages_data), 200
        return jsonify({"status": "error", "message": "Dates not provided"}), 400

    def get_all_destinations(self):
        destinations = self.travel_package_service.get_all_destinations()
        destinations_data = [{'destination': destination} for destination in destinations]
        return jsonify(destinations_data), 200
########     CRUD CLIENTI   #############
    def display_clients(self):
        clients = self.client_service.get_all_clients()
        clients_data = [{'id': client.ClientId, 'first_name': client.FirstName, 'last_name': client.LastName} for client
                        in clients]
        return jsonify(clients_data), 200

    def add_client(self):
        data = request.json
        client_id = data.get('client_id')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        if client_id and first_name and last_name:
            self.client_service.add_client(client_id, first_name, last_name)
            return jsonify({"status": "success", "message": "Client added successfully"}), 200
        return jsonify({"status": "error", "message": "Invalid client data"}), 400

    def update_client(self):
        data = request.json
        client_id = data.get('client_id')
        fields = data.get('fields')
        if client_id and fields:
            self.client_service.update_client(client_id, fields)
            return jsonify({"status": "success", "message": "Client updated successfully"}), 200
        return jsonify({"status": "error", "message": "Invalid client data"}), 400

    def delete_client(self):
        data = request.json
        client_id = data.get('client_id')
        if client_id:
            self.client_service.delete_client(client_id)
            return jsonify({"status": "success", "message": "Client deleted successfully"}), 200
        return jsonify({"status": "error", "message": "Client ID not provided"}), 400
                #########   CRUD PACHETE  ############

    def add_package(self):
        data = request.json
        print(data)
        package_id = data.get('packageId')
        destination = data.get('destination')
        price = data.get('price')
        start_date = data.get('startDate')
        end_date = data.get('endDate')
        if (package_id and destination and price and start_date and end_date):
            self.travel_package_service.add_package(package_id, destination, price, start_date, end_date)
            return jsonify({"status": "success", "message": "Package added successfully"}), 200
        return jsonify({"status": "error", "message": "Invalid package data"}), 400

    def update_package(self):
        data = request.json
        print(data)
        package_id = data.get('packageId')

        if not package_id:
            return jsonify({"status": "error", "message": "Package ID is required"}), 400
        updates = {
            'destination': data.get('destination'),
            'price': data.get('price'),
            'startDate': data.get('startDate'),
            'endDate': data.get('endDate')
        }

        # Remove None entries for fields not provided
        updates = {k: v for k, v in updates.items() if v is not None}

        if not updates:
            return jsonify({"status": "error", "message": "No valid fields provided for update"}), 400
        try:
            self.travel_package_service.update_package(package_id, updates)
            return jsonify({"status": "success", "message": "Package updated successfully"}), 200
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 400
    def delete_package(self):
        data = request.json
        package_id = data.get('package_id')
        if package_id:
            self.travel_package_service.delete_package(package_id)
            return jsonify({"status": "success", "message": "Package deleted successfully"}), 200
        return jsonify({"status": "error", "message": "Package ID not provided"}), 400
