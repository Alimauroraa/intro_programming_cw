import tkinter as tk
from tkinter import *
from tkinter import messagebox
import pandas as pd
from tkinter import ttk
from display_camp_resources_frame import DisplayAllocatedResourcesFrame


user_df = pd.read_csv('volunteers_file.csv')
csv_filename = 'Refugee_DataFrame.csv'
refugee_df = pd.read_csv(csv_filename)
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
            if user['active'].iloc[0] == False:
                messagebox.showinfo("Warning", "Hey! Your account is not active. Please contact the administrator.")
            else:
                messagebox.showinfo("", f"Access granted, {username}!")
                root.withdraw()  # Hide the login window
                main_application()  # Call the main application window
        else:
            user_index = user.index[0]
            if user['active'].iloc[0] == False:
                messagebox.showinfo("Warning", "Hey! Your account is not active. Please contact the administrator.")
            elif pd.isnull(user['camp_id'].iloc[0]):
                messagebox.showinfo("Warning", "Hey! Please choose a camp firstly!")
                updating()
            else:
                messagebox.showinfo("Warning", "The password you have entered is wrong!")
    else:
        messagebox.showinfo("Warning", "The user account does not exist!")
        user_index = None


import pandas as pd

def update_camp_volunteer_numbers():
    global user_df
    try:
        user_df = pd.read_csv('volunteers_file.csv')
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
    valid_fields = ["first_name","last_name","dob","gender","contact_number", "address1", "address2", "city", "user_email", "camp_id"]
    def update_info():
        field_to_update = field_var.get()
        new_value = entry_value.get()

        if field_to_update in valid_fields:
            try:
                if field_to_update == "contact_number":
                    new_value = int(new_value)
                elif field_to_update == "camp_id":
                    new_value = int(new_value)
                    camp_ids = set(pd.read_csv('camps.csv')['camp_id'])
                    if new_value not in camp_ids:
                        result_label.config(text="Error: The entered camp_id does not exist.", fg="red",
                                            font=("Calibri", 12))
                        return
            except ValueError:
                result_label.config(text="Invalid input. Please enter a valid value.", fg="red",font=("Calibri", 12))
                return

            user_df.loc[user_index, field_to_update] = new_value
            result_label.config(text=f"{field_to_update} updated successfully.", fg="green",font=("Calibri", 12))
            user_df.to_csv('volunteers_file.csv', index=False)
        else:
            result_label.config(text=f"Invalid field to update. Valid fields are:\n {valid_fields}", fg="red",font=("Calibri", 12))
        
        if field_to_update == "camp_id":
            update_camp_volunteer_numbers()

    def back_to_main():
        update_window.destroy()

    def redirect_to_main():
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

    Label(update_window, text="Select field to update: ",bg=bg_color,fg="white",font=("Calibri", 14)).pack(pady=(200,10))
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
        redirect_button.pack(pady=10)

        display_camp_button = Button(update_window, text="Display all camps", command=lambda:display_all_camps(update_window),
                                     font=("Calibri", 10),
                                     width=15,
                                     height=0,
                                     bg="#FFFFFF",
                                     fg="black",
                                     cursor="hand2",
                                     activebackground="#B8B8B8",
                                     activeforeground="black", )
        display_camp_button.place(x=40, y=70)
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
    fields = ["Username", "Password", "First Name", "Last Name", "Birthday", "Phone", "Address1", "Address2", "City", "Email", "Gender", "Availability","Camp_id"]

    entry_vars = []

    for i, field in enumerate(fields):
        Label(add_window, text=f"{field}: ",bg=bg_color,fg="white",font=("Calibri", 14)).place(x=220,y=125+i*30)
        entry_var = StringVar()
        Entry(add_window, textvariable=entry_var).place(x=340,y=130+i*30)
        entry_vars.append(entry_var)
    back_button = Button(add_window, text="Back", command=add_window.destroy,
        font=("Calibri", 12),
        width=16,
        height=0,
        bg="#FFFFFF",
        fg="black",
        cursor="hand2",
        activebackground="#B8B8B8",
        activeforeground="black",)
    back_button.place(x=280,y=600)
    submit_button = Button(add_window, text="Create Account", command=lambda: create_account(entry_vars, add_window),
        font=("Calibri", 12),
        width=16,
        height=0,
        bg="#FFFFFF",
        fg="black",
        cursor="hand2",
        activebackground="#B8B8B8",
        activeforeground="black",)
        # submit_button.grid(row=len(fields), column=0, columnspan=2, pady=10)
    submit_button.place(x=280,y=650)

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

    live_update_button = Button(main_window, text="Send Live Updates", command=lambda: live_update(),
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
    import create_refugee
    from create_refugee import MainMenuWindow, main_menu_window
    # Check if the main_menu_window already exists
    if main_menu_window is not None:
        try:
            main_menu_window.master.destroy()  # Attempt to destroy the existing window
        except AttributeError:
            pass  # Handle the case where destroy method doesn't exist

    # Create a new instance of Tk for the main application window
    root = tk.Toplevel()
    main_menu_window = MainMenuWindow(root)

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


def live_update():
    from liveupdatevolunteer import submit_update
    submit_update()
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

root.mainloop()
