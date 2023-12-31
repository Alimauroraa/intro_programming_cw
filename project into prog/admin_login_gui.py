import pandas as pd
import tkinter as tk
from tkinter import messagebox
from admin_home_frame import admin_home

admin_df = pd.read_csv('admin_credentials.csv')

class Admin:
    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email
        self.created_plans = []  # List of HumanitarianPlans created by this admin

    def create_login_frame(self, admin_login_window, root):
        def check_credentials():
            entered_username = username_entry.get()
            entered_password = int(password_entry.get())

            user = admin_df[
                (admin_df['username'] == entered_username) & (admin_df['user_password'] == entered_password)]
            if not user.empty:
                messagebox.showinfo("Login", f"Access granted, {entered_username}!")
                root.withdraw()
                admin_home(root)
            else:
                messagebox.showerror("Login Error",
                                     "The username or password you have entered is wrong. Please try again!")
                username_entry.delete(0, tk.END)
                password_entry.delete(0, tk.END)

            return entered_username

        def back_to_main():
            # Close the admin login window
            admin_login_window.destroy()

            # Re-display the home window
            root.deiconify()

        # Use admin_login_window for creating frame and widgets
        frame = tk.Frame(admin_login_window, bg='#021631')
        frame.pack(padx=50, pady=50)

        tk.Label(frame, text="Username: ", bg = '#021631', fg = 'white',font=("Calibri", 14)).grid(row=0, column=0)
        username_entry = tk.Entry(frame)
        username_entry.grid(row=0, column=1)

        tk.Label(frame, text="Password: ", bg = '#021631', fg = 'white',font=("Calibri", 14)).grid(row=1, column=0)
        password_entry = tk.Entry(frame, show="*")
        password_entry.grid(row=1, column=1)

        login_button = tk.Button(frame, text="Login", command=check_credentials,font=("Calibri", 12),
        width=16,
        height=0,
        bg="#FFFFFF",
        fg="black",
        cursor="hand2",
        activebackground="#B8B8B8",
        activeforeground="black")
        login_button.grid(row=2, columnspan=2,pady=20)
        back_button = tk.Button(frame, text ="Back", command=back_to_main,font=("Calibri", 12),
        width=16,
        height=0,
        bg="#FFFFFF",
        fg="black",
        cursor="hand2",
        activebackground="#B8B8B8",
        activeforeground="black")
        back_button.grid(row=3, columnspan=2, pady=1)

        root.mainloop()

