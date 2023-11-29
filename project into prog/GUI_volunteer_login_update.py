
from tkinter import *
from tkinter import messagebox
import pandas as pd
from tkinter import ttk

user_df = pd.read_csv('volunteers_file.csv')
bg_color = '#021631'

def login():
    global user_index,user
    username = enrey1.get()
    password = enrey2.get()

    try:
        password = int(password)
    except ValueError:
        messagebox.showinfo("", "Invalid password.")
        return None

    user_df = pd.read_csv('volunteers_file.csv')
    user = user_df[user_df['username'] == username]

    if not user.empty:
        if not pd.isnull(user['camp_id'].iloc[0]) and (user['user_password'].iloc[0] == password):
            user_index = user.index[0]
            if user['active'].iloc[0] == 'False':
                messagebox.showinfo("Warning", "Hey! Your account is not active. Please contact the administrator.")
            else:
                messagebox.showinfo("", f"Access granted, {username}!")
                root.withdraw()  # Hide the login window
                main_application()  # Call the main application window
        else:
            user_index = user.index[0]
            if pd.isnull(user['camp_id'].iloc[0]):
                messagebox.showinfo("Warning", "Hey! Please choose a camp firstly!")
                updating()
            else:
                messagebox.showinfo("", "The password you have entered is wrong!")
    else:
        messagebox.showinfo("", "The user account does not exist!")
        user_index = None

def updating():
    global user_df, user_index
    valid_fields = ["contact_number", "address1", "address2", "city", "user_email", "camp_id"]
    def update_info():
        field_to_update = field_var.get()
        new_value = entry_value.get()

        if field_to_update in valid_fields:
            try:
                if field_to_update == "contact_number":
                    new_value = int(new_value)
                elif field_to_update == "camp_id":
                    new_value = int(new_value)
            except ValueError:
                result_label.config(text="Invalid input. Please enter a valid value.", fg="red",font=("Calibri", 12))
                return

            user_df.loc[user_index, field_to_update] = new_value
            result_label.config(text=f"{field_to_update} updated successfully.", fg="green",font=("Calibri", 12))
            user_df.to_csv('volunteers_file.csv', index=False)
        else:
            result_label.config(text=f"Invalid field to update. Valid fields are:\n {valid_fields}", fg="red",font=("Calibri", 12))

    def back_to_main():
        update_window.destroy()

    def redirect_to_main():
        update_window.destroy()
        main_application()
    # Create the update window
    update_window = Toplevel(root)
    update_window.title("Update Information")
    update_window['bg'] = '#021631'
    # Set window size
    window_width = 480
    window_height = 340



    # Get screen width and height
    screen_width = update_window.winfo_screenwidth()
    screen_height = update_window.winfo_screenheight()

    # Calculate the position to center the window
    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2

    # Set the window geometry
    update_window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

    Label(update_window, text="Select field to update: ",bg=bg_color,fg="white",font=("Calibri", 14)).pack(pady=10)
    field_var = ttk.Combobox(update_window, values=valid_fields)
    field_var.pack(pady=10)
    field_var.set("Choose a field")

    Label(update_window, text="Enter new value: ",bg=bg_color,fg="white",font=("Calibri", 14)).pack(pady=10)
    entry_value = Entry(update_window)
    entry_value.pack(pady=10)


    # Button(update_window, text="Update", command=update_info).pack(pady=10)
    update_button = Button(update_window, text="Update", command=update_info)
    update_button.pack(pady=10)

    if pd.isnull(user['camp_id'].iloc[0]):
        # Add the redirect_button only when the condition is true
        redirect_button = Button(update_window, text="Redirect to Main", command=redirect_to_main)
        redirect_button.pack(pady=10)
    else:
        # Add the back_button when the condition is false
        back_button = Button(update_window, text="Back", command=back_to_main)
        back_button.pack(pady=10)
    # redirect_button = Button(update_window, text="Redirect to Main", command=redirect_to_main)
    # redirect_button.pack(pady=10)

    result_label = Label(update_window,bg='#021631')
    result_label.pack(pady=10)
    # Add functionality to simulate "Enter" key press
    def on_enter(event):
        update_info()

    update_window.bind("<Return>", on_enter)

def create_account_window():
    add_window = Toplevel(root)
    add_window.title('Create Account')
    window_width = 300
    window_height = 650
    add_window['bg'] = '#021631'
    # Get screen width and height
    screen_width = add_window.winfo_screenwidth()
    screen_height = add_window.winfo_screenheight()

    # Calculate the position to center the window
    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2

    # Set the window geometry
    add_window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
    fields = ["Username", "Password", "First Name", "Last Name", "Birthday", "Phone", "Address1", "Address2", "City", "Email", "Gender", "Availability","Camp_id"]

    entry_vars = []

    for i, field in enumerate(fields):
        Label(add_window, text=f"{field}: ",bg=bg_color,fg="white",font=("Calibri", 14)).grid(row=i, column=0, padx=10, pady=5)
        entry_var = StringVar()
        Entry(add_window, textvariable=entry_var).grid(row=i, column=1, padx=10, pady=5)
        entry_vars.append(entry_var)
    back_button = Button(add_window, text="Back", command=add_window.destroy)
    back_button.grid(row=len(fields) + 1, column=0, columnspan=2, pady=10)
    submit_button = Button(add_window, text="Add Volunteer", command=lambda: create_account(entry_vars, add_window))
    submit_button.grid(row=len(fields), column=0, columnspan=2, pady=10)

