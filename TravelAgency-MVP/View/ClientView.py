import tkinter as tk
from tkinter import ttk

from Presenter.ClientPresenter import ClientPresenter
from View.AbstractClientView import AbstractClientView
from View.LoginView import LoginView


class ClientView(AbstractClientView):
    def __init__(self, root):
        self.abs_view:AbstractClientView=self
        self.clientpresenter = ClientPresenter(self.abs_view)
        self.root = root
        self.root.title("Travel Agency")
        self.root.geometry("600x500")

        self.root.config(bg="lightblue")
        self.display_packages_button = tk.Button(root, text="View Packages",
                                                 command=self.clientpresenter.display_sorted_packages_by_destination_and_period,
                                                 bg="white", fg="black", font=("Arial", 12, "bold"))
        self.display_packages_button.pack(anchor=tk.NW, padx=10, pady=10)

        self.packages_listbox = tk.Listbox(self.root)
        self.packages_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.destination_frame = tk.Frame(root, bg="lightblue")
        self.destination_frame.pack(anchor=tk.NW, padx=10, pady=10)

        self.destination_button = tk.Button(self.destination_frame, text="Destination",
                                            command=self.open_destination_combo)
        self.destination_button.pack(side=tk.LEFT)

        self.destination_var = tk.StringVar()
        self.destination_combobox = ttk.Combobox(self.destination_frame, textvariable=self.destination_var)
        self.destination_combobox.pack(side=tk.LEFT)
        self.destination_combobox.pack_forget()
        self.destination_combobox.bind("<<ComboboxSelected>>", self.select_destination)

        self.price_frame = tk.Frame(root, bg="lightblue")
        self.price_frame.pack(anchor=tk.NW, padx=10, pady=10)

        self.price_button = tk.Button(self.price_frame, text="Price", command=self.open_price_combo)
        self.price_button.pack(side=tk.LEFT)

        self.price_var = tk.StringVar()
        self.price_combobox = ttk.Combobox(self.price_frame, textvariable=self.price_var)
        self.price_combobox.pack(side=tk.LEFT)
        self.price_combobox.pack_forget()
        self.price_combobox.bind("<<ComboboxSelected>>", self.select_price)

        self.select_dates_frame = tk.Frame(root, bg="lightblue")
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

        self.login_button = tk.Button(root, text="Login", command=self.open_login_view, bg="blue",
                                      fg="white", font=("Arial", 12, "bold"))
        self.login_button.pack(anchor=tk.NW, padx=10, pady=10)

        self.login_frame = tk.Frame(root, bg="lightblue")
        self.login_frame.pack(side=tk.TOP, anchor=tk.NE, padx=10, pady=10)
    def reset_table(self):
        self.packages_listbox.delete(0, tk.END)

    def populate_destinations(self):
        destinations = self.clientpresenter.get_all_destinations()
        self.destination_combobox["values"] = destinations

    def open_destination_combo(self):
        self.destination_combobox.pack(anchor=tk.NW, padx=10, pady=10)

    def selected_dest(self):
        selected_destination = self.destination_var.get()
        return selected_destination

    def select_destination(self, event):
        selected_destination = self.destination_var.get()
        self.clientpresenter.search_packages_by_destination(selected_destination)

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
        self.clientpresenter.search_packages_by_price(min_price, max_price)

    def display_package(self, package):
        self.packages_listbox.insert(tk.END, package)

    def open_date_comboboxes(self):
        self.start_date_combobox.pack(side=tk.LEFT, padx=(10, 5), pady=10)
        self.end_date_combobox.pack(side=tk.LEFT, padx=(5, 10), pady=10)

    def populate_dates(self):
        dates = self.clientpresenter.travel_package_repository.get_all_start_dates()
        self.start_date_combobox["values"] = dates

        dates = self.clientpresenter.travel_package_repository.get_all_end_dates()
        self.end_date_combobox["values"] = dates

    def select_by_date(self, event):
        selected_start_date = self.start_date_var.get()
        selected_end_date = self.end_date_var.get()
        self.clientpresenter.search_packages_by_dates(selected_start_date, selected_end_date)


    def open_login_view(self):
        self.root.withdraw()
        authentication_dialog = LoginView(self.root)
        self.root.wait_window(authentication_dialog)


if __name__ == "__main__":
     root = tk.Tk()
     app = ClientView(root)
     root.mainloop()
