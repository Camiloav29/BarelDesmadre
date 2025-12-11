import tkinter as tk
from tkinter import messagebox
from bar_app.logic.auth import verify_user

class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Bar Inventory - Login")
        self.geometry("300x200")

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

        self.login_success = False

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if verify_user(username, password):
            self.login_success = True
            self.destroy()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def is_login_successful(self):
        return self.login_success
