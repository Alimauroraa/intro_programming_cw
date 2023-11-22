
from tkinter import *
from tkinter import messagebox
import pandas as pd


user_df = pd.read_csv('volunteers_file.csv')

def login():
    global user_index
    username = enrey1.get()
    password = enrey2.get()

    try:
        password = int(password)
    except ValueError:
        messagebox.showinfo("", "The username or password you have entered is wrong!")
        return None

    user_df = pd.read_csv('volunteers_file.csv')
    user = user_df[(user_df['username'] == username) & (user_df['user_password'] == password)]

    if not user.empty:
        user_index=user.index[0]
        messagebox.showinfo("", f"Access granted, {username}!")
        root.withdraw()  # Hide the login window
        main_application()  # Call the main application window

    else:
        messagebox.showinfo("", "The username or password you have entered is wrong! ")
        user_index=None

def updating():
    global user_df, user_index

    def update_info():
        field_to_update = entry_field.get()
        new_value = entry_value.get()

        valid_fields = ["contact_number", "address1", "address2", "city", "user_email"]

        if field_to_update in valid_fields:
            try:
                if field_to_update == "contact_number":
                    new_value = int(new_value)
            except ValueError:
                result_label.config(text="Invalid input. Please enter a valid value.", fg="red")
                return

            user_df.loc[user_index, field_to_update] = new_value
            result_label.config(text=f"{field_to_update} updated successfully.", fg="green")
            user_df.to_csv('volunteers_file.csv', index=False)
        else:
            result_label.config(text=f"Invalid field to update. Valid fields are: {valid_fields}", fg="red")

    def back_to_main():
        update_window.destroy()

    update_window = Toplevel(root)
    update_window.title("Update Information")

    window_width = 600
    window_height = 300

    screen_width = update_window.winfo_screenwidth()
    screen_height = update_window.winfo_screenheight()

    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2

    update_window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

    Label(update_window, text="Enter field to update: ").pack(pady=10)
    entry_field = Entry(update_window)
    entry_field.pack(pady=10)

    Label(update_window, text="Enter new value: ").pack(pady=10)
    entry_value = Entry(update_window)
    entry_value.pack(pady=10)

    update_button = Button(update_window, text="Update", command=update_info)
    update_button.pack(pady=10)

    back_button = Button(update_window, text="Back", command=back_to_main)
    back_button.pack(pady=10)

    result_label = Label(update_window, text="", fg="black")
    result_label.pack(pady=10)

    def on_enter(event):
        update_info()

    update_window.bind("<Return>", on_enter)

def add_account_window():
    add_window = Toplevel(root)
    add_window.title('Add Account')
    window_width = 300
    window_height = 600

    screen_width = add_window.winfo_screenwidth()
    screen_height = add_window.winfo_screenheight()

    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2

    add_window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
    fields = ["Username", "Password", "First Name", "Last Name", "Birthday", "Phone", "Address1", "Address2", "City",
              "Account Type", "Email", "Gender", "Active", "Availability"]

    entry_vars = []

    for i, field in enumerate(fields):
        Label(add_window, text=f"{field}: ").grid(row=i, column=0, padx=10, pady=5)
        entry_var = StringVar()
        Entry(add_window, textvariable=entry_var).grid(row=i, column=1, padx=10, pady=5)
        entry_vars.append(entry_var)
    back_button = Button(add_window, text="Back", command=add_window.destroy)
    back_button.grid(row=len(fields) + 1, column=0, columnspan=2, pady=10)
    submit_button = Button(add_window, text="Add Volunteer", command=lambda: add_account(entry_vars, add_window))
    submit_button.grid(row=len(fields), column=0, columnspan=2, pady=10)





def add_account(entry_vars, add_window):
    fields = ["username", "user_password", "first_name", "last_name", "birthday", "phone", "address1", "address2", "city",
              "acc_type", "email", "gender", "active", "availability"]
    new_volunteer_info = {fields[i]: entry_var.get() for i, entry_var in enumerate(entry_vars)}
    add_volunteer(**new_volunteer_info)
    user_df.to_csv('volunteers_file.csv', index=False)

    success_label = Label(add_window,text=f"Volunteer {new_volunteer_info['first_name']} {new_volunteer_info['last_name']} added successfully.",fg="green")
    success_label.grid(row=len(fields) + 2, column=0, columnspan=2, pady=10)
    add_window.after(3000, lambda: success_label.destroy())

