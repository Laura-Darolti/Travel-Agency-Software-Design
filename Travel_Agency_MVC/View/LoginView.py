import tkinter as tk
from tkinter import messagebox

from Controller.LoginController import LoginController
from Model.Observer import Observer
from Model.ModelUsers import ModelUsers
from View.AdministratorView import AdministratorView
from View.EmployeeView import EmployeeView

class LoginView(tk.Toplevel, Observer):
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        self.login_controller = LoginController(self)
        self.model_users = ModelUsers()
        self.title("Login")
        self.geometry("300x200")

        # Username label and entry
        tk.Label(self, text="Username:").pack(pady=(10, 0))
        self.username_entry = tk.Entry(self)
        self.username_entry.pack(pady=(0, 10))

        # Password label and entry
        tk.Label(self, text="Password:").pack(pady=(10, 0))
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack(pady=(0, 10))

        self.model_users.add_observer(self)
        self.model_users.add_observer(self.login_controller)
        # Login button
        tk.Button(self, text="Login", command=self.login_controller.login).pack(pady=(10, 0))

    def get_username(self):
        return self.username_entry.get()

    def get_password(self):
        return self.password_entry.get()

    def display_error(self):
        messagebox.showerror("Login Failed", "Invalid username or password. Please try again.")

    def update(self):
        self.destroy()
        views={
            "employee":EmployeeView,
            "admin":AdministratorView
        }
        # operation_type = self.model_users.operation[0].get('Type', '')
        print(self.model_users.operation)
        if self.model_users.operation == "admin":
            print("admin view")
            view=views[self.model_users.operation](parent=self.master)
        elif self.model_users.operation == "employee":
            view=views[self.model_users.operation](parent=self.master)
            print("employee view")




# if __name__ == "__main__":
#     root = tk.Tk()
#     app = LoginView(root)
#     root.mainloop()