def create_account(entry_vars, add_window):
    fields = ["username", "user_password", "first_name", "last_name", "birthday", "phone", "address1", "address2", "city",
               "email", "gender",  "availability","camp_id"]
    default_values = {"active": "True", "acc_type": "volunteer"}

    # Get the user-entered values
    user_values = {fields[i]: entry_var.get() for i, entry_var in enumerate(entry_vars)}

    # Update the dictionary with default values for missing keys
    new_volunteer_info = {**default_values, **user_values}

    add_volunteer(**new_volunteer_info)
    user_df.to_csv('volunteers_file.csv', index=False)

    success_label = Label(add_window,text=f"Volunteer {new_volunteer_info['first_name']} {new_volunteer_info['last_name']} added successfully.",fg="green",bg=bg_color,font=("Calibri", 12))
    success_label.grid(row=len(fields) + 2, column=0, columnspan=2, pady=10)
    add_window.after(3000, lambda: success_label.destroy())

def display_information():
    # Implement the functionality for displaying information here
    display_user_row(user_index, user_df)

def quit_application():
    # Implement the functionality for quitting the application here
    root.destroy()

def main_application():
    main_window = Toplevel(root)
    main_window.title('Volunteer Management System')
    # Set the window size
    main_window_width = 350
    main_window_height = 300
    main_window['bg'] = '#021631'
    # Get screen width and height
    screen_width = main_window.winfo_screenwidth()
    screen_height = main_window.winfo_screenheight()

    # Calculate the position to center the window
    x_position = (screen_width - main_window_width) // 2
    y_position = (screen_height - main_window_height) // 2
    # Set the window geometry
    main_window.geometry(f"{main_window_width}x{main_window_height}+{x_position}+{y_position}")

    # Add widgets and functionality for the main application
    display_button = Button(main_window, text="Display Information", command=display_information, font=("Calibri", 12))
    display_button.pack(pady=10)

    update_button = Button(main_window, text="Update Information", command=updating, font=("Calibri", 12))
    update_button.pack(pady=10)

    refugee_portal_button = Button(main_window, text="Refugee Portal", command=open_refugee_portal,font=("Calibri", 12))
    refugee_portal_button.pack(pady=10)

    edit_camp_button = Button(main_window, text="Edit Camp", command=edit_camp, font=("Calibri", 12))
    edit_camp_button.pack(pady=10)

    quit_button = Button(main_window, text="Quit", command=quit_application, font=("Calibri", 12))
    quit_button.pack(pady=10)

def open_refugee_portal():
    from create_refugee import MainMenuWindow
    refugee_portal_window = Toplevel(root)
    refugee_portal_window = MainMenuWindow(refugee_portal_window)

def edit_camp():
    from edit_camp_frame import EditCampFrame
    from edit_camp_frame import  main
    main()

def add_volunteer(username, user_password, first_name, last_name,birthday, phone, address1, address2, city,acc_type,email,gender,active,availability,camp_id):
    global user_df
    new_user_id = user_df['user_id'].max() + 1
    new_volunteer = pd.DataFrame({
        "user_id": [new_user_id],
        "username": [username],
        "user_password": [user_password],
        "first_name": [first_name],
        "last_name": [last_name],
        'dob':[birthday],
        "contact_number": [int(phone)],  # Convert phone number to integer
        "address1": [address1],
        "address2": [address2],
        "city": [city],
        "acc_type":[acc_type],
        "user_email": [email],
        'gender':[gender],
        'active':[active],
        'availability':[availability],
        'camp_id': [int(camp_id)],
    })
    user_df = pd.concat([user_df, new_volunteer], ignore_index=True)


def display_user_row(user_index, user_df):

    user_row = user_df.loc[[user_index]]
    # print("\nUser Information:")
    # print(user_row.to_string(index=False))
    display_window = Toplevel(root)
    display_window.title("User Information")
    display_window['bg'] = '#021631'
    # Set window size
    window_width = 400
    window_height = 420

    # Get screen width and height
    screen_width = display_window.winfo_screenwidth()
    screen_height = display_window.winfo_screenheight()

    # Calculate the position to center the window
    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2

    # Set the window geometry
    display_window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

    # Create a Treeview widget
    tree = ttk.Treeview(display_window, columns=("Property", "Value"))

    # Insert data into the treeview
    for col, value in user_row.items():
        tree.insert("", "end", values=(col, value.values[0]))

    # Format columns
    tree.column("#0", width=0, stretch="no")  # Hidden column
    tree.column("Property", anchor="w", width=150)
    tree.column("Value", anchor="w", width=150)

    # Set column headings
    tree.heading("#0", text="", anchor="w")
    tree.heading("Property", text="Property", anchor="w")
    tree.heading("Value", text="Value", anchor="w")

    # Pack the Treeview with an increased height
    tree.pack(pady=10,expand=True, fill="y")

    # Add a close button to close the display window
    close_button = Button(display_window, text="Back", command=display_window.destroy)
    close_button.pack(pady=10)


root = Tk()
root.title('Volunteer Login')
root['bg'] = '#021631'
# Set window size
window_width = 300
window_height = 200

# Get screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculate the position to center the window
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2

# Set the window geometryy
root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")



Label(root, text="Username: ",bg=bg_color,fg="white",font=("Calibri", 14)).place(x=20, y=20)
Label(root, text="Password: ",bg=bg_color,fg="white",font=("Calibri", 14)).place(x=20, y=70)

global enrey1
global enrey2

enrey1 = Entry(root, bd=5)
enrey1.place(x=140, y=20)

enrey2 = Entry(root, bd=5, show='*')
enrey2.place(x=140, y=70)



# Button(root, text="Login", command=login, height=2, width=13, bd=6).place(x=100, y=120)
log_button = Button(root, text="Login", command=login)
log_button.place(x=130, y=110)

add_button = Button(root, text="Create Account", command=create_account_window)

add_button.place(x=100, y=150)

root.mainloop()