class Client():
    def __init__(self, ClientId, FirstName, LastName):
        self.ClientId = ClientId
        self.FirstName = FirstName
        self.LastName = LastName

    def __str__(self):
        return f"User ID: {self.ClientId}, First Name: {self.FirstName}, Last Name: {self.LastName}"

