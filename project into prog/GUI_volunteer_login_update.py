import tkinter as tk
from tkinter import *
from tkinter import messagebox
import pandas as pd
from tkinter import ttk
from display_camp_resources_frame import DisplayAllocatedResourcesFrame
import re
from datetime import datetime
user_df = pd.read_csv('volunteers_file.csv')
csv_filename = 'Refugee_DataFrame.csv'
refugee_df = pd.read_csv(csv_filename)
bg_color = '#021631'

country_list = ["Afghanistan", "Albania", "Algeria", "Andorra", "Angola",
                "Antigua and Barbuda", "Argentina", "Armenia", "Australia",
                "Austria", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh",
                "Barbados", "Belarus", "Belgium", "Belize", "Benin",
                "Bhutan", "Bolivia", "Bosnia and Herzegovina", "Botswana",
                "Brazil", "Brunei", "Bulgaria", "Burkina Faso", "Burundi",
                "Cabo Verde", "Cambodia", "Cameroon", "Canada",
                "Central African Republic", "Chad", "Chile", "China",
                "Colombia", "Comoros", "Congo, Democratic Republic of the",
                "Congo, Republic of the", "Costa Rica", "Cote d'Ivoire",
                "Croatia", "Cuba", "Cyprus", "Czechia", "Denmark", "Djibouti",
                "Dominica", "Dominican Republic", "Ecuador", "Egypt",
                "El Salvador", "Equatorial Guinea", "Eritrea", "Estonia",
                "Eswatini", "Ethiopia", "Fiji", "Finland", "France",
                "Gabon", "Gambia", "Georgia", "Germany", "Ghana", "Greece",
                "Grenada", "Guatemala", "Guinea", "Guinea-Bissau", "Guyana",
                "Haiti", "Honduras", "Hungary", "Iceland", "India",
                "Indonesia", "Iran", "Iraq", "Ireland", "Israel", "Italy",
                "Jamaica", "Japan", "Jordan", "Kazakhstan", "Kenya",
                "Kiribati", "Korea, North", "Korea, South", "Kosovo",
                "Kuwait", "Kyrgyzstan", "Laos", "Latvia", "Lebanon",
                "Lesotho", "Liberia", "Libya", "Liechtenstein", "Lithuania",
                "Luxembourg", "Madagascar", "Malawi", "Malaysia", "Maldives",
                "Mali", "Malta", "Marshall Islands", "Mauritania", "Mauritius",
                "Mexico", "Micronesia", "Moldova", "Monaco", "Mongolia",
                "Montenegro", "Morocco", "Mozambique", "Myanmar", "Namibia",
                "Nauru", "Nepal", "Netherlands", "New Zealand", "Nicaragua",
                "Niger", "Nigeria", "North Macedonia", "Norway", "Oman",
                "Pakistan", "Palau", "Palestine State", "Panama",
                "Papua New Guinea", "Paraguay", "Peru", "Philippines",
                "Poland", "Portugal", "Qatar", "Romania", "Russia", "Rwanda",
                "Saint Kitts and Nevis", "Saint Lucia", "Saint Vincent and the Grenadines",
                "Samoa", "San Marino", "Sao Tome and Principe", "Saudi Arabia",
                "Senegal", "Serbia", "Seychelles", "Sierra Leone", "Singapore",
                "Slovakia", "Slovenia", "Solomon Islands", "Somalia",
                "South Africa", "South Sudan", "Spain", "Sri Lanka", "Sudan",
                "Suriname", "Sweden", "Switzerland", "Syria", "Taiwan",
                "Tajikistan", "Tanzania", "Thailand", "Timor-Leste", "Togo",
                "Tonga", "Trinidad and Tobago", "Tunisia", "Turkey", "Turkmenistan",
                "Tuvalu", "Uganda", "Ukraine", "United Arab Emirates",
                "United Kingdom", "United States", "Uruguay", "Uzbekistan",
                "Vanuatu", "Vatican City", "Venezuela", "Vietnam",
                "Yemen", "Zambia", "Zimbabwe"]

