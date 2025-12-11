import tkinter as tk
from tkinter import ttk, messagebox
from bar_app.logic import sales, inventory

class SalesPanel(ttk.Frame):
    def __init__(self, parent, inventory_panel): # inventory_panel added
        super().__init__(parent)

        self.inventory_panel = inventory_panel # store reference
        self.product = None

        # --- Sale Registration Form ---
        form_frame = ttk.LabelFrame(self, text="Register Sale")
        form_frame.pack(padx=10, pady=10, fill="x")

        ttk.Label(form_frame, text="Product Shortcut:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.shortcut_entry = ttk.Entry(form_frame)
        self.shortcut_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.shortcut_entry.bind("<Return>", self.find_product)

        ttk.Label(form_frame, text="Product Name:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.product_name_label = ttk.Label(form_frame, text="", font=("Arial", 10, "bold"))
        self.product_name_label.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(form_frame, text="Quantity:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.quantity_entry = ttk.Entry(form_frame, validate="key", validatecommand=(self.register(self.validate_integer), '%P'))
        self.quantity_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        self.quantity_entry.bind("<KeyRelease>", self.calculate_total)

        ttk.Label(form_frame, text="Total (COP):").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.total_label = ttk.Label(form_frame, text="0", font=("Arial", 12, "bold"))
        self.total_label.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(form_frame, text="Amount Received (COP):").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.received_entry = ttk.Entry(form_frame, validate="key", validatecommand=(self.register(self.validate_integer), '%P'))
        self.received_entry.grid(row=4, column=1, padx=5, pady=5, sticky="ew")
        self.received_entry.bind("<KeyRelease>", self.calculate_change)

        ttk.Label(form_frame, text="Change (COP):").grid(row=5, column=0, padx=5, pady=5, sticky="w")
        self.change_label = ttk.Label(form_frame, text="0", font=("Arial", 12, "bold"))
        self.change_label.grid(row=5, column=1, padx=5, pady=5, sticky="w")

        form_frame.columnconfigure(1, weight=1)

        # --- Buttons ---
        button_frame = ttk.Frame(self)
        button_frame.pack(fill="x", padx=10, pady=10)

        ttk.Button(button_frame, text="Confirm Sale", command=self.confirm_sale).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Clear", command=self.clear_form).pack(side="right", padx=5)

    def validate_integer(self, value):
        if value.isdigit() or value == "":
            return True
        return False

    def find_product(self, event=None):
        shortcut = self.shortcut_entry.get()
        if not shortcut:
            return

        product = sales.get_product_by_shortcut(shortcut)
        if product:
            self.product = product
            self.product_name_label.config(text=f"{product[1]} (Stock: {product[2]})")
            self.quantity_entry.focus()
            self.calculate_total()
        else:
            messagebox.showerror("Error", "Product not found for this shortcut.")
            self.clear_form()

    def calculate_total(self, event=None):
        if self.product and self.quantity_entry.get():
            try:
                quantity = int(self.quantity_entry.get())
                price = self.product[3]
                total = quantity * price
                self.total_label.config(text=f"{total:,.0f}")
                self.calculate_change()
            except ValueError:
                self.total_label.config(text="0")
        else:
            self.total_label.config(text="0")

    def calculate_change(self, event=None):
        if self.total_label.cget("text") != "0" and self.received_entry.get():
            try:
                total = int(self.total_label.cget("text").replace(",", ""))
                received = int(self.received_entry.get())
                change = received - total
                self.change_label.config(text=f"{change:,.0f}")
            except ValueError:
                self.change_label.config(text="0")
        else:
            self.change_label.config(text="0")

    def confirm_sale(self):
        if not self.product:
            messagebox.showerror("Error", "Please select a product.")
            return

        try:
            quantity = int(self.quantity_entry.get())
            if quantity <= 0:
                messagebox.showerror("Error", "Quantity must be greater than zero.")
                return
        except ValueError:
            messagebox.showerror("Error", "Invalid quantity.")
            return

        stock = self.product[2]
        if quantity > stock:
            messagebox.showerror("Error", f"Not enough stock. Available: {stock}")
            return

        total = int(self.total_label.cget("text").replace(",", ""))

        sales.record_sale(self.product[0], quantity, total)
        messagebox.showinfo("Success", "Sale recorded successfully.")

        # Actualizar la lista de productos en el panel de inventario
        self.inventory_panel.load_products()
        self.clear_form()


    def clear_form(self):
        self.product = None
        self.shortcut_entry.delete(0, "end")
        self.product_name_label.config(text="")
        self.quantity_entry.delete(0, "end")
        self.total_label.config(text="0")
        self.received_entry.delete(0, "end")
        self.change_label.config(text="0")
        self.shortcut_entry.focus()
