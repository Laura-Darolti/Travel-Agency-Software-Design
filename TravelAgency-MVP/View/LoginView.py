import tkinter as tk
from tkinter import messagebox

from View.AdministratorView import AdministratorView
from View.EmployeeView import EmployeeView
from Presenter.LoginPresenter import LoginPresenter

class LoginView(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        self.login_presenter = LoginPresenter(self)
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

        # Login button
        tk.Button(self, text="Login", command=self.login_presenter.login_user).pack(pady=(10, 0))

    def get_username(self):
        return self.username_entry.get()

    def get_password(self):
        return self.password_entry.get()

    def display_error(self):
        messagebox.showerror("Login Failed", "Invalid username or password. Please try again.")

    def logged_in(self, user_type):
        self.destroy()
        views={
            "employee":EmployeeView,
            "admin":AdministratorView
        }

        view=views[user_type](parent=self.master)
