import tkinter as tk
from tkinter import messagebox
import sqlite3
from bar_app.logic.auth import verify_user

class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Bar Inventory - Login")
        self.geometry("300x200")

        self.db_conn = sqlite3.connect('bar_app/database/bar_database.db')

        # Placeholder for the bar logo
        self.logo_label = tk.Label(self, text="[ BAR LOGO ]", font=("Arial", 16, "bold"))
        self.logo_label.pack(pady=10)

        self.username_label = tk.Label(self, text="Username")
        self.username_label.pack()
        self.username_entry = tk.Entry(self)
        self.username_entry.pack()

        self.password_label = tk.Label(self, text="Password")
        self.password_label.pack()
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        self.login_button = tk.Button(self, text="Login", command=self.login)
        self.login_button.pack(pady=10)

        self.user_role = None
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        role = verify_user(self.db_conn, username, password)
        if role:
            self.user_role = role
            self.db_conn.close()
            self.destroy()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def get_user_role(self):
        return self.user_role

    def on_closing(self):
        self.db_conn.close()
        self.destroy()