def login(display_messages=True):
    global user_index, user
    username = enrey1.get()
    password = enrey2.get()  # Keep password as a string

    # try:
    #     password = int(password)
    # except ValueError:
    #     messagebox.showinfo("", "Invalid password.")
    #     return None

    user_df = pd.read_csv('volunteers_file.csv')
    user = user_df[user_df['username'] == username]

    if not user.empty:
        # Check if password matches (as string comparison)
        if str(user['user_password'].iloc[0]) == password and not pd.isnull(user['camp_id'].iloc[0]):
            user_index = user.index[0]
            volunteer_camp_id = user_df.loc[user_index, 'camp_id']
            print("user_index:", user_index)
            print(volunteer_camp_id)
            # Check if account is active
            if user['active'].iloc[0] == False:
                if display_messages:
                    messagebox.showinfo("Warning", "Hey! Your account is not active. Please contact the administrator.")
                return False, None
            else:
                if display_messages:
                    messagebox.showinfo("", f"Access granted, {username}!")
                    root.withdraw()  # Hide the login window
                    main_application()  # Call the main application window
                return True, username
        else:
            if str(user['user_password'].iloc[0]) == password:
                user_index = user.index[0]
                if user['active'].iloc[0] == False:
                    if display_messages:
                        messagebox.showinfo("Warning",
                                            "Hey! Your account is not active. Please contact the administrator.")
                    return False, None
                elif pd.isnull(user['camp_id'].iloc[0]):
                    if display_messages:
                        messagebox.showinfo("Warning", "Hey! Please choose a camp firstly!")
                        updating()
                    return False, None
                    # else:
                    #     messagebox.showinfo("Warning", "The password you have entered is wrong!")
            else:
                    messagebox.showinfo("Warning", "The password you have entered is wrong!")
    else:
        messagebox.showinfo("Warning", "The user account does not exist!")
        user_index = None
    print(type(user['user_password'].iloc[0]))
    print(type(password))

import pandas as pd

def update_camp_volunteer_numbers():
    global user_df
    try:
        user_df = pd.read_csv('volunteers_file.csv', dtype={'camp_id': 'Int64'})
        camps_df = pd.read_csv("camps.csv")

        volunteer_counts = user_df['camp_id'].value_counts()

        for camp_id, count in volunteer_counts.items():
            camps_df.loc[camps_df['camp_id'] == camp_id, 'volunteers_number'] = count

        camps_df['volunteers_number'] = camps_df['camp_id'].apply(lambda x: volunteer_counts.get(x, 0))

        camps_df.to_csv("camps.csv", index=False)

    except pd.errors.ParserError as e:
        print(f"Error reading camps.csv: {e}")

    except Exception as e:
        print(f"An error occurred: {e}")

