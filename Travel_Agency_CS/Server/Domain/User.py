class User:
    def __init__(self, UserId, Username, Password, Type):
        self.UserId = UserId
        self.Username = Username
        self.Password = Password
        self.Type = Type

    def __str__(self):
        return f"User ID: {self.UserId}, Username: {self.Username}, Type: {self.Type}"

