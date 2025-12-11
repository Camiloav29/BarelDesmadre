import tkinter as tk
from tkinter import ttk
from bar_app.gui.login_window import LoginWindow
from bar_app.gui.inventory_panel import InventoryPanel
from bar_app.gui.sales_panel import SalesPanel
from bar_app.gui.cierre_panel import CierrePanel
from bar_app.database.database import init_database

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Bar Inventory and Sales")
        self.geometry("800x600")

        # Create a notebook for tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill='both')

        # Create the panels
        self.inventory_panel = InventoryPanel(self.notebook)
        self.sales_panel = SalesPanel(self.notebook, self.inventory_panel) # Pass inventory_panel reference
        self.cierre_panel = CierrePanel(self.notebook)

        # Add panels to the notebook
        self.notebook.add(self.inventory_panel, text='Inventory')
        self.notebook.add(self.sales_panel, text='Sales')
        self.notebook.add(self.cierre_panel, text='Closing')

if __name__ == "__main__":
    init_database()  # Initialize the database at startup
    login_window = LoginWindow()
    login_window.mainloop()

    if login_window.is_login_successful():
        app = Application()
        app.mainloop()