def updating():
    global user_df, user_index
    if pd.isnull(user['camp_id'].iloc[0]):
        valid_fields = ["camp_id"]
    else:
        valid_fields = ["first_name","last_name","dob","gender","contact_number", "address1", "address2", "country", "user_email", "camp_id"]
    had_no_camp_id = pd.isnull(user['camp_id'].iloc[0])
    def update_info():
        field_to_update = field_var.get()
        new_value = entry_value.get()

        if field_to_update in valid_fields:
            try:
                if not new_value:
                    raise ValueError(f"Field {field_to_update} cannot be empty.")

                if field_to_update == "contact_number":
                    try:
                        new_value = int(new_value)
                    except ValueError:
                        raise ValueError("Invalid contact number. Please enter a numeric value.")
                # if not str(new_value).isdigit():
                #     raise ValueError("Invalid contact number. Please enter a numeric value.")

                elif field_to_update == "dob":
                    try:
                        new_value = pd.to_datetime(new_value, format='%Y-%m-%d', errors='raise')
                    except ValueError as e:
                        raise ValueError("Invalid birthday format. Please use YYYY-MM-DD format.") from e
                    # Check if the birthday is later than the current date
                    if new_value > pd.to_datetime(datetime.now().strftime('%Y-%m-%d')):
                        raise ValueError("Invalid birthday. Birthdate cannot be in the future.")

                elif field_to_update == "user_email":
                    if not re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', new_value):
                        raise ValueError("Invalid email address. Please enter a valid email.")


                elif field_to_update == "camp_id":

                    try:

                        new_camp_id = int(new_value)

                        camp_ids = set(pd.read_csv('camps.csv')['camp_id'])

                        # Check if the new camp_id exists

                        if new_camp_id in camp_ids:

                            old_camp_id = int(user_df.loc[user_index, 'camp_id']) if pd.notna(
                                user_df.loc[user_index, 'camp_id']) else None

                            user_id = user_df.loc[user_index, 'user_id']

                            first_namee = user_df.loc[user_index, 'first_name']

                            last_namee = user_df.loc[user_index, 'last_name']

                            # Call the method to send camp id update

                            from liveupdatevolunteer import send_camp_id_update

                            send_camp_id_update(user_id, first_namee, last_namee, old_camp_id, new_camp_id)

                        else:

                            raise ValueError("Error: The entered camp_id does not exist.")


                    except ValueError:

                        result_label.config(text="Invalid camp_id. Please enter a valid integer.", fg="red")

                        return



                elif field_to_update in ["first_name", "last_name"]:
                    if not new_value.isalpha():
                        raise ValueError(f"{field_to_update.replace('_', ' ').title()} must only contain letters.")

                elif field_to_update == "gender" and new_value.lower() not in ["male", "female", "other"]:
                    raise ValueError("Gender must be 'male', 'female', or 'other'.")
                elif field_to_update == "country":
                    valid_countries = set(country_list)  # Replace with your actual list of valid countries
                    if new_value.capitalize() not in valid_countries:
                        raise ValueError("Invalid country. Please select a valid country.")
            except ValueError as e:
                result_label.config(text=str(e), fg="red", font=("Calibri", 12))
                return

            user_df.loc[user_index, field_to_update] = new_value
            result_label.config(text=f"{field_to_update} updated successfully.", fg="green",font=("Calibri", 12))
            user_df.to_csv('volunteers_file.csv', index=False)

            if field_to_update == "camp_id":
                update_camp_volunteer_numbers()

            # If the update is successful, and the volunteer had no camp_id before, show the 'Redirect to Main' button
            if had_no_camp_id:
                redirect_button.pack(pady=10)
        else:
            result_label.config(text=f"Invalid field to update. Valid fields are:\n {valid_fields}", fg="red",font=("Calibri", 12))
            redirect_button.pack_forget()


    def back_to_main():
        update_window.destroy()

    def redirect_to_main():
        global user, valid_fields

        # Set the value of pd.isnull(user['camp_id'].iloc[0]) to False
        user['camp_id'].iloc[0] = 'some_non_null_value'


        update_window.destroy()
        main_application()
    global update_window
    # Create the update window
    update_window = Toplevel(root)
    update_window.title("Update Information")
    update_window['bg'] = '#021631'
    # Set window size
    window_width = 700
    window_height = 800



    # Get screen width and height
    screen_width = update_window.winfo_screenwidth()
    screen_height = update_window.winfo_screenheight()

    # Calculate the position to center the window
    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2

    # Set the window geometry
    update_window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
    Label(update_window, text="When you switch a camp by updating your camp_id, a live update will be sent to admin",
          bg=bg_color, fg="white", font=("Calibri", 12)).pack(pady=(180,10))
    Label(update_window, text="Select field to update: ",bg=bg_color,fg="white",font=("Calibri", 14)).pack(pady=(10,10))
    field_var = ttk.Combobox(update_window, values=valid_fields)
    field_var.pack(pady=10)
    field_var.set("Choose a field")

    Label(update_window, text="Enter new value: ",bg=bg_color,fg="white",font=("Calibri", 14)).pack(pady=10)
    entry_value = Entry(update_window)
    entry_value.pack(pady=10)


    # Button(update_window, text="Update", command=update_info).pack(pady=10)
    update_button = Button(update_window, text="Update", command=update_info,
                           font=("Calibri", 10),
                           width=15,
                           height=0,
                           bg="#FFFFFF",
                           fg="black",
                           cursor="hand2",
                           activebackground="#B8B8B8",
                           activeforeground="black", )
    update_button.pack(pady=10)
    display_camp_button = Button(update_window, text="Display all camps",
                                 command=lambda: display_all_camps(update_window),
                                 font=("Calibri", 10),
                                 width=15,
                                 height=0,
                                 bg="#FFFFFF",
                                 fg="black",
                                 cursor="hand2",
                                 activebackground="#B8B8B8",
                                 activeforeground="black", )
    display_camp_button.pack(pady=10)
    if pd.isnull(user['camp_id'].iloc[0]):

        # Add the redirect_button only when the condition is true
        redirect_button = Button(update_window, text="Redirect to Main", command=redirect_to_main,
                                 font=("Calibri", 10),
                                 width=15,
                                 height=0,
                                 bg="#FFFFFF",
                                 fg="black",
                                 cursor="hand2",
                                 activebackground="#B8B8B8",
                                 activeforeground="black", )


    else:


        # Add the back_button when the condition is false
        back_button = Button(update_window, text="Back", command=back_to_main,
                             font=("Calibri", 10),
                             width=10,
                             height=0,
                             bg="#FFFFFF",
                             fg="black",
                             cursor="hand2",
                             activebackground="#B8B8B8",
                             activeforeground="black", )
        back_button.pack(pady=10)


    # redirect_button = Button(update_window, text="Redirect to Main", command=redirect_to_main)
    # redirect_button.pack(pady=10)

    result_label = Label(update_window,bg='#021631')
    result_label.pack(pady=10)
    # Add functionality to simulate "Enter" key press
    def on_enter(event):
        update_info()

    update_window.bind("<Return>", on_enter)
