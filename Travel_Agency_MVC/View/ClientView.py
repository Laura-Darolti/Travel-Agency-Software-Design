import os
import tkinter as tk
from tkinter import ttk

from Controller.ClientController import ClientController
from Model.ModelTravelPackage import ModelTravelPackage
from Model.Observer import Observer
from View.LoginView import LoginView
from PIL import Image, ImageTk


class ClientView(Observer):
    def __init__(self, root):
        self.client_con = ClientController(self)
        self.model_package = ModelTravelPackage()
        self.root = root
        self.data = []
        self.language = 'en'
        self.root.title("Travel Agency")
        self.root.geometry("600x500")

        self.root.config(bg="lightblue")
        # Language selection menu
        self.language_var = tk.StringVar(value=self.language)
        language_menu = ttk.OptionMenu(root, self.language_var, self.language, *languages.keys(),
                                       command=lambda lang: self.client_con.change_language(lang))

        language_menu.pack(side=tk.TOP, anchor=tk.E)
        # self.setup_ui()
        self.display_packages_button = tk.Button(root, text="View Packages",
                                                 command=self.client_con.display_sorted_packages_by_destination_and_period,
                                                 bg="white", fg="black", font=("Arial", 12, "bold"))
        self.display_packages_button.pack(anchor=tk.NW, padx=10, pady=10)

        self.packages_listbox = tk.Listbox(self.root)
        self.packages_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.packages_listbox.bind("<Double-1>", self.on_row_double_click)

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

        self.login_button = tk.Button(root, text="Login", command=self.client_con.login, bg="blue",
                                      fg="white", font=("Arial", 12, "bold"))
        self.login_button.pack(anchor=tk.NW, padx=10, pady=10)

        self.login_frame = tk.Frame(root, bg="lightblue")
        self.login_frame.pack(side=tk.TOP, anchor=tk.NE, padx=10, pady=10)

        self.model_package.add_observer(self)
        self.model_package.add_observer(self.client_con)

    def reset_table(self):
        self.packages_listbox.delete(0, tk.END)

    def populate_destinations(self):
        destinations = self.client_con.get_all_destinations()
        self.destination_combobox["values"] = destinations

    def open_destination_combo(self):
        self.destination_combobox.pack(anchor=tk.NW, padx=10, pady=10)

    def selected_dest(self):
        selected_destination = self.destination_var.get()
        return selected_destination

    def select_destination(self, event):
        selected_destination = self.destination_var.get()
        self.client_con.search_packages_by_destination(selected_destination)

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
        self.client_con.search_packages_by_price(min_price, max_price)

    def display_package(self, package):
        self.packages_listbox.insert(tk.END, package)

    def set_table(self):
        self.reset_table()
        for line in self.data:
            self.display_package(line)

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
        self.client_con.search_packages_by_dates(selected_start_date, selected_end_date)

    def open_login_view(self):
        self.root.withdraw()
        authentication_dialog = LoginView(self.root)
        self.root.wait_window(authentication_dialog)

    def get_clicked_row_id(self):
        selected_indices = self.packages_listbox.curselection()
        selected_row = self.packages_listbox.get(selected_indices[0]) if selected_indices else None
        return selected_row.split(',')[0].split(':')[1].strip() if selected_row else None

    def on_row_double_click(self, event):
        package_id = self.get_clicked_row_id()
        if package_id:
            self.open_images(package_id)

    def open_images(self, package_id):
        folder_path2 = "D:/An3SEM2/PS/Tema3Images"
        image_files = [f for f in os.listdir(folder_path2) if f.startswith(str(package_id))]

        for image_file in image_files:
            image_path = os.path.join(folder_path2, image_file)
            if os.path.exists(image_path):
                self.show_image_popup(image_path)
            else:
                print(f"Image not found: {image_path}")

    def show_image_popup(self, image_path):
        popup2 = tk.Toplevel(self.root)
        popup2.title("Image Viewer")

        img = Image.open(image_path)
        img = img.resize((400, 300), Image.LANCZOS)  # Use Image.LANCZOS instead of Image.ANTIALIAS
        photo = ImageTk.PhotoImage(img)

        label = tk.Label(popup2, image=photo)
        label.image = photo  # Keep a reference to avoid garbage collection
        label.pack()

        close_button = tk.Button(popup2, text="Close", command=popup2.destroy)
        close_button.pack()

    def change_language(self):
        lang = self.model_package.language
        self.display_packages_button.config(text=languages[lang]['view_packages'])
        self.login_button.config(text=languages[lang]['login'])
        self.select_dates_button.config(text=languages[lang]['select_dates'])
        self.destination_button.config(text=languages[lang]['destination'])
        self.price_button.config(text=languages[lang]['price'])

    def update(self):
        operation = self.model_package.operation
        if operation == "language":
            self.change_language()
        elif operation == "visualisation":
            self.set_table()
        elif operation == "login":
            self.open_login_view()


languages = {
    'en': {
        'view_packages': "View Packages",
        'login': "Login",
        'select_dates': "Select Dates",
        'destination': "Destination",
        'price': "Price"
    },
    'fr': {
        'view_packages': "Voir les forfaits",
        'login': "Connexion",
        'select_dates': "Sélectionner les dates",
        'destination': "Destination",
        'price': "Prix"
    },
    'es': {
        'view_packages': "Ver Paquetes",
        'login': "Iniciar sesión",
        'select_dates': "Seleccionar fechas",
        'destination': "Destino",
        'price': "Precio"
    },
    'de': {
        'view_packages': "Pakete ansehen",
        'login': "Anmelden",
        'select_dates': "Termine auswählen",
        'destination': "Ziel",
        'price': "Preis"
    },
    'it': {
        'view_packages': "Visualizza pacchetti",
        'login': "Accedi",
        'select_dates': "Seleziona date",
        'destination': "Destinazione",
        'price': "Prezzo"
    }
}

if __name__ == "__main__":
    root = tk.Tk()
    app = ClientView(root)
    root.mainloop()
