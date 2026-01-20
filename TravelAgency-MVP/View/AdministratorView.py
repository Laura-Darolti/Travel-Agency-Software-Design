import tkinter as tk
from tkinter import ttk

from Presenter.AdministratorPresenter import AdministratorPresenter
from View.AbstractAdministratorView import AbstractAdministratorView
from View.AbstractEmployeeView import AbstractEmployeeView


class AdministratorView(AbstractAdministratorView):
    def __init__(self, parent=None):
        self.abs_view = AbstractAdministratorView = self
        self.adminpresenter = AdministratorPresenter(self.abs_view)
        self.root = tk.Toplevel(parent)
        self.root.title("Travel Agency")
        self.root.geometry("600x550")
        self.root.configure(bg="navy")
        self.add_user_window = None

        self.buttons_frame = tk.Frame(self.root, bg="navy")
        self.buttons_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        self.display_packages_button = tk.Button(self.buttons_frame, text="View Packages",
                                                 command=self.adminpresenter.display_sorted_packages_by_destination_and_period,
                                                 bg="white", fg="black", font=("Arial", 10, "bold"))
        self.display_packages_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.display_users_button = tk.Button(self.buttons_frame, text="View Users",
                                              command=self.adminpresenter.display_users,
                                              bg="white", fg="black", font=("Arial", 10, "bold"))
        self.display_users_button.pack(side=tk.LEFT, padx=(10, 0), pady=10)

        self.packages_listbox = tk.Listbox(self.root)
        self.packages_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.destination_frame = tk.Frame(self.root, bg="navy")
        self.destination_frame.pack(anchor=tk.NW, padx=10, pady=10)

        self.destination_button = tk.Button(self.destination_frame, text="Destination",
                                            command=self.open_destination_combo)
        self.destination_button.pack(side=tk.LEFT)

        self.destination_var = tk.StringVar()
        self.destination_combobox = ttk.Combobox(self.destination_frame, textvariable=self.destination_var)
        self.destination_combobox.pack(side=tk.LEFT)
        self.destination_combobox.pack_forget()
        self.destination_combobox.bind("<<ComboboxSelected>>", self.select_destination)

        self.price_frame = tk.Frame(self.root, bg="navy")
        self.price_frame.pack(anchor=tk.NW, padx=10, pady=10)

        self.price_button = tk.Button(self.price_frame, text="Price", command=self.open_price_combo)
        self.price_button.pack(side=tk.LEFT)

        self.price_var = tk.StringVar()
        self.price_combobox = ttk.Combobox(self.price_frame, textvariable=self.price_var)
        self.price_combobox.pack(side=tk.LEFT)
        self.price_combobox.pack_forget()
        self.price_combobox.bind("<<ComboboxSelected>>", self.select_price)

        self.select_dates_frame = tk.Frame(self.root, bg="navy")
        self.select_dates_frame.pack(anchor=tk.NW, padx=10, pady=10)

        self.select_dates_button = tk.Button(self.select_dates_frame, text="Select Dates",
                                             command=self.open_date_comboboxes)
        self.select_dates_button.pack(side=tk.LEFT)

        self.start_date_var = tk.StringVar()
        self.start_date_combobox = ttk.Combobox(self.select_dates_frame, textvariable=self.start_date_var)
        self.start_date_combobox.pack(side=tk.LEFT)
        self.start_date_combobox.pack_forget()
        self.start_date_combobox.bind("<<ComboboxSelected>>", self.select_by_date)

        self.end_date_var = tk.StringVar()
        self.end_date_combobox = ttk.Combobox(self.select_dates_frame, textvariable=self.end_date_var)
        self.end_date_combobox.pack(side=tk.LEFT)
        self.end_date_combobox.pack_forget()
        self.end_date_combobox.bind("<<ComboboxSelected>>", self.select_by_date)

        self.populate_destinations()
        self.populate_price()
        self.populate_dates()
        ######  Butoane CRUD USER  ############
        self.crud_user_frame = tk.Frame(self.root, bg="navy")
        self.crud_user_frame.pack(anchor=tk.NW, padx=10, pady=10)

        self.add_user_button = tk.Button(self.crud_user_frame, text="Add User",
                                         command=self.open_add_user_window, bg="darkblue", fg="white",
                                         font=("Arial", 10))
        self.add_user_button.pack(side=tk.LEFT, padx=10, pady=5)

        self.update_user_button = tk.Button(self.crud_user_frame, text="Update User",
                                            command=self.open_update_user_window, bg="darkblue", fg="white",
                                            font=("Arial", 10))
        self.update_user_button.pack(side=tk.LEFT, padx=10, pady=5)

        self.delete_user_button = tk.Button(self.crud_user_frame, text="Delete User",
                                            command=self.adminpresenter.delete_selected_user, bg="darkblue",
                                            fg="white", font=("Arial", 10))
        self.delete_user_button.pack(side=tk.LEFT, padx=10, pady=5)

        ####   aici pt UPDATE     ######
        self.update_user_window = None
        self.user_id_entry = None
        self.username_entry = None
        self.password_entry = None
        self.type_entry = None
        self.user_id_combobox = None
        self.new_username_entry = None
        self.new_password_entry = None
        self.new_type_entry = None
        self.update_button = None
    ### CLIENT FUNCTIONALITIES###
    def reset_table(self):
        self.packages_listbox.delete(0, tk.END)