def display_all_camps(update_window):
    df = pd.read_csv('plan.csv')

    new_window=tk.Toplevel(update_window)
    new_window.title('Camps Table')

    #create treeview to display table
    tree=ttk.Treeview(new_window, columns=('Plan Name','Country','Number of Camps','Camp ID'), show='headings')
    tree.heading('Plan Name',text='Plan Name')
    tree.heading('Country', text='Country')
    tree.heading('Number of Camps', text='Number of Camps')
    tree.heading('Camp ID', text='Camp ID')

    for i, row in df.iterrows():
        plan_name= row['planName']
        country= row['geographicalArea']
        no_camps = row['NumberOfCamps']
        campid= row['camp_id']
        tree.insert(parent='',index=0, values=(plan_name,country,no_camps,campid))

    #adding scrollbar
    scrollbar= ttk.Scrollbar(new_window, orient='vertical', command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side='right', fill='y')

    tree.pack(expand=True, fill='both')

def create_account_window():

    add_window = Toplevel(root)
    add_window.title('Create Account')
    window_width = 700
    window_height = 800
    add_window['bg'] = '#021631'

    screen_width = add_window.winfo_screenwidth()
    screen_height = add_window.winfo_screenheight()

    x_position = (screen_width - 600) // 2
    y_position = (screen_height - 850) // 2

    add_window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
    fields = ["username", "user_password", "first_name", "last_name", "birthday", "phone", "address1", "address2",
              "country", "email", "gender"]
    entry_vars = {}


    for i, field in enumerate(fields):
        label_text = field.replace('_', ' ').title()
        Label(add_window, text=f"{label_text}: ", bg=bg_color, fg="white", font=("Calibri", 14)).place(x=200,
                                                                                                       y=125 + i * 30)

        if field == "country":
            country_var = StringVar(add_window)
            country_dropdown = ttk.Combobox(add_window, textvariable=country_var, values=country_list,width=17,)
            country_dropdown.place(x=340, y=130 + i * 30)
            entry_vars[field] = country_var
        else:
            entry_var = StringVar(add_window)
            Entry(add_window, textvariable=entry_var).place(x=340, y=130 + i * 30)
            entry_vars[field] = entry_var

    back_button = Button(add_window, text="Back", command=add_window.destroy, font=("Calibri", 12), width=16, height=0, bg="#FFFFFF", fg="black", cursor="hand2", activebackground="#B8B8B8", activeforeground="black")
    back_button.place(x=280, y=600)

    submit_button = Button(add_window, text="Create Account", command=lambda: create_account(entry_vars, add_window), font=("Calibri", 12), width=16, height=0, bg="#FFFFFF", fg="black", cursor="hand2", activebackground="#B8B8B8", activeforeground="black")
    submit_button.place(x=280, y=650)


