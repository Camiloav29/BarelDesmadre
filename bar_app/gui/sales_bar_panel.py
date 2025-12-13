import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from bar_app.logic import inventory, orders

class SalesBarPanel(ttk.Frame):
    def __init__(self, parent, db_conn, on_sale_confirmed):
        super().__init__(parent)
        self.db_conn = db_conn
        self.on_sale_confirmed = on_sale_confirmed
        self.current_order_items = []

        # --- Main Layout ---
        main_frame = ttk.Frame(self)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)

        # --- Left Side: Product Selection & Current Order ---
        left_frame = ttk.Frame(main_frame)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        left_frame.rowconfigure(1, weight=1)
        left_frame.columnconfigure(0, weight=1)

        # Product selection
        selection_frame = ttk.LabelFrame(left_frame, text="Add Product")
        selection_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        selection_frame.columnconfigure(1, weight=1)

        ttk.Label(selection_frame, text="Shortcut:").grid(row=0, column=0, padx=5, pady=5)
        self.shortcut_entry = ttk.Entry(selection_frame)
        self.shortcut_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.shortcut_entry.bind("<Return>", self.add_product_to_order)

        ttk.Label(selection_frame, text="Quantity:").grid(row=1, column=0, padx=5, pady=5)
        self.quantity_entry = ttk.Entry(selection_frame)
        self.quantity_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.quantity_entry.insert(0, "1")

        ttk.Button(selection_frame, text="Add to Order", command=self.add_product_to_order).grid(row=2, column=0, columnspan=2, pady=5)

        # Current Order
        current_order_frame = ttk.LabelFrame(left_frame, text="Current Order")
        current_order_frame.grid(row=1, column=0, sticky="nsew")
        current_order_frame.columnconfigure(0, weight=1)
        current_order_frame.rowconfigure(0, weight=1)

        self.order_tree = ttk.Treeview(current_order_frame, columns=("Product", "Qty", "Total"), show="headings")
        self.order_tree.heading("Product", text="Product")
        self.order_tree.heading("Qty", text="Qty")
        self.order_tree.heading("Total", text="Total (COP)")
        self.order_tree.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        # --- Right Side: Finalization & History ---
        right_frame = ttk.Frame(main_frame)
        right_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
        right_frame.rowconfigure(1, weight=1)
        right_frame.columnconfigure(0, weight=1)

        # Finalization
        finalize_frame = ttk.LabelFrame(right_frame, text="Finalize Sale")
        finalize_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        finalize_frame.columnconfigure(1, weight=1)

        ttk.Label(finalize_frame, text="Total Order:", font=("Arial", 12, "bold")).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.total_order_label = ttk.Label(finalize_frame, text="0 COP", font=("Arial", 12, "bold"))
        self.total_order_label.grid(row=0, column=1, padx=5, pady=5, sticky="e")

        ttk.Button(finalize_frame, text="Process Payment", command=self.process_payment).grid(row=1, column=0, columnspan=2, pady=10)
        ttk.Button(finalize_frame, text="Clear Order", command=self.clear_order).grid(row=2, column=0, columnspan=2, pady=5)

        # History
        history_frame = ttk.LabelFrame(right_frame, text="Last 5 Sales")
        history_frame.grid(row=1, column=0, sticky="nsew")
        history_frame.columnconfigure(0, weight=1)
        history_frame.rowconfigure(0, weight=1)

        self.history_tree = ttk.Treeview(history_frame, columns=("ID", "Total", "Time"), show="headings")
        self.history_tree.heading("ID", text="Order ID")
        self.history_tree.heading("Total", text="Total (COP)")
        self.history_tree.heading("Time", text="Time")
        self.history_tree.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        self.update_history()

    def add_product_to_order(self, event=None):
        shortcut = self.shortcut_entry.get()
        quantity_str = self.quantity_entry.get()

        if not shortcut or not quantity_str:
            messagebox.showerror("Error", "Shortcut and quantity are required.")
            return

        try:
            quantity = int(quantity_str)
            if quantity <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Quantity must be a positive integer.")
            return

        product = inventory.get_product_by_shortcut(self.db_conn, shortcut)

        if not product:
            messagebox.showerror("Error", "Product not found.")
            return

        product_id, name, stock, price = product

        if quantity > stock:
            messagebox.showerror("Error", f"Not enough stock for {name}. Available: {stock}")
            return

        # Add to current order list
        self.current_order_items.append({
            "product_id": product_id,
            "name": name,
            "quantity": quantity,
            "price": price,
            "total": price * quantity
        })

        self.update_order_tree()
        self.shortcut_entry.delete(0, "end")
        self.quantity_entry.delete(0, "end")
        self.quantity_entry.insert(0, "1")
        self.shortcut_entry.focus()

    def update_order_tree(self):
        for item in self.order_tree.get_children():
            self.order_tree.delete(item)

        total_order = 0
        for item in self.current_order_items:
            self.order_tree.insert("", "end", values=(item["name"], item["quantity"], f"{item['total']:,.0f}"))
            total_order += item["total"]

        self.total_order_label.config(text=f"{total_order:,.0f} COP")

    def process_payment(self):
        if not self.current_order_items:
            messagebox.showerror("Error", "The order is empty.")
            return

        total_order = sum(item['total'] for item in self.current_order_items)

        paid_with_str = simpledialog.askstring("Payment", f"Total to pay: {total_order:,.0f} COP\n\nEnter amount paid:", parent=self)

        if paid_with_str is None:
            return

        try:
            paid_with = int(paid_with_str)
            if paid_with < total_order:
                raise ValueError
        except (ValueError, TypeError):
            messagebox.showerror("Error", "Invalid amount paid.")
            return

        change = paid_with - total_order
        messagebox.showinfo("Payment Successful", f"Change: {change:,.0f} COP")

        # Record the order in the database
        items_to_record = [(item['product_id'], item['quantity'], item['price']) for item in self.current_order_items]
        orders.create_order(self.db_conn, items_to_record, 'bar')

        self.clear_order()
        self.update_history()
        self.on_sale_confirmed() # Callback to refresh other panels

    def clear_order(self):
        self.current_order_items = []
        self.update_order_tree()

    def update_history(self):
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)

        last_sales = orders.get_last_n_orders(self.db_conn, 5, 'bar')
        for sale in last_sales:
            order_id, total, time = sale
            formatted_time = time.split(" ")[1].split(".")[0]
            self.history_tree.insert("", "end", values=(order_id, f"{total:,.0f}", formatted_time))