########de schimbat
    def populate_destinations(self):

        destinations = self.adminpresenter.travel_package_repository.get_all_destinations()
        self.destination_combobox["values"] = destinations

    def open_destination_combo(self):

        self.destination_combobox.pack(anchor=tk.NW, padx=10, pady=10)

    def select_destination(self, event):
        selected_destination = self.destination_var.get()
        self.adminpresenter.search_packages_by_destination(selected_destination)

    def populate_price(self):
        prices = [(500, 1000), (1000, 1500), (1500, 2000), (2000, 3000), (3000, 5000)]
        self.price_combobox["values"] = prices

    def open_price_combo(self):
        self.price_combobox.pack(anchor=tk.NW, padx=10, pady=10)

    def select_price(self, event):

        selected_price_str = self.price_var.get()

        prices = selected_price_str.split(' ')
        min_price = prices[0]
        max_price = prices[1]
        print(min_price, max_price)
        self.adminpresenter.search_packages_by_price(min_price, max_price)

    def display_package(self, package):
        self.packages_listbox.insert(tk.END, package)

    def open_date_comboboxes(self):
        self.start_date_combobox.pack(side=tk.LEFT, padx=(10, 5), pady=10)
        self.end_date_combobox.pack(side=tk.LEFT, padx=(5, 10), pady=10)
#####de schimbat
    def populate_dates(self):
        dates = self.adminpresenter.travel_package_repository.get_all_start_dates()
        self.start_date_combobox["values"] = dates

        dates = self.adminpresenter.travel_package_repository.get_all_end_dates()
        self.end_date_combobox["values"] = dates

    def select_by_date(self, event):
        selected_start_date = self.start_date_var.get()
        selected_end_date = self.end_date_var.get()
        self.adminpresenter.search_packages_by_dates(selected_start_date, selected_end_date)

    ######### ADMINISTRATOR FCT ################

    def open_add_user_window(self):
        self.add_user_window = tk.Toplevel()
        self.add_user_window.title("Add User")
        self.add_user_window.geometry("300x200")

        tk.Label(self.add_user_window, text="UserId:").pack()
        self.user_id_entry = tk.Entry(self.add_user_window)
        self.user_id_entry.pack()

        tk.Label(self.add_user_window, text="Username:").pack()
        self.username_entry = tk.Entry(self.add_user_window)
        self.username_entry.pack()

        tk.Label(self.add_user_window, text="Password:").pack()
        self.password_entry = tk.Entry(self.add_user_window)
        self.password_entry.pack()

        tk.Label(self.add_user_window, text="Type:").pack()
        self.type_entry = tk.Entry(self.add_user_window)
        self.type_entry.pack()

        submit_button = tk.Button(self.add_user_window, text="Submit",
                                  command=self.submit_user)
        submit_button.pack()

    def submit_user(self):
        user_id = self.user_id_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()
        type = self.type_entry.get()

        self.adminpresenter.add_user(user_id, username, password, type)
        self.add_user_window.destroy()

    def open_update_user_window(self):
        self.update_user_window = tk.Toplevel()
        self.update_user_window.title("Update User")
        self.update_user_window.geometry("300x250")

        tk.Label(self.update_user_window, text="Select User ID:").pack()
        self.user_id_combobox = ttk.Combobox(self.update_user_window)
        self.user_id_combobox.pack()

        tk.Label(self.update_user_window, text="New Username:").pack()
        self.new_username_entry = tk.Entry(self.update_user_window)
        self.new_username_entry.pack()

        tk.Label(self.update_user_window, text="New Password:").pack()
        self.new_password_entry = tk.Entry(self.update_user_window)
        self.new_password_entry.pack()

        tk.Label(self.update_user_window, text="New Type:").pack()
        self.new_type_entry = tk.Entry(self.update_user_window)
        self.new_type_entry.pack()

        self.update_button = tk.Button(self.update_user_window, text="Update", command=self.update_user)
        self.update_button.pack()
        ######de schimbat
        package_ids = [package.UserId for package in
                       self.adminpresenter.user_repository.get_all_users()]
        self.user_id_combobox["values"] = package_ids

    def update_user(self):
        selected_user_id = self.user_id_combobox.get()
        new_username = self.new_username_entry.get()
        new_password = self.new_password_entry.get()
        new_type = self.new_type_entry.get()
        new_field_dict = {}
        new_field_dict['Password'] = new_password
        new_field_dict['Username'] = new_username
        new_field_dict['Type'] = new_type
        self.adminpresenter.update_user(selected_user_id,new_field_dict)
        self.update_user_window.destroy()

    def get_clicked_row_id(self):
        selected_indices = self.packages_listbox.curselection()
        selected_row = self.packages_listbox.get(selected_indices[0]) if selected_indices else None
        return selected_row.split(',')[0].split(':')[1].strip() if selected_row else None


# if __name__ == "__main__":
#     root = tk.Tk()
#     app = AdministratorView(root)
#     root.mainloop()