def create_account(entry_vars, add_window):
    fields = ["username", "user_password", "first_name", "last_name", "birthday", "phone", "address1", "address2", "country", "email", "gender",]
    default_values = {"active": True, "acc_type": "volunteer"}
    existing_usernames = pd.read_csv('volunteers_file.csv')['username'].tolist()
    # Get the user-entered values. Using the field names directly from the fields list
    user_values = {field: entry_vars[field].get() for field in fields}
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    # Debugging: Print user_values to check inputs
    print("User Values:", user_values)
    # Validation check
    for key, value in user_values.items():
        if not value:
            messagebox.showerror("Error", f"Field {key} cannot be empty.")
            return
        elif key == "username":
            if not value.startswith("volunteer") or not value[len("volunteer"):].isdigit():
                messagebox.showerror("Error", "Username must start with 'volunteer' followed by a number.")
                return
            if value in existing_usernames:
                messagebox.showerror("Error", "This username already exists. Please choose a different username.")
                return
        elif key == "user_password":
            try:
                int(value)  # Check if the password is an integer
            except ValueError:
                messagebox.showerror("Error", "User password must be an integer.")
                return
        elif key in ["first_name", "last_name"]:
            if not value.isalpha():
                messagebox.showerror("Error", f"{key.replace('_', ' ').title()} must only contain letters.")
                return

        elif key == "birthday":
            try:
                value = pd.to_datetime(value, format='%Y-%m-%d', errors='raise')
            except ValueError:
                messagebox.showerror("Error", "Invalid birthday format. Please use YYYY-MM-DD format.")
                return
            # Check if the birthday is later than the current date
            if value > pd.to_datetime(datetime.now().strftime('%Y-%m-%d')):
                messagebox.showerror("Error", "Invalid birthday. Birthdate cannot be in the future.")
                return

        elif key == "phone":
            try:
                int(value)  # Check if the phone number is an integer
            except ValueError:
                messagebox.showerror("Error", "Phone must be a number.")
                return
        elif key == "email" and not re.fullmatch(regex, value):
            messagebox.showerror("Error", "Invalid email format.")
            return
        elif key == "gender" and value.lower() not in ["male", "female", "other"]:
            messagebox.showerror("Error", "Gender must be 'male', 'female', or 'other'.")
            return

    # Update the dictionary with default values for missing keys
    new_volunteer_info = {**default_values, **user_values}

    # Add the new volunteer
    add_volunteer(**new_volunteer_info)

    # Display success message
    messagebox.showinfo("Success", f"Volunteer {new_volunteer_info['first_name']} {new_volunteer_info['last_name']} added successfully.")

    # Optionally, refresh or close the add_window if necessary

def display_information():
    # Implement the functionality for displaying information here
    display_user_row(user_index, user_df)

def quit_application():
    # Implement the functionality for quitting the application here
    root.destroy()

