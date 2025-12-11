import tkinter as tk
from tkinter import ttk, messagebox
from bar_app.logic import inventory

class InventoryPanel(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # --- Product List ---
        list_frame = ttk.LabelFrame(self, text="Product List")
        list_frame.pack(fill="both", expand="yes", padx=10, pady=10)

        self.tree = ttk.Treeview(list_frame, columns=("ID", "Name", "Quantity", "Price", "Shortcut"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Quantity", text="Quantity")
        self.tree.heading("Price", text="Price (COP)")
        self.tree.heading("Shortcut", text="Shortcut")
        self.tree.column("ID", width=40)
        self.tree.pack(fill="both", expand="yes")

        self.tree.bind("<<TreeviewSelect>>", self.on_item_select)

        # --- Product Form ---
        form_frame = ttk.LabelFrame(self, text="Product Form")
        form_frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(form_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.name_entry = ttk.Entry(form_frame)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(form_frame, text="Quantity:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.quantity_entry = ttk.Entry(form_frame)
        self.quantity_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(form_frame, text="Price (COP):").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.price_entry = ttk.Entry(form_frame)
        self.price_entry.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        ttk.Label(form_frame, text="Shortcut:").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.shortcut_entry = ttk.Entry(form_frame)
        self.shortcut_entry.grid(row=1, column=3, padx=5, pady=5, sticky="ew")

        form_frame.columnconfigure(1, weight=1)
        form_frame.columnconfigure(3, weight=1)

        # --- Buttons ---
        button_frame = ttk.Frame(self)
        button_frame.pack(fill="x", padx=10, pady=10)

        ttk.Button(button_frame, text="Add", command=self.add_product).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Update", command=self.update_product).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Delete", command=self.delete_product).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Clear Form", command=self.clear_form).pack(side="right", padx=5)

        self.load_products()

    def load_products(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for product in inventory.get_products():
            self.tree.insert("", "end", values=product)

    def on_item_select(self, event):
        selected_item = self.tree.focus()
        if selected_item:
            values = self.tree.item(selected_item, "values")
            self.clear_form()
            self.name_entry.insert(0, values[1])
            self.quantity_entry.insert(0, values[2])
            self.price_entry.insert(0, values[3])
            self.shortcut_entry.insert(0, values[4])

    def clear_form(self):
        self.name_entry.delete(0, "end")
        self.quantity_entry.delete(0, "end")
        self.price_entry.delete(0, "end")
        self.shortcut_entry.delete(0, "end")
        if self.tree.selection():
            self.tree.selection_remove(self.tree.selection())

    def validate_fields(self, shortcut, product_id=None):
        name = self.name_entry.get()
        quantity_str = self.quantity_entry.get()
        price_str = self.price_entry.get()

        if not all([name, quantity_str, price_str, shortcut]):
            messagebox.showerror("Validation Error", "All fields are required.")
            return False

        try:
            int(quantity_str)
            int(price_str)
        except ValueError:
            messagebox.showerror("Validation Error", "Quantity and Price must be integers.")
            return False

        if not inventory.is_shortcut_unique(shortcut, product_id):
            messagebox.showerror("Validation Error", "Shortcut must be unique.")
            return False

        return True

    def add_product(self):
        shortcut = self.shortcut_entry.get()
        if self.validate_fields(shortcut):
            name = self.name_entry.get()
            quantity = int(self.quantity_entry.get())
            price = int(self.price_entry.get())
            inventory.add_product(name, quantity, price, shortcut)
            messagebox.showinfo("Success", "Product added successfully.")
            self.load_products()
            self.clear_form()

    def update_product(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showerror("Error", "Please select a product to update.")
            return

        product_id = self.tree.item(selected_item, "values")[0]
        shortcut = self.shortcut_entry.get()

        if self.validate_fields(shortcut, product_id):
            name = self.name_entry.get()
            quantity = int(self.quantity_entry.get())
            price = int(self.price_entry.get())
            inventory.update_product(product_id, name, quantity, price, shortcut)
            messagebox.showinfo("Success", "Product updated successfully.")
            self.load_products()
            self.clear_form()

    def delete_product(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showerror("Error", "Please select a product to delete.")
            return

        if messagebox.askyesno("Confirm", "Are you sure you want to delete this product?"):
            product_id = self.tree.item(selected_item, "values")[0]
            inventory.delete_product(product_id)
            messagebox.showinfo("Success", "Product deleted successfully.")
            self.load_products()
            self.clear_form()
