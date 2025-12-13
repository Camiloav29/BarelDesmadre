import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from bar_app.logic import billar, inventory, orders

class SalesBillarPanel(ttk.Frame):
    def __init__(self, parent, db_conn, on_sale_confirmed):
        super().__init__(parent)
        self.db_conn = db_conn
        self.on_sale_confirmed = on_sale_confirmed
        self.selected_tab_id = None

        # --- Main Layout (3 columns) ---
        main_frame = ttk.Frame(self)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        main_frame.columnconfigure(0, weight=1) # Open Tabs
        main_frame.columnconfigure(1, weight=2) # Tab Details
        main_frame.columnconfigure(2, weight=1) # Add Product & Product List
        main_frame.rowconfigure(0, weight=1)

        # --- Column 1: Open Tabs ---
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

        # --- Column 2: Tab Details ---
        center_frame = ttk.LabelFrame(main_frame, text="Tab Details")
        center_frame.grid(row=0, column=1, sticky="nsew", padx=5)
        center_frame.rowconfigure(0, weight=1)
        center_frame.columnconfigure(0, weight=1)

        self.details_tree = ttk.Treeview(center_frame, columns=("Product", "Qty", "Price", "Total"), show="headings")
        self.details_tree.heading("Product", text="Product")
        self.details_tree.heading("Qty", text="Qty")
        self.details_tree.heading("Price", text="Unit Price")
        self.details_tree.heading("Total", text="Total")
        self.details_tree.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        ttk.Button(center_frame, text="Liquidate Tab", command=self.liquidate_tab).grid(row=1, column=0, pady=5, padx=5, sticky="ew")

        # --- Column 3: Add Product & Product List ---
        right_frame = ttk.Frame(main_frame)
        right_frame.grid(row=0, column=2, sticky="nsew", padx=(5, 0))
        right_frame.rowconfigure(1, weight=1)
        right_frame.columnconfigure(0, weight=1)

        add_product_frame = ttk.LabelFrame(right_frame, text="Add Product to Tab")
        add_product_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        add_product_frame.columnconfigure(1, weight=1)

        ttk.Label(add_product_frame, text="Shortcut:").grid(row=0, column=0, padx=5, pady=5)
        self.shortcut_entry = ttk.Entry(add_product_frame)
        self.shortcut_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(add_product_frame, text="Quantity:").grid(row=1, column=0, padx=5, pady=5)
        self.quantity_entry = ttk.Entry(add_product_frame)
        self.quantity_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.quantity_entry.insert(0, "1")

        self.add_product_button = ttk.Button(add_product_frame, text="Add", state="disabled", command=self.add_product_to_tab)
        self.add_product_button.grid(row=2, column=0, columnspan=2, pady=5)

        product_list_frame = ttk.LabelFrame(right_frame, text="Available Products")
        product_list_frame.grid(row=1, column=0, sticky="nsew")
        product_list_frame.rowconfigure(0, weight=1)
        product_list_frame.columnconfigure(0, weight=1)

        self.product_tree = ttk.Treeview(product_list_frame, columns=("Name", "Shortcut"), show="headings")
        self.product_tree.heading("Name", text="Product")
        self.product_tree.heading("Shortcut", text="Shortcut")
        self.product_tree.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        self.update_tabs_list()
        self.load_product_list()

    def load_product_list(self):
        for item in self.product_tree.get_children():
            self.product_tree.delete(item)
        for prod in inventory.get_products(self.db_conn):
            self.product_tree.insert("", "end", values=(prod[1], prod[4]))

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
            self.selected_tab_id = None
            self.clear_details()
            return

        self.selected_tab_id = self.tabs_tree.item(selected_item, "values")[0]
        self.update_details_tree()
        self.add_product_button.config(state="normal")

    def update_details_tree(self):
        for item in self.details_tree.get_children():
            self.details_tree.delete(item)
        if self.selected_tab_id:
            for item in billar.get_tab_items(self.db_conn, self.selected_tab_id):
                name, qty, price, total = item
                self.details_tree.insert("", "end", values=(name, qty, f"{price:,.0f}", f"{total:,.0f}"))

    def add_product_to_tab(self):
        shortcut = self.shortcut_entry.get()
        quantity_str = self.quantity_entry.get()

        if not shortcut or not quantity_str:
            messagebox.showerror("Error", "Shortcut and quantity are required."); return

        try:
            quantity = int(quantity_str)
            if quantity <= 0: raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Invalid quantity."); return

        product = inventory.get_product_by_shortcut(self.db_conn, shortcut)
        if not product:
            messagebox.showerror("Error", "Product not found."); return

        product_id, _, stock, price = product
        if quantity > stock:
            messagebox.showerror("Error", f"Not enough stock. Available: {stock}"); return

        billar.add_item_to_tab(self.db_conn, self.selected_tab_id, product_id, quantity, price)
        self.update_details_tree()
        self.shortcut_entry.delete(0, "end"); self.quantity_entry.delete(0, "end"); self.quantity_entry.insert(0, "1")
        self.on_sale_confirmed()

    def liquidate_tab(self):
        if not self.selected_tab_id:
            messagebox.showerror("Error", "No tab selected."); return

        items = billar.get_tab_items(self.db_conn, self.selected_tab_id)
        if not items:
            if messagebox.askyesno("Confirm", "This tab is empty. Do you want to close it?"):
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
            messagebox.showerror("Error", "Invalid amount paid."); return

        change = paid_with - total
        messagebox.showinfo("Payment Successful", f"Change: {change:,.0f} COP")

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
