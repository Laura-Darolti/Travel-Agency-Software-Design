import tkinter as tk
from tkinter import ttk
import os
import csv
import json
from xml.etree.ElementTree import Element, SubElement, ElementTree
from docx import Document
from Controller.EmployeeController import EmployeeController
from Model.ModelBookedPackage import ModelBookedPackage
from Model.ModelClients import ModelClients
from Model.ModelTravelPackage import ModelTravelPackage
from Model.Observer import Observer
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class EmployeeView(Observer):
    def __init__(self, parent=None):
        self.emp_con = EmployeeController(self)
        self.model_package = ModelTravelPackage()
        self.model_clients = ModelClients()
        self.model_booked = ModelBookedPackage()
        self.root = tk.Toplevel(parent)
        self.root.title("Travel Agency")
        self.root.geometry("600x550")
        self.add_package_window = None
        self.data = []
        self.language = 'en'
        self.root.config(bg="skyblue")

        self.buttons_frame = tk.Frame(self.root, bg="skyblue")
        self.buttons_frame.pack(anchor=tk.NW, padx=10, pady=10)

        # Language selection menu
        self.language_var = tk.StringVar(value=self.language)
        language_menu = ttk.OptionMenu(self.root, self.language_var, self.language, *languages.keys(),
                                       command=lambda lang: self.emp_con.change_language(lang))

        language_menu.pack(side=tk.TOP, anchor=tk.E)
        # Add Save As button with dropdown for format selection
        self.save_format_var = tk.StringVar(value='csv')
        self.save_frame = tk.Frame(self.root, bg="skyblue")
        self.save_frame.pack(anchor=tk.NW, padx=10, pady=10)

        self.save_as_button = tk.Button(self.save_frame, text="Save As", command=self.save_as, bg="white", fg="black",
                                        font=("Arial", 10))
        self.save_as_button.pack(side=tk.LEFT, padx=10)

        self.save_format_combobox = ttk.Combobox(self.save_frame, textvariable=self.save_format_var,
                                                 values=['csv', 'json', 'xml', 'doc'])
        self.save_format_combobox.pack(side=tk.LEFT, padx=10)
        # Add button for visualizing statistics
        self.view_statistics_button = tk.Button(self.buttons_frame, text="View Statistics",
                                                command=self.emp_con.set_operation_statistics, bg="white", fg="black",
                                                font=("Arial", 10, "bold"))
        self.view_statistics_button.pack(side=tk.LEFT, padx=10)
        self.display_packages_button = tk.Button(self.buttons_frame, text="View Packages",
                                                 command=self.emp_con.display_sorted_packages_by_destination_and_period,
                                                 bg="white", fg="black", font=("Arial", 10, "bold"))
        self.display_packages_button.pack(side=tk.LEFT)

        self.get_all_clients_button = tk.Button(self.buttons_frame, text="View Clients",
                                                command=self.emp_con.display_clients, bg="white", fg="black",
                                                font=("Arial", 10, "bold"))
        self.get_all_clients_button.pack(side=tk.LEFT,
                                         padx=(10, 0))

        self.packages_listbox = tk.Listbox(self.root)
        self.packages_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.packages_listbox.bind("<Double-1>", self.on_row_double_click)

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

        self.model_package.add_observer(self)
        self.model_package.add_observer(self.emp_con)

        self.model_clients.add_observer(self)
        self.model_clients.add_observer(self.emp_con)

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
                                               command=self.emp_con.delete_selected_package, bg="white",
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
                                              command=self.emp_con.delete_client, bg="white",
                                              fg="black", font=("Arial", 10))
        self.delete_client_button.pack(side=tk.LEFT, padx=10)
        # tema 3 butoane
        self.book_package_button = tk.Button(self.buttons_frame3, text="Book Package",
                                             command=self.open_book_package_window, bg="white", fg="black",
                                             font=("Arial", 10))
        self.book_package_button.pack(side=tk.LEFT, padx=10)

        ####   aici pt UPDATE     ######
        self.update_package_window = None
        self.package_id_entry = None
        self.destination_entry = None
        self.price_entry = None
        self.start_date_entry = None
        self.end_date_entry = None
        self.package_id_combobox = None
        self.new_destination_entry = None
        self.new_price_entry = None
        self.new_start_date_entry = None
        self.new_end_date_entry = None
        self.update_button = None
        ##########pt add client ########
        self.add_client_window = None
        self.client_id_entry = None
        self.first_name_entry = None
        self.last_name_entry = None
        self.client_id_combobox = None
        self.new_first_name_entry = None
        self.new_last_name_entry = None
        self.submit_cl_button = None

        self.update_client_window = None

    def reset_table(self):
        self.packages_listbox.delete(0, tk.END)

    def populate_destinations(self):
        destinations = self.model_package.package_repo.get_all_destinations()
        self.destination_combobox["values"] = destinations

    def open_destination_combo(self):
        self.destination_combobox.pack(anchor=tk.NW, padx=10, pady=10)

    def select_destination(self, event):
        selected_destination = self.destination_var.get()
        self.emp_con.search_packages_by_destination(selected_destination)

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
        self.emp_con.search_packages_by_price(min_price, max_price)

    def display_package(self, package):
        self.packages_listbox.insert(tk.END, package)

    def open_date_comboboxes(self):
        self.start_date_combobox.pack(side=tk.LEFT, padx=(10, 5), pady=10)
        self.end_date_combobox.pack(side=tk.LEFT, padx=(5, 10), pady=10)

    def populate_dates(self):
        dates = self.model_package.package_repo.get_all_start_dates()
        self.start_date_combobox["values"] = dates

        dates = self.model_package.package_repo.get_all_end_dates()
        self.end_date_combobox["values"] = dates

    def select_by_date(self, event):
        selected_start_date = self.start_date_var.get()
        selected_end_date = self.end_date_var.get()
        self.emp_con.search_packages_by_dates(selected_start_date, selected_end_date)

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

        self.emp_con.add_package(package_id, destination, price, start_date, end_date)
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
                       self.model_package.package_repo.get_sorted_packages_by_destination_and_period()]
        self.package_id_combobox["values"] = package_ids

    def update_package(self):
        selected_package_id = self.package_id_combobox.get()
        new_destination = self.new_destination_entry.get()
        new_price = self.new_price_entry.get()
        new_start_date = self.new_start_date_entry.get()
        new_end_date = self.new_end_date_entry.get()

        self.emp_con.update_package(selected_package_id, new_destination, new_price, new_start_date,
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

        self.emp_con.add_client(client_id, first_name, last_name)
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
                       self.model_clients.cl_repo.get_all_clients()]
        self.client_id_combobox["values"] = package_ids

    def update_client(self):
        selected_user_id = self.client_id_combobox.get()
        new_first_name = self.new_first_name_entry.get()
        new_last_name = self.new_last_name_entry.get()
        new_field_dict = {}
        new_field_dict['FirstName'] = new_first_name
        new_field_dict['Lastname'] = new_last_name
        self.emp_con.update_client(selected_user_id, new_field_dict)
        self.update_client_window.destroy()

    def set_table(self):
        self.reset_table()
        for line in self.data:
            self.display_package(line)

    def on_row_double_click(self, event):
        package_id = self.get_clicked_row_id()
        if package_id:
            self.open_images(package_id)

    def open_images(self, package_id):
        folder_path = "D:/An3SEM2/PS/Tema3Images"
        image_files = [f for f in os.listdir(folder_path) if f.startswith(str(package_id))]
        for image_file in image_files:
            image_path = os.path.join(folder_path, image_file)
            if os.path.exists(image_path):
                self.show_image_popup(image_path)
            else:
                print(f"Image not found: {image_path}")

    def show_image_popup(self, image_path):
        popup = tk.Toplevel(self.root)
        popup.title("Image Viewer")

        img = Image.open(image_path)
        img = img.resize((400, 300), Image.LANCZOS)  # Use Image.LANCZOS instead of Image.ANTIALIAS
        photo = ImageTk.PhotoImage(img)

        label = tk.Label(popup, image=photo)
        label.image = photo  # Keep a reference to avoid garbage collection
        label.pack()

        close_button = tk.Button(popup, text="Close", command=popup.destroy)
        close_button.pack()

    def open_book_package_window(self):
        self.book_package_window = tk.Toplevel()
        self.book_package_window.title("Book Package")
        self.book_package_window.geometry("300x200")

        tk.Label(self.book_package_window, text="Select Package ID:").pack(pady=5)
        self.package_id_combobox = ttk.Combobox(self.book_package_window)
        self.package_id_combobox.pack(pady=5)

        tk.Label(self.book_package_window, text="Select Client ID:").pack(pady=5)
        self.client_id_combobox = ttk.Combobox(self.book_package_window)
        self.client_id_combobox.pack(pady=5)

        submit_button = tk.Button(self.book_package_window, text="Book", command=self.book_package)
        submit_button.pack(pady=10)

        package_ids = [package.PackageId for package in
                       self.model_package.package_repo.get_sorted_packages_by_destination_and_period()]
        self.package_id_combobox["values"] = package_ids

        client_ids = [client.ClientId for client in self.model_clients.cl_repo.get_all_clients()]
        self.client_id_combobox["values"] = client_ids

    def book_package(self):
        selected_package_id = self.package_id_combobox.get()
        selected_client_id = self.client_id_combobox.get()

        if selected_package_id and selected_client_id:
            self.emp_con.book_package(selected_package_id, selected_client_id)
            self.book_package_window.destroy()

    def save_as(self):
        selected_format = self.save_format_var.get()
        self.emp_con.save_as(selected_format)

    def save_as_csv(self, data, filename):
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['Package ID', 'Destination', 'Price', 'Start Date', 'End Date'])
                for package in data:
                    writer.writerow(
                        [package.PackageId, package.Destination, package.Price, package.StartDate, package.EndDate])
        except Exception as e:
            print(f"Failed to write CSV: {e}")

    def save_as_json(self, data, filename):
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump([{
                'Package ID': package.PackageId,
                'Destination': package.Destination,
                'Price': package.Price,
                'Start Date': str(package.StartDate),  # Convert Start Date to string
                'End Date': str(package.EndDate)  # Convert End Date to string
            } for package in data], file, indent=4)

    def save_as_xml(self, data, filename):
        root = Element('TravelPackages')
        for package in data:
            package_element = SubElement(root, 'Package')
            SubElement(package_element, 'PackageID').text = str(package.PackageId)
            SubElement(package_element, 'Destination').text = package.Destination
            SubElement(package_element, 'Price').text = str(package.Price)
            SubElement(package_element, 'StartDate').text = str(package.StartDate)  # Convert Start Date to string
            SubElement(package_element, 'EndDate').text = str(package.EndDate)  # Convert End Date to string
        tree = ElementTree(root)
        tree.write(filename, xml_declaration=True, encoding='utf-8')

    def save_as_doc(self, data, filename):
        doc = Document()
        for package in data:
            doc.add_paragraph(
                f"Package ID: {package.PackageId}, Destination: {package.Destination}, Price: {package.Price}, Start Date: {package.StartDate}, End Date: {package.EndDate}")
        doc.save(filename)

    def save_data(self, format):
        data = self.model_package.package_repo.get_sorted_packages_by_destination_and_period()
        filename = f'travel_packages.{format}'
        if format == 'csv':
            self.save_as_csv(data, filename)
        elif format == 'json':
            self.save_as_json(data, filename)
        elif format == 'xml':
            self.save_as_xml(data, filename)
        elif format == 'doc':
            self.save_as_doc(data, filename)

    def change_language(self):
        lang = self.model_package.language
        self.display_packages_button.config(text=languages[lang]['view_packages'])
        self.get_all_clients_button.config(text=languages[lang]['view_clients'])
        self.add_package_button.config(text=languages[lang]['add_package'])
        self.update_package_button.config(text=languages[lang]['update_package'])
        self.delete_package_button.config(text=languages[lang]['delete_package'])
        self.add_client_button.config(text=languages[lang]['add_client'])
        self.update_client_button.config(text=languages[lang]['update_client'])
        self.delete_client_button.config(text=languages[lang]['delete_client'])
        self.book_package_button.config(text=languages[lang]['book_package'])
        self.select_dates_button.config(text=languages[lang]['select_dates'])
        self.destination_button.config(text=languages[lang]['destination'])
        self.price_button.config(text=languages[lang]['price'])
        self.save_as_button.config(text=languages[lang]['save_as'])
        self.view_statistics_button.config(text=languages[lang]['view_statistics'])

    def open_statistics_window(self):
        self.stats_window = tk.Toplevel(self.root)
        self.stats_window.title("Statistics")
        self.stats_window.geometry("800x600")

        figure = self.emp_con.generate_statistics()
        canvas = FigureCanvasTkAgg(figure, self.stats_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def update(self):
        operation = self.model_package.operation
        if operation == "language":
            self.change_language()
        elif operation == "visualisation":
            self.set_table()
        elif operation == "save":
            self.save_data(self.model_package.selected_format)
        elif operation == "statistics":
            print("statisici")
            self.open_statistics_window()


languages = {
    'en': {
        'view_packages': "View Packages",
        'view_clients': "View Clients",
        'add_package': "Add Package",
        'update_package': "Update Package",
        'delete_package': "Delete Package",
        'add_client': "Add Client",
        'update_client': "Update Client",
        'delete_client': "Delete Client",
        'book_package': "Book Package",
        'login': "Login",
        'select_dates': "Select Dates",
        'destination': "Destination",
        'price': "Price",
        'save_as': "Save As",
        'view_statistics': "View Statistics"
    },
    'fr': {
        'view_packages': "Voir les forfaits",
        'view_clients': "Voir les clients",
        'add_package': "Ajouter un forfait",
        'update_package': "Mettre à jour le forfait",
        'delete_package': "Supprimer le forfait",
        'add_client': "Ajouter un client",
        'update_client': "Mettre à jour le client",
        'delete_client': "Supprimer le client",
        'book_package': "Réserver le forfait",
        'login': "Connexion",
        'select_dates': "Sélectionner les dates",
        'destination': "Destination",
        'price': "Prix",
        'save_as': "Enregistrer sous",
        'view_statistics': "Voir les statistiques"
    },
    'es': {
        'view_packages': "Ver Paquetes",
        'view_clients': "Ver Clientes",
        'add_package': "Agregar Paquete",
        'update_package': "Actualizar Paquete",
        'delete_package': "Eliminar Paquete",
        'add_client': "Agregar Cliente",
        'update_client': "Actualizar Cliente",
        'delete_client': "Eliminar Cliente",
        'book_package': "Reservar Paquete",
        'login': "Iniciar sesión",
        'select_dates': "Seleccionar fechas",
        'destination': "Destino",
        'price': "Precio",
        'save_as': "Guardar como",
        'view_statistics': "Ver estadísticas"
    },
    'de': {
        'view_packages': "Pakete ansehen",
        'view_clients': "Kunden ansehen",
        'add_package': "Paket hinzufügen",
        'update_package': "Paket aktualisieren",
        'delete_package': "Paket löschen",
        'add_client': "Kunden hinzufügen",
        'update_client': "Kunden aktualisieren",
        'delete_client': "Kunden löschen",
        'book_package': "Paket buchen",
        'login': "Anmelden",
        'select_dates': "Termine auswählen",
        'destination': "Ziel",
        'price': "Preis",
        'save_as': "Speichern als",
        'view_statistics': "Statistiken anzeigen"
    },
    'it': {
        'view_packages': "Visualizza pacchetti",
        'view_clients': "Visualizza clienti",
        'add_package': "Aggiungi pacchetto",
        'update_package': "Aggiorna pacchetto",
        'delete_package': "Elimina pacchetto",
        'add_client': "Aggiungi cliente",
        'update_client': "Aggiorna cliente",
        'delete_client': "Elimina cliente",
        'book_package': "Prenota pacchetto",
        'login': "Accedi",
        'select_dates': "Seleziona date",
        'destination': "Destinazione",
        'price': "Prezzo",
        'save_as': "Salva come",
        'view_statistics': "Visualizza statistiche"
    }
}

# if __name__ == '__main__':
#     root = tk.Tk()
#     app = EmployeeView()
#     root.mainloop()
