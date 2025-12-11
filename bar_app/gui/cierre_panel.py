import tkinter as tk
from tkinter import ttk, messagebox
from bar_app.logic import cierre

class CierrePanel(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # --- Report Display ---
        report_frame = ttk.LabelFrame(self, text="Daily Sales Report")
        report_frame.pack(fill="both", expand="yes", padx=10, pady=10)

        self.tree = ttk.Treeview(report_frame, columns=("Product", "Qty Sold", "Total Revenue", "Stock Left"), show="headings")
        self.tree.heading("Product", text="Product")
        self.tree.heading("Qty Sold", text="Quantity Sold")
        self.tree.heading("Total Revenue", text="Total Revenue (COP)")
        self.tree.heading("Stock Left", text="Remaining Stock")
        self.tree.pack(fill="both", expand="yes")

        # --- Totals ---
        total_frame = ttk.Frame(self)
        total_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(total_frame, text="Total Daily Revenue:", font=("Arial", 12, "bold")).pack(side="left")
        self.total_revenue_label = ttk.Label(total_frame, text="0 COP", font=("Arial", 12, "bold"))
        self.total_revenue_label.pack(side="left", padx=5)

        # --- Buttons ---
        button_frame = ttk.Frame(self)
        button_frame.pack(fill="x", padx=10, pady=10)

        ttk.Button(button_frame, text="Generate/Refresh Report", command=self.generate_report).pack(side="left", padx=5)

    def generate_report(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        report_data = cierre.get_daily_sales_report()
        for row in report_data:
            self.tree.insert("", "end", values=(row[0], row[1], f"{row[2]:,.0f}", row[3]))

        total_revenue = cierre.get_total_revenue()
        self.total_revenue_label.config(text=f"{total_revenue:,.0f} COP")
