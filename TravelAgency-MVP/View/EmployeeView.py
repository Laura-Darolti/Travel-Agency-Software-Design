import tkinter as tk
from tkinter import ttk

from Presenter.EmployeePresenter import EmployeePresenter
from View.AbstractEmployeeView import AbstractEmployeeView


class EmployeeView(AbstractEmployeeView):
    def __init__(self,parent=None):
        self.abs_view=AbstractEmployeeView=self
        self.employeepresenter = EmployeePresenter(self.abs_view)
        self.root = tk.Toplevel(parent)
        self.root.title("Travel Agency")
        self.root.geometry("600x550")
        self.add_package_window = None

        self.root.config(bg="skyblue")

        self.buttons_frame = tk.Frame(self.root, bg="skyblue")
        self.buttons_frame.pack(anchor=tk.NW, padx=10, pady=10)

        self.display_packages_button = tk.Button(self.buttons_frame, text="View Packages",
                                                 command=self.employeepresenter.display_sorted_packages_by_destination_and_period,
                                                 bg="white", fg="black", font=("Arial", 10, "bold"))
        self.display_packages_button.pack(side=tk.LEFT)

        self.get_all_clients_button = tk.Button(self.buttons_frame, text="View Clients",
                                                command=self.employeepresenter.display_clients, bg="white", fg="black",
                                                font=("Arial", 10,"bold"))
        self.get_all_clients_button.pack(side=tk.LEFT,
                                         padx=(10, 0))

        self.packages_listbox = tk.Listbox(self.root)
        self.packages_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.destination_frame = tk.Frame(self.root, bg="skyblue")
        self.destination_frame.pack(anchor=tk.NW, padx=10, pady=10)

        self.destination_button = tk.Button(self.destination_frame, text="Destination",
                                            command=self.open_destination_combo)
        self.destination_button.pack(side=tk.LEFT)

        self.destination_var = tk.StringVar()
        self.destination_combobox = ttk.Combobox(self.destination_frame, textvariable=self.destination_var)
        self.destination_combobox.pack(side=tk.LEFT)
        self.destination_combobox.pack_forget()
        self.destination_combobox.bind("<<ComboboxSelected>>", self.select_destination)

        self.price_frame = tk.Frame(self.root, bg="skyblue")
        self.price_frame.pack(anchor=tk.NW, padx=10, pady=10)

        self.price_button = tk.Button(self.price_frame, text="Price", command=self.open_price_combo)
        self.price_button.pack(side=tk.LEFT)

        self.price_var = tk.StringVar()
        self.price_combobox = ttk.Combobox(self.price_frame, textvariable=self.price_var)
        self.price_combobox.pack(side=tk.LEFT)
        self.price_combobox.pack_forget()
        self.price_combobox.bind("<<ComboboxSelected>>", self.select_price)

        self.select_dates_frame = tk.Frame(self.root, bg="skyblue")
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

        self.buttons_frame2 = tk.Frame(self.root, bg="skyblue")
        self.buttons_frame2.pack(anchor=tk.NW, padx=10, pady=10)

        self.add_package_button = tk.Button(self.buttons_frame2, text="Add Package",
                                            command=self.open_add_package_window, bg="white", fg="black",
                                            font=("Arial", 10))
        self.add_package_button.pack(side=tk.LEFT, padx=10)

        self.update_package_button = tk.Button(self.buttons_frame2, text="Update Package",
                                               command=self.open_update_package_window, bg="white", fg="black",
                                               font=("Arial", 10))
        self.update_package_button.pack(side=tk.LEFT, padx=10)

        self.delete_package_button = tk.Button(self.buttons_frame2, text="Delete Package",
                                               command=self.employeepresenter.delete_selected_package, bg="white",
                                               fg="black", font=("Arial", 10))
        self.delete_package_button.pack(side=tk.LEFT, padx=10)

        ###### BUTOANE CRUD CLIENT ###############
        self.buttons_frame3 = tk.Frame(self.root, bg="skyblue")
        self.buttons_frame3.pack(anchor=tk.NW, padx=10, pady=10)

        self.add_client_button = tk.Button(self.buttons_frame3, text="Add Client",
                                           command=self.open_add_client_window, bg="white", fg="black",
                                           font=("Arial", 10))
        self.add_client_button.pack(side=tk.LEFT, padx=10)

        self.update_client_button = tk.Button(self.buttons_frame3, text="Update Client",
                                              command=self.open_update_client_window, bg="white", fg="black",
                                              font=("Arial", 10))
        self.update_client_button.pack(side=tk.LEFT, padx=10)

        self.delete_client_button = tk.Button(self.buttons_frame3, text="Delete Client",
                                              command=self.employeepresenter.delete_client, bg="white",
                                              fg="black", font=("Arial", 10))
        self.delete_client_button.pack(side=tk.LEFT, padx=10)

        ####   aici pt UPDATE     ######
        self.update_package_window=None
        self.package_id_entry=None
        self.destination_entry= None
        self.price_entry= None
        self.start_date_entry= None
        self.end_date_entry= None
        self.package_id_combobox=None
        self.new_destination_entry= None
        self.new_price_entry=None
        self.new_start_date_entry= None
        self.new_end_date_entry= None
        self.update_button= None
        ##########pt add client ########
        self.add_client_window=None
        self.client_id_entry=None
        self.first_name_entry=None
        self.last_name_entry=None
        self.client_id_combobox = None
        self.new_first_name_entry = None
        self.new_last_name_entry = None
        self.submit_cl_button = None

        self.update_client_window=None

    def reset_table(self):
        self.packages_listbox.delete(0, tk.END)

    def populate_destinations(self):

        destinations = self.employeepresenter.travel_package_repository.get_all_destinations()
        self.destination_combobox["values"] = destinations

    def open_destination_combo(self):

        self.destination_combobox.pack(anchor=tk.NW, padx=10, pady=10)

    def select_destination(self, event):
        selected_destination = self.destination_var.get()
        self.employeepresenter.search_packages_by_destination(selected_destination)

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
        self.employeepresenter.search_packages_by_price(min_price, max_price)

    def display_package(self, package):
        self.packages_listbox.insert(tk.END, package)

    def open_date_comboboxes(self):
        self.start_date_combobox.pack(side=tk.LEFT, padx=(10, 5), pady=10)
        self.end_date_combobox.pack(side=tk.LEFT, padx=(5, 10), pady=10)

    def populate_dates(self):
        dates = self.employeepresenter.travel_package_repository.get_all_start_dates()
        self.start_date_combobox["values"] = dates

        dates = self.employeepresenter.travel_package_repository.get_all_end_dates()
        self.end_date_combobox["values"] = dates

    def select_by_date(self, event):
        selected_start_date = self.start_date_var.get()
        selected_end_date = self.end_date_var.get()
        self.employeepresenter.search_packages_by_dates(selected_start_date, selected_end_date)



    #########employeee################
    def open_add_package_window(self):
        self.add_package_window = tk.Toplevel()
        self.add_package_window.title("Add Package")
        self.add_package_window.geometry("300x250")

        tk.Label(self.add_package_window, text="PackageId:").pack()
        self.package_id_entry = tk.Entry(self.add_package_window)
        self.package_id_entry.pack()

        tk.Label(self.add_package_window, text="Destination:").pack()
        self.destination_entry = tk.Entry(self.add_package_window)
        self.destination_entry.pack()

        tk.Label(self.add_package_window, text="Price:").pack()
        self.price_entry = tk.Entry(self.add_package_window)
        self.price_entry.pack()

        tk.Label(self.add_package_window, text="Start Date:").pack()
        self.start_date_entry = tk.Entry(self.add_package_window)
        self.start_date_entry.pack()

        tk.Label(self.add_package_window, text="End Date:").pack()
        self.end_date_entry = tk.Entry(self.add_package_window)
        self.end_date_entry.pack()

        submit_button = tk.Button(self.add_package_window, text="Submit",
                                  command=self.submit_package)
        submit_button.pack()


    def submit_package(self):

        package_id = self.package_id_entry.get()
        destination = self.destination_entry.get()
        price = self.price_entry.get()
        start_date = self.start_date_entry.get()
        end_date = self.end_date_entry.get()

        self.employeepresenter.add_package(package_id, destination, price, start_date, end_date)
        self.add_package_window.destroy()

    def open_update_package_window(self):
        self.update_package_window = tk.Toplevel()
        self.update_package_window.title("Update Package")
        self.update_package_window.geometry("300x250")

        tk.Label(self.update_package_window, text="Select Package ID:").pack()
        self.package_id_combobox = ttk.Combobox(self.update_package_window)
        self.package_id_combobox.pack()

        tk.Label(self.update_package_window, text="New Destination:").pack()
        self.new_destination_entry = tk.Entry(self.update_package_window)
        self.new_destination_entry.pack()

        tk.Label(self.update_package_window, text="New Price:").pack()
        self.new_price_entry = tk.Entry(self.update_package_window)
        self.new_price_entry.pack()

        tk.Label(self.update_package_window, text="New Start Date:").pack()
        self.new_start_date_entry = tk.Entry(self.update_package_window)
        self.new_start_date_entry.pack()

        tk.Label(self.update_package_window, text="New End Date:").pack()
        self.new_end_date_entry = tk.Entry(self.update_package_window)
        self.new_end_date_entry.pack()

        self.update_button = tk.Button(self.update_package_window, text="Update", command=self.update_package)
        self.update_button.pack()

        package_ids = [package.PackageId for package in
                       self.employeepresenter.travel_package_repository.get_sorted_packages_by_destination_and_period()]
        self.package_id_combobox["values"] = package_ids

    def update_package(self):
        selected_package_id = self.package_id_combobox.get()
        new_destination = self.new_destination_entry.get()
        new_price = self.new_price_entry.get()
        new_start_date = self.new_start_date_entry.get()
        new_end_date = self.new_end_date_entry.get()

        self.employeepresenter.update_package(selected_package_id, new_destination, new_price, new_start_date,
                                              new_end_date)
        self.update_package_window.destroy()

    def get_clicked_row_id(self):
        selected_indices = self.packages_listbox.curselection()
        selected_row = self.packages_listbox.get(selected_indices[0]) if selected_indices else None
        return selected_row.split(',')[0].split(':')[1].strip() if selected_row else None

    ######### PT CLIENTI ##############
    def open_add_client_window(self):
        self.add_client_window = tk.Toplevel()
        self.add_client_window.title("Add Client")
        self.add_client_window.geometry("300x250")

        tk.Label(self.add_client_window, text="ClientId:").pack()
        self.client_id_entry = tk.Entry(self.add_client_window)
        self.client_id_entry.pack()

        tk.Label(self.add_client_window, text="First Name:").pack()
        self.first_name_entry = tk.Entry(self.add_client_window)
        self.first_name_entry.pack()

        tk.Label(self.add_client_window, text="Last Name:").pack()
        self.last_name_entry = tk.Entry(self.add_client_window)
        self.last_name_entry.pack()

        submit_cl_button = tk.Button(self.add_client_window, text="Submit",
                                  command=self.submit_client)
        submit_cl_button.pack()


    def submit_client(self):

        client_id = self.client_id_entry.get()
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()

        self.employeepresenter.add_client(client_id, first_name, last_name)
        self.add_client_window.destroy()

    def open_update_client_window(self):
        self.update_client_window = tk.Toplevel()
        self.update_client_window.title("Update Client")
        self.update_client_window.geometry("300x250")

        tk.Label(self.update_client_window, text="Select Client ID:").pack()
        self.client_id_combobox = ttk.Combobox(self.update_client_window)
        self.client_id_combobox.pack()

        tk.Label(self.update_client_window, text="New First Name:").pack()
        self.new_first_name_entry = tk.Entry(self.update_client_window)
        self.new_first_name_entry.pack()

        tk.Label(self.update_client_window, text="New Last Name :").pack()
        self.new_last_name_entry = tk.Entry(self.update_client_window)
        self.new_last_name_entry.pack()

        self.update_button = tk.Button(self.update_client_window, text="Update", command=self.update_client)
        self.update_button.pack()

        package_ids = [package.ClientId for package in
                       self.employeepresenter.client_repository.get_all_clients()]
        self.client_id_combobox["values"] = package_ids

    def update_client(self):
        selected_user_id = self.client_id_combobox.get()
        new_first_name = self.new_first_name_entry.get()
        new_last_name = self.new_last_name_entry.get()
        new_field_dict = {}
        new_field_dict['FirstName'] = new_first_name
        new_field_dict['Lastname'] = new_last_name
        self.employeepresenter.update_client(selected_user_id,new_field_dict)
        self.update_client_window.destroy()



# if __name__ == '__main__':
#     root = tk.Tk()
#     app = EmployeeView()
#     root.mainloop()