def main_application():
    global main_window
    main_window = Toplevel(root)
    main_window.title('Volunteer Management System')
    # Set the window size
    main_window_width = 700
    main_window_height = 800
    main_window['bg'] = '#021631'
    # Get screen width and height
    screen_width = main_window.winfo_screenwidth()
    screen_height = main_window.winfo_screenheight()

    # Calculate the position to center the window
    x_position = (screen_width - main_window_width) // 2
    y_position = (screen_height - main_window_height) // 2
    # Set the window geometry
    main_window.geometry(f"{main_window_width}x{main_window_height}+{x_position}+{y_position}")
    welcome_label = Label(main_window, text="Welcome volunteer! What do you want to do for today?",
                          bg=bg_color,
                          fg="white",
                          font=("Calibri", 14))
    welcome_label.pack(pady=(150, 10), side='top', anchor='center')
    # Add widgets and functionality for the main application
    display_button = Button(main_window, text="Account Information", command=display_information,
        font=("Calibri", 11),
        width=22,
        height=0,
        bg="#FFFFFF",
        fg="black",
        cursor="hand2",
        activebackground="#B8B8B8",
        activeforeground="black",)
    display_button.pack(pady=( 10), side='top', anchor='center')


    update_button = Button(main_window, text="Update Information", command=updating, font=("Calibri", 11),
        width=22,
        height=0,
        bg="#FFFFFF",
        fg="black",
        cursor="hand2",
        activebackground="#B8B8B8",
        activeforeground="black",)
    update_button.pack(pady=10, side='top', anchor='center')

    refugee_portal_button = Button(main_window, text="Refugee Portal", command=open_refugee_portal,
        font=("Calibri", 11),
        width=22,
        height=0,
        bg="#FFFFFF",
        fg="black",
        cursor="hand2",
        activebackground="#B8B8B8",
        activeforeground="black",)
    refugee_portal_button.pack(pady=10, side='top', anchor='center')

    def open_display_camp_resources_frame():
        volunteer_camp_id = user_df.loc[user_index, 'camp_id'] if user_index is not None else None
        display_camp_resources_window = tk.Toplevel(root)
        display_camp_resources_window.title("Camp Resources")
        display_camp_resources_frame = DisplayCampResourcesFrame(display_camp_resources_window, volunteer_camp_id)
        display_camp_resources_frame.pack(expand=True, fill='both')

    display_allocated_resources_button = Button(main_window, text="Display Allocated Resources",
                                                command=open_display_allocated_resources_frame,
                                                font=("Calibri", 11),
                                                width=22,
                                                height=0,
                                                bg="#FFFFFF",
                                                fg="black",
                                                cursor="hand2",
                                                activebackground="#B8B8B8",
                                                activeforeground="black")
    display_allocated_resources_button.pack(pady=10, side='top', anchor='center')

    edit_camp_button = Button(main_window, text="Edit Camp", command=edit_camp,
        font=("Calibri", 11),
        width=22,
        height=0,
        bg="#FFFFFF",
        fg="black",
        cursor="hand2",
        activebackground="#B8B8B8",
        activeforeground="black",)
    edit_camp_button.pack(pady=10, side='top', anchor='center')

    live_update_button = Button(main_window, text="Send Live Updates", command=open_live_updates,
                              font=("Calibri", 11),
                              width=22,
                              height=0,
                              bg="#FFFFFF",
                              fg="black",
                              cursor="hand2",
                              activebackground="#B8B8B8",
                              activeforeground="black", )
    live_update_button.pack(pady=10, side='top', anchor='center')


    quit_button = Button(main_window, text="Quit", command=quit_application,
        font=("Calibri", 11),
        width=22,
        height=0,
        bg="#FFFFFF",
        fg="black",
        cursor="hand2",
        activebackground="#B8B8B8",
        activeforeground="black",)
    quit_button.pack(pady=10, side='top', anchor='center')
def open_refugee_portal():
    # global user_index, user_df, user
    # import refugee_portal_volunteer
    from Refugee_portal_volunteer_test import RefugeePortalVolunteerApp
    # Check if the main_menu_window already exists
    # if main_menu_window is not None:
    #     try:
    #         main_menu_window.master.destroy()  # Attempt to destroy the existing window
    #     except AttributeError:
    #         pass  # Handle the case where destroy method doesn't exist

    volunteer_camp_id = user_df.loc[user_index, 'camp_id']
    volunteer_volunteer_id = user_df.loc[user_index, 'user_id']
    # portal_window = tk.Toplevel(root)
    # portal_window.geometry("1400x700")
    # main_menu_window = MainMenuWindow(portal_window)
    # main_menu_window.set_camp_id(volunteer_camp_id)
    # Create a new instance of Tk for the main application window
    # root = tk.Toplevel()
    # # Create a new Toplevel window
    portal_window = tk.Toplevel(root)
    #
    # Set the desired window size
    portal_window.geometry("1400x700")  # Adjust the size as needed
    #
    main_menu_window = RefugeePortalVolunteerApp(portal_window, camp_id=volunteer_camp_id, volunteer_id=volunteer_volunteer_id)


    # def open_refugee_portal():
    # # Create an instance of MainMenuWindow when the button is clicked
    # from create_refugee import MainMenuWindow
    # refugee_portal_window = Toplevel(root)
    # # refugee_portal_window.title("Refugee Portal")
    # # Pass user_df to the MainMenuWindow constructor
    # refugee_portal_window = MainMenuWindow(refugee_portal_window)

def edit_camp():
    from manage_camps_frame import ManageCampsFrame

    # Extract the camp_id of the logged-in volunteer
    volunteer_camp_id = user_df.loc[user_index, 'camp_id'] if user_index is not None else None

    # Create a new Toplevel window
    manage_camp_window = tk.Toplevel(root)

    # Set the desired window size
    manage_camp_window.geometry("1400x700")  # Adjust the size as needed

    # Define the callback for the "Back" button
    def on_back():
        manage_camp_window.destroy()

    # Pass the volunteer's camp_id to the ManageCampsFrame
    manage_camp_app = ManageCampsFrame(manage_camp_window, on_back=on_back, camp_id=volunteer_camp_id)
