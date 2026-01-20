class TravelPackage:
    def __init__(self, PackageId, Destination, Price, StartDate, EndDate):
        self.PackageId = PackageId
        self.Destination = Destination
        self.Price = Price
        self.StartDate = StartDate
        self.EndDate = EndDate

    def __str__(self):
        return f"Package ID: {self.PackageId}, Destination: {self.Destination}, Price: {self.Price}, Start Date: {self.StartDate}, End Date: {self.EndDate}"

