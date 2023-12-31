import pandas as pd
import tkinter as tk
from tkinter import messagebox

admin_df = pd.read_csv('admin_credentials.csv')
class Admin:
    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email
        self.created_plans = []  # List of HumanitarianPlans created by this admin

    def AdminLogin(self):
        def check_credentials():
            entered_username = username_entry.get()
            entered_password = int(password_entry.get())

            user = admin_df[
                (admin_df['username'] == entered_username) & (admin_df['user_password'] == entered_password)]
            if not user.empty:
                messagebox.showinfo("Login", f"Access granted, {entered_username}!")
                root.destroy()
            else:
                messagebox.showerror("Login Error", "The username or password you have entered is wrong. Please try again!")
                username_entry.delete(0, tk.END)
                password_entry.delete(0, tk.END)

        root = tk.Tk()
        root.title("Admin Login")

        frame = tk.Frame(root)
        frame.pack(padx=50, pady=50)

        tk.Label(frame, text="Username: ").grid(row=0, column=0)
        username_entry = tk.Entry(frame)
        username_entry.grid(row=0, column=1)

        tk.Label(frame, text="Password: ").grid(row=1, column=0)
        password_entry = tk.Entry(frame, show="*")
        password_entry.grid(row=1, column=1)

        login_button = tk.Button(frame, text="Login", command=check_credentials)
        login_button.grid(row=2, columnspan=2)

        root.mainloop()


user = Admin("", "", "")
user.AdminLogin()