def display_information():
    display_user_row(user_index, user_df)

def quit_application():

    root.destroy()

def main_application():
    main_window = Toplevel(root)
    main_window.title('Volunteer Management System')

    main_window_width = 400
    main_window_height = 300


    screen_width = main_window.winfo_screenwidth()
    screen_height = main_window.winfo_screenheight()


    x_position = (screen_width - main_window_width) // 2
    y_position = (screen_height - main_window_height) // 2


    main_window.geometry(f"{main_window_width}x{main_window_height}+{x_position}+{y_position}")


    display_button = Button(main_window, text="Display Information", command=display_information)
    display_button.pack(pady=10)

    update_button = Button(main_window, text="Update Information", command=updating)
    update_button.pack(pady=10)

    add_button = Button(main_window, text="Add Account", command=add_account_window)
    add_button.pack(pady=10)

    quit_button = Button(main_window, text="Quit", command=quit_application)
    quit_button.pack(pady=10)

def update_information(user_index, field_to_update, new_value,user_df):
    valid_fields = ["contact_number", "address1", "address2", "city", "user_email"]

    if field_to_update in valid_fields:
        if field_to_update == "phone":
            new_value = int(new_value)
        user_df.loc[user_index, field_to_update] = new_value
        print(f"{field_to_update} updated successfully.")
    else:
        print("Invalid field to update. Valid fields are:", valid_fields)


def add_volunteer(username, user_password, first_name, last_name,birthday, phone, address1, address2, city,acc_type,email,gender,active,availability,):
    global user_df
    new_user_id = user_df['user_id'].max() + 1
    new_volunteer = pd.DataFrame({
        "user_id": [new_user_id],
        "username": [username],
        "user_password": [user_password],
        "first_name": [first_name],
        "last_name": [last_name],
        'dob':[birthday],
        "contact_number": [int(phone)],
        "address1": [address1],
        "address2": [address2],
        "city": [city],
        "acc_type":[acc_type],
        "user_email": [email],
        'gender':[gender],
        'active':[active],
        'availability':[availability],
    })
    user_df = pd.concat([user_df, new_volunteer], ignore_index=True)


def display_user_row(user_index, user_df):
    from tkinter import ttk
    user_row = user_df.loc[[user_index]]
    display_window = Toplevel(root)
    display_window.title("User Information")

    window_width = 400
    window_height = 400

    screen_width = display_window.winfo_screenwidth()
    screen_height = display_window.winfo_screenheight()

    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2

    display_window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

    tree = ttk.Treeview(display_window, columns=("Property", "Value"))

    for col, value in user_row.items():
        tree.insert("", "end", values=(col, value.values[0]))

    tree.column("#0", width=0, stretch="no")  # Hidden column
    tree.column("Property", anchor="w", width=150)
    tree.column("Value", anchor="w", width=150)

    tree.heading("#0", text="", anchor="w")
    tree.heading("Property", text="Property", anchor="w")
    tree.heading("Value", text="Value", anchor="w")

    tree.pack(pady=10,expand=True, fill="y")

    close_button = Button(display_window, text="Back", command=display_window.destroy)
    close_button.pack(pady=10)


root = Tk()
root.title('Volunteer Login')

window_width = 300
window_height = 200

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2

root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")



Label(root, text="Username: ").place(x=20, y=20)
Label(root, text="Password: ").place(x=20, y=70)

global enrey1
global enrey2

enrey1 = Entry(root, bd=5)
enrey1.place(x=140, y=20)

enrey2 = Entry(root, bd=5, show='*')
enrey2.place(x=140, y=70)



Button(root, text="Login", command=login, height=2, width=13, bd=6).place(x=100, y=120)

root.mainloop()
