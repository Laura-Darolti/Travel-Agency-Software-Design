class BookedTravelPackage():
    def __init__(self,PackageId,ClientId):
        self.ClientId = ClientId
        self.PackageId = PackageId

    def __str__(self):
        return f"User ID: {self.PackageId}, First Name: {self.ClientId}"


