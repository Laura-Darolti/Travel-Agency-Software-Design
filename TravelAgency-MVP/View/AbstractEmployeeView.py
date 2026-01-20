from abc import abstractmethod,ABC


class AbstractEmployeeView(ABC):


    def reset_table(self):
        pass

    def populate_destinations(self):
        pass

    def open_destination_combo(self):
        pass

    def select_destination(self, event):
        pass

    def populate_price(self):
        pass

    def open_price_combo(self):
        pass

    def select_price(self, event):
        pass

    def display_package(self, package):
        pass

    def open_date_comboboxes(self):
        pass

    def populate_dates(self):
        pass

    def select_by_date(self, event):
        pass

    def selected_dest(self):
        pass

    def open_add_package_window(self):
        pass

    def submit_package(self):
        pass