def open_display_allocated_resources_frame():
    print("Opening Display Allocated Resources Frame")
    display_resources_window = tk.Toplevel(root)
    display_resources_window.title("Allocated Resources")
    volunteer_id = user_df.loc[user_index, 'user_id'] if user_index is not None else None
    print(f"Volunteer ID: {volunteer_id}")
    display_resources_frame = DisplayAllocatedResourcesFrame(display_resources_window, volunteer_id=volunteer_id)
    display_resources_frame.pack(expand=True, fill='both')


def open_live_updates():
    # from liveupdatevolunteer import submit_update
    # submit_update()
    # main_window.destroy()
    # import liveupdatevolunteer
    main_window.destroy()
    from liveupdatevolunteer import main_live_updates
    main_live_updates()

def add_volunteer(username, user_password, first_name, last_name, birthday, phone, address1, address2, country, acc_type, email, gender, active,):
    global user_df
    # Ensure user_df is loaded
    user_df = pd.read_csv('volunteers_file.csv')

    # Generate a new user ID
    new_user_id = user_df['user_id'].max() + 1

    # Create the new volunteer DataFrame
    new_volunteer = pd.DataFrame({
        "user_id": [new_user_id],
        "username": [username],
        "user_password": [user_password],
        "first_name": [first_name],
        "last_name": [last_name],
        'dob': [birthday],
        "contact_number": [phone],
        "address1": [address1],
        "address2": [address2],
        "country": [country],
        "acc_type": [acc_type],
        "user_email": [email],
        'gender': [gender],
        'active': [active],


    })

    # Concatenate the new volunteer data to the existing DataFrame
    user_df = pd.concat([user_df, new_volunteer], ignore_index=True)

    # Save the updated DataFrame back to CSV
    user_df.to_csv('volunteers_file.csv', index=False)

def display_user_row(user_index, user_df):
    user_row = user_df.loc[[user_index]]
    user_row = user_row.fillna('')  # Replace NaNs with empty strings for display
    # print("\nUser Information:")
    # print(user_row.to_string(index=False))
    display_window = Toplevel(root)
    display_window.title("User Information")
    display_window['bg'] = '#021631'
    # Set window size
    window_width = 700
    window_height = 800

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

    # Convert camp_id to an integer for display, handling NaN values
    for col, value in user_row.items():
        if col == 'camp_id':
            if pd.isna(value.iloc[0]):
                display_value = ''  # or some placeholder like 'N/A'
            else:
                display_value = str(int(value.iloc[0]))  # Convert to integer and then to string for display
        else:
            display_value = str(value.iloc[0])

        tree.insert("", "end", values=(col, display_value))

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
    close_button = Button(display_window, text="Back", command=display_window.destroy,
                          font=("Calibri", 12),
                          width=16,
                          height=0,
                          bg="#FFFFFF",
                          fg="black",
                          cursor="hand2",
                          activebackground="#B8B8B8",
                          activeforeground="black", )
    close_button.pack(pady=10)

def back_to_main():
    root.destroy()


root = tk.Toplevel()
root.title('Volunteer Login')
root['bg'] = '#021631'
# Set window size
window_width = 350
window_height = 250

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
log_button = Button(root, text="Log In", command=login,font=("Calibri", 12),
        width=16,
        height=0,
        bg="#FFFFFF",
        fg="black",
        cursor="hand2",
        activebackground="#B8B8B8",
        activeforeground="black")
log_button.place(x=80, y=110)

add_button = Button(root, text="Create Account", command=create_account_window,font=("Calibri", 12),
        width=16,
        height=0,
        bg="#FFFFFF",
        fg="black",
        cursor="hand2",
        activebackground="#B8B8B8",
        activeforeground="black")

add_button.place(x=80, y=150)

back_button = Button(root, text="Back", command=back_to_main,font=("Calibri", 12),
        width=16,
        height=0,
        bg="#FFFFFF",
        fg="black",
        cursor="hand2",
        activebackground="#B8B8B8",
        activeforeground="black")

back_button.place(x=80, y=190)


root.mainloop()
