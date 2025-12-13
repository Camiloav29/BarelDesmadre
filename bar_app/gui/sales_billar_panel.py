import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from bar_app.logic import billar, inventory, orders

class SalesBillarPanel(ttk.Frame):
    def __init__(self, parent, db_conn, on_sale_confirmed):
        super().__init__(parent)
        self.db_conn = db_conn
        self.on_sale_confirmed = on_sale_confirmed
        self.selected_tab_id = None

        # --- Main Layout ---
        main_frame = ttk.Frame(self)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=2)
        main_frame.rowconfigure(0, weight=1)

        # --- Left Side: Open Tabs ---
        left_frame = ttk.LabelFrame(main_frame, text="Open Tabs")
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        left_frame.rowconfigure(1, weight=1)
        left_frame.columnconfigure(0, weight=1)

        ttk.Button(left_frame, text="Create New Tab", command=self.create_new_tab).grid(row=0, column=0, pady=5, padx=5, sticky="ew")

        self.tabs_tree = ttk.Treeview(left_frame, columns=("ID", "Customer", "Time"), show="headings")
        self.tabs_tree.heading("ID", text="Tab ID")
        self.tabs_tree.heading("Customer", text="Customer")
        self.tabs_tree.heading("Time", text="Open Since")
        self.tabs_tree.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.tabs_tree.bind("<<TreeviewSelect>>", self.on_tab_select)

        # --- Right Side: Tab Details ---
        right_frame = ttk.LabelFrame(main_frame, text="Tab Details")
        right_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
        right_frame.rowconfigure(1, weight=1)
        right_frame.columnconfigure(0, weight=1)

        # Details tree
        self.details_tree = ttk.Treeview(right_frame, columns=("Product", "Qty", "Price", "Total"), show="headings")
        self.details_tree.heading("Product", text="Product")
        self.details_tree.heading("Qty", text="Qty")
        self.details_tree.heading("Price", text="Unit Price")
        self.details_tree.heading("Total", text="Total")
        self.details_tree.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

        # Buttons
        button_frame = ttk.Frame(right_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=5)
        self.add_product_button = ttk.Button(button_frame, text="Add Product", state="disabled", command=self.add_product_to_tab)
        self.add_product_button.pack(side="left", padx=5)
        self.liquidate_button = ttk.Button(button_frame, text="Liquidate Tab", state="disabled", command=self.liquidate_tab)
        self.liquidate_button.pack(side="right", padx=5)

        self.update_tabs_list()

    def update_tabs_list(self):
        for item in self.tabs_tree.get_children():
            self.tabs_tree.delete(item)
        for tab in billar.get_open_tabs(self.db_conn):
            tab_id, name, time = tab
            formatted_time = time.split(" ")[1].split(".")[0]
            self.tabs_tree.insert("", "end", values=(tab_id, name, formatted_time))
        self.clear_details()

    def create_new_tab(self):
        customer_name = simpledialog.askstring("New Tab", "Enter customer name:", parent=self)
        if customer_name:
            billar.create_tab(self.db_conn, customer_name)
            self.update_tabs_list()

    def on_tab_select(self, event=None):
        selected_item = self.tabs_tree.focus()
        if not selected_item:
            return

        self.selected_tab_id = self.tabs_tree.item(selected_item, "values")[0]
        self.update_details_tree()
        self.add_product_button.config(state="normal")
        self.liquidate_button.config(state="normal")

    def update_details_tree(self):
        for item in self.details_tree.get_children():
            self.details_tree.delete(item)
        if self.selected_tab_id:
            for item in billar.get_tab_items(self.db_conn, self.selected_tab_id):
                self.details_tree.insert("", "end", values=item)

    def add_product_to_tab(self):
        shortcut = simpledialog.askstring("Add Product", "Enter product shortcut:", parent=self)
        if not shortcut: return

        quantity_str = simpledialog.askstring("Add Product", "Enter quantity:", parent=self)
        if not quantity_str: return

        try:
            quantity = int(quantity_str)
            if quantity <= 0: raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Invalid quantity.")
            return

        product = inventory.get_product_by_shortcut(self.db_conn, shortcut)
        if not product:
            messagebox.showerror("Error", "Product not found.")
            return

        product_id, _, stock, price = product
        if quantity > stock:
            messagebox.showerror("Error", f"Not enough stock. Available: {stock}")
            return

        billar.add_item_to_tab(self.db_conn, self.selected_tab_id, product_id, quantity, price)
        self.update_details_tree()
        self.on_sale_confirmed() # To update stock in other views if open

    def liquidate_tab(self):
        items = billar.get_tab_items(self.db_conn, self.selected_tab_id)
        if not items:
            messagebox.showinfo("Info", "This tab has no items. Closing it.")
            billar.close_tab(self.db_conn, self.selected_tab_id)
            self.update_tabs_list()
            return

        total = sum(item[3] for item in items)

        paid_with_str = simpledialog.askstring("Payment", f"Total to pay: {total:,.0f} COP\n\nEnter amount paid:", parent=self)
        if paid_with_str is None: return

        try:
            paid_with = int(paid_with_str)
            if paid_with < total: raise ValueError
        except (ValueError, TypeError):
            messagebox.showerror("Error", "Invalid amount paid.")
            return

        change = paid_with - total
        messagebox.showinfo("Payment Successful", f"Change: {change:,.0f} COP")

        # Convert tab to an order and then close it
        items_for_order = billar.get_tab_items_for_order(self.db_conn, self.selected_tab_id)
        orders.create_order(self.db_conn, items_for_order, 'billar')
        billar.close_tab(self.db_conn, self.selected_tab_id)

        self.update_tabs_list()
        self.on_sale_confirmed()

    def clear_details(self):
        self.selected_tab_id = None
        for item in self.details_tree.get_children():
            self.details_tree.delete(item)
        self.add_product_button.config(state="disabled")
        self.liquidate_button.config(state="disabled")
