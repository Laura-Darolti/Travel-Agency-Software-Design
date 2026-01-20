from flask import Flask, jsonify, request
from Server.service.TravelPackageService import TravelPackageService

class ClientController:
    def __init__(self, app):
        self.app = app
        self.travel_package_service = TravelPackageService()
        self.setup_routes()

    def setup_routes(self):
        self.app.add_url_rule('/api/sorted-packages', 'sorted_packages',
                              self.display_sorted_packages_by_destination_and_period, methods=['GET'])
        self.app.add_url_rule('/api/search-destination', 'search_destination', self.search_packages_by_destination,
                              methods=['POST'])
        self.app.add_url_rule('/api/search-price', 'search_price', self.search_packages_by_price, methods=['POST'])
        self.app.add_url_rule('/api/search-dates', 'search_dates', self.search_packages_by_dates, methods=['POST'])
        self.app.add_url_rule('/api/destinations', 'destinations', self.get_all_destinations, methods=['GET'])

    def display_sorted_packages_by_destination_and_period(self):
        sorted_packages = self.travel_package_service.get_sorted_packages_by_destination_and_period()
        packages_data = [{'id': package.PackageId, 'destination': package.Destination, 'price': package.Price, 'start_date': package.StartDate, 'end_date': package.EndDate} for package in sorted_packages]
        return jsonify(packages_data), 200

    def search_packages_by_destination(self):
        data = request.json
        destination = data.get('destination')
        if destination:
            packages = self.travel_package_service.search_by_destination(destination)
            packages_data = [{'id': package.PackageId, 'destination': package.Destination, 'price': package.Price, 'start_date': package.StartDate, 'end_date': package.EndDate} for package in packages]
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
            packages_data = [{'id': package.PackageId, 'destination': package.Destination, 'price': package.Price, 'start_date': package.StartDate, 'end_date': package.EndDate} for package in packages]
            return jsonify(packages_data), 200
        return jsonify({"status": "error", "message": "Dates not provided"}), 400

    def get_all_destinations(self):
        destinations = self.travel_package_service.get_all_destinations()
        destinations_data = [{'destination': destination} for destination in destinations]
        return jsonify(destinations_data), 200

