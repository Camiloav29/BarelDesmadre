import tkinter as tk
from tkinter import ttk
import sqlite3
from bar_app.gui.login_window import LoginWindow
from bar_app.gui.inventory_panel import InventoryPanel
from bar_app.gui.sales_bar_panel import SalesBarPanel
from bar_app.gui.sales_billar_panel import SalesBillarPanel
from bar_app.gui.cierre_panel import CierrePanel
from bar_app.database.database import init_database

class Application(tk.Tk):
    def __init__(self, user_role):
        super().__init__()
        self.title("Bar Inventory and Sales")
        self.geometry("1024x768")

        self.db_conn = sqlite3.connect('bar_app/database/bar_database.db', check_same_thread=False)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill='both')

        # --- Create all panels first ---
        self.sales_bar_panel = SalesBarPanel(self.notebook, self.db_conn, on_sale_confirmed=self.on_sale_confirmed)
        self.sales_billar_panel = SalesBillarPanel(self.notebook, self.db_conn, on_sale_confirmed=self.on_sale_confirmed)

        # --- Add panels based on role ---
        if user_role == 'admin':
            self.inventory_panel = InventoryPanel(self.notebook, self.db_conn)
            self.cierre_panel = CierrePanel(self.notebook, self.db_conn)

            self.notebook.add(self.inventory_panel, text='Inventory')
            self.notebook.add(self.sales_bar_panel, text='Bar Sales')
            self.notebook.add(self.sales_billar_panel, text='Billar Tabs')
            self.notebook.add(self.cierre_panel, text='Closing')
        else: # Cashier
            self.notebook.add(self.sales_bar_panel, text='Bar Sales')
            self.notebook.add(self.sales_billar_panel, text='Billar Tabs')

    def on_sale_confirmed(self):
        """Callback to refresh panels after a sale."""
        if hasattr(self, 'inventory_panel'):
            self.inventory_panel.load_products()

        # Sales panels always exist, so we can update them
        self.sales_bar_panel.update_history()
        self.sales_bar_panel.load_product_list() # Also refresh product list for stock changes
        self.sales_billar_panel.update_tabs_list()
        self.sales_billar_panel.load_product_list()

        if hasattr(self, 'cierre_panel'):
            self.cierre_panel.generate_report()

    def on_closing(self):
        """Close the database connection and destroy the window."""
        self.db_conn.close()
        self.destroy()

if __name__ == "__main__":
    init_database()
    login_window = LoginWindow()
    login_window.mainloop()

    user_role = login_window.get_user_role()
    if user_role:
        app = Application(user_role)
        app.mainloop()
