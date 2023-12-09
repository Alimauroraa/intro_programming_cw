import csv
import tkinter as tk
from tkinter import messagebox
from data_model import Volunteer
import pandas as pd

# Function to load, volunteer accounts from a CSV file
def load_volunteers_from_csv(volunteers_file):
    volunteers = []
    with open(volunteers_file, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            row.pop('emergency_profiles', None)
            volunteer = Volunteer(**row)
            volunteers.append(volunteer)
    return volunteers


# Function to save updated volunteer data to the CSV file
def save_volunteers_to_csv(volunteers_file, volunteers):
    with open(volunteers_file, mode='w', newline='') as csvfile:
        fieldnames = ['user_id', 'username', 'user_password', 'first_name', 'last_name', 'dob', 'user_email',
                      'contact_number', 'address1', 'address2', 'country', 'acc_type',
                      'gender', 'active', 'camp_id']  # Add 'country' here
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for volunteer in volunteers:
            writer.writerow(vars(volunteer))

# # Create the main window
# root = tk.Tk()
# root.title("Edit Volunteer")
# root.geometry("700x800")
# root['bg'] = '#021631'
#
# main_window = root
# main_window.title('Volunteer Management System')
# # Set the window size
# main_window_width = 800
# main_window_height = 800
#
#     # Get screen width and height
# screen_width = main_window.winfo_screenwidth()
# screen_height = main_window.winfo_screenheight()
#
# screen_width = main_window.winfo_screenwidth()
# screen_height = main_window.winfo_screenheight()
#
#     # Calculate the position to center the window
# x_position = (screen_width - main_window_width) // 2
# y_position = (screen_height - main_window_height) // 2
#
#     # Set the window geometry
# main_window.geometry(f"{main_window_width}x{main_window_height}+{x_position}+{y_position}")
#
# # Create a mapping from field names to labels
# field_labels = {
#     'user_id': 'User ID',
#     'username': 'Username',
#     'user_password': 'User Password',
#     'first_name': 'First Name',
#     'last_name': 'Last Name',
#     'dob': 'Date of Birth',
#     'user_email': 'User Email',
#     'contact_number': 'Contact Number',
#     'address1': 'Address 1',
#     'address2': 'Address 2',
#     'city': 'City',
#     'acc_type': 'Account Type',
#     'availability': 'Availability',
#     'gender': 'Gender',
#     'active': 'Active',
#     'camp_id': 'Camp ID',
#     'emergency_profiles': 'Emergency Profiles'
# }
#
# # Create form fields
# entries = {field: tk.Entry(root, bd=2, font="calibri 10") for field in field_labels.keys()}
#
# # Arrange the form fields in a grid
# for i, field in enumerate(field_labels.keys()):
#     tk.Label(root, text=field_labels[field], font="calibri 16", bg="#021631", fg="#fff").grid(row=i, pady=10)  # Add vertical padding
#     entries[field].grid(row=i, column=1, pady=10)  # Add vertical padding

# # Create form fields
# fields = ['user_id', 'username', 'user_password', 'first_name', 'last_name', 'dob', 'user_email',
#               'contact_number', 'address1', 'address2', 'city', 'acc_type', 'availability', 'gender', 'active',
#               'camp_id', 'emergency_profiles']
# entries = {field: tk.Entry(root, bd=2, font="calibri 10") for field in fields}

# # Arrange the form fields in a grid
# for i, field in enumerate(fields):
#     tk.Label(root, text=field, font="calibri 16", bg="#021631", fg="#fff").grid(row=i, pady=10)  # Add vertical padding
# #     entries[field].grid(row=i, column=1, pady=10)  # Add vertical padding
#
# # Create a listbox for displaying volunteers
# volunteers_listbox = tk.Listbox(root)
# volunteers_listbox.grid(row=0, column=2, rowspan=len(field), padx=20)
#
# # Load volunteers from the CSV file
# volunteers = load_volunteers_from_csv('volunteers_file.csv')

# Listbox callback function
def update_form(Event):
    # Update the form fields with the selected volunteer's data
    selected_index = volunteers_listbox.curselection()[0]
    for field, entry in entries.items():
        entry.delete(0, tk.END)
        entry.insert(0, getattr(volunteers[selected_index], field))

# # Bind the listbox callback function
# volunteers_listbox.bind('<<ListboxSelect>>', update_form)

# Button callback functions
def load_volunteers():
    # Update the listbox with the volunteers' names
    volunteers_listbox.delete(0, tk.END)
    for volunteer in volunteers:
        volunteers_listbox.insert(tk.END, volunteer.first_name)

def save_volunteers():
    # Update the selected volunteer with the form data
    selected_index = volunteers_listbox.curselection()[0]
    print(f"Saving volunteer at index {selected_index}")
    for field, entry in entries.items():
        if field != 'active':
            entry_value = entry.get()
            print(f"Setting attribute {field} to {entry_value}")
            setattr(volunteers[selected_index], field, entry_value)
    # Save the volunteers to the CSV file
    save_volunteers_to_csv('volunteers_file.csv', volunteers)
    messagebox.showinfo("Success", "Volunteer data saved successfully.")

def reactivate_volunteer():
    # Get the selected volunteer
    selected_index = volunteers_listbox.curselection()
    if selected_index:  # Check if a volunteer is selected
        selected_index = selected_index[0]
        # Reactivate the selected volunteer
        volunteers[selected_index].active = 'True'
        # Save the updated volunteers list to the CSV file
        save_volunteers_to_csv('volunteers_file.csv', volunteers)
        # Show a success message
        messagebox.showinfo("Success", "Volunteer reactivated successfully.")
    else:
        # Show an error message if no volunteer is selected
        messagebox.showerror("Error", "No volunteer selected.")

def deactivate_volunteer():
    selected_index = volunteers_listbox.curselection()
    if selected_index:
        selected_index = selected_index[0]
        selected_volunteer = volunteers[selected_index]

        # Load camps data
        camps_df = pd.read_csv("camps.csv")

        # Convert camp_id to integer for comparison
        volunteer_camp_id = int(float(selected_volunteer.camp_id))
        camps_df['camp_id'] = camps_df['camp_id'].astype(int)

        if volunteer_camp_id in camps_df['camp_id'].values:
            camp_row_index = camps_df.index[camps_df['camp_id'] == volunteer_camp_id].tolist()
            if camp_row_index:
                camp_row_index = camp_row_index[0]
                camps_df.at[camp_row_index, 'volunteers_number'] = max(0, camps_df.at[camp_row_index, 'volunteers_number'] - 1)

        # Deactivate the selected volunteer
        selected_volunteer.active = 'False'
        selected_volunteer.camp_id = ''

        # Save changes
        save_volunteers_to_csv('volunteers_file.csv', volunteers)
        camps_df.to_csv("camps.csv", index=False)

        messagebox.showinfo("Success", "Volunteer deactivated successfully.")
    else:
        messagebox.showerror("Error", "No volunteer selected.")

def delete_volunteer():
    selected_index = volunteers_listbox.curselection()
    if selected_index:
        selected_index = selected_index[0]
        selected_volunteer = volunteers[selected_index]

        # Load camps data
        camps_df = pd.read_csv("camps.csv")

        # Convert camp_id to integer for comparison, if it's numeric
        volunteer_camp_id = int(selected_volunteer.camp_id) if selected_volunteer.camp_id.isdigit() else selected_volunteer.camp_id
        camps_df['camp_id'] = camps_df['camp_id'].apply(lambda x: int(x) if str(x).isdigit() else x)

        # Check if the camp_id exists and update the volunteer count
        if volunteer_camp_id in camps_df['camp_id'].values:
            camp_row_index = camps_df.index[camps_df['camp_id'] == volunteer_camp_id].tolist()
            if camp_row_index:
                camp_row_index = camp_row_index[0]
                camps_df.at[camp_row_index, 'volunteers_number'] = max(0, camps_df.at[camp_row_index, 'volunteers_number'] - 1)

        # Delete the selected volunteer
        del volunteers[selected_index]

        # Save changes
        save_volunteers_to_csv('volunteers_file.csv', volunteers)
        camps_df.to_csv("camps.csv", index=False)

        messagebox.showinfo("Success", "Volunteer deleted successfully.")
    else:
        messagebox.showerror("Error", "No volunteer selected.")

def go_back(root):
    # Code to go back to the previous screen
    root.grid_forget()

def edit_volunteer_frame(parent):
    root = tk.Frame(parent, width=700, height=800, bg='#021631')
    tk.Label(root, text="Edit volunteer", font="calibri 16", bg="#021631",fg="#fff").place(x=30,y=30)

    # Create buttons
    load_button = tk.Button(root, text="Load Volunteers", command=load_volunteers, width=16)
    # save_button = tk.Button(root, text="Save Volunteer Data", command=save_volunteers)
    deactivate_button = tk.Button(root, text="Deactivate Volunteer", command=deactivate_volunteer)
    delete_button = tk.Button(root, text="Delete Volunteer", command=delete_volunteer)
    go_back_button = tk.Button(root, text="Back", command=lambda:go_back(root))
    reactivate_button = tk.Button(root, text="Reactivate Volunteer", command=reactivate_volunteer)

    load_button.place(x=30,y=200, width=120)
    # save_button.place(x=200,y=650, width=120)
    deactivate_button.place(x=130,y=690, width=120)
    delete_button.place(x=430,y=690, width=120)
    go_back_button.place(x=280,y=730, width=120)
    reactivate_button.place(x=280,y=690, width=120)

    # Create a mapping from field names to labels
    field_labels = {
        'user_id': 'User ID',
        'username': 'Username',
        'first_name': 'First Name',
        'last_name': 'Last Name',
        'dob': 'Date of Birth',
        'user_email': 'User Email',
        'contact_number': 'Contact Number',
        'address1': 'Address 1',
        'address2': 'Address 2',
        'country': 'Country',  # New field added
        'gender': 'Gender',
        'active': 'Active',
        'camp_id': 'Camp ID',
    }

    #'emergency_profiles': 'Emergency Profiles'
#'user_password': 'User Password',
#'acc_type': 'Account Type',
    global entries
    # Create form fields
    entries = {field: tk.Entry(root, bd=2, font="calibri 10", state='readonly') for field in field_labels.keys()}

    for i, (field, label) in enumerate(field_labels.items()):
        tk.Label(root, text=label, font="calibri 12", bg="#021631", fg="#fff").place(x=200, y=130 + i * 30)
        entries[field] = tk.Entry(root, bd=2, font="calibri 10")
        entries[field].place(x=400, y=130 + i * 30, width=250)

    global volunteers_listbox
    # Create a listbox for displaying volunteers
    volunteers_listbox = tk.Listbox(root)
    #volunteers_listbox.grid(row=0, column=2, rowspan=len(field), padx=20)
    volunteers_listbox.place(x=30,y=250)

    global volunteers
    # Load volunteers from the CSV file
    volunteers = load_volunteers_from_csv('volunteers_file.csv')

    # Function to update form fields with selected volunteer's data
    def update_form(Event):
        selected_index = volunteers_listbox.curselection()
        if selected_index:  # Check if a volunteer is selected
            selected_index = selected_index[0]
            volunteer_data = volunteers[selected_index]
            for field, entry in entries.items():
                if field in vars(volunteer_data):
                    entry.config(state='normal')  # Set state to normal to update the entry
                    entry.delete(0, tk.END)
                    entry.insert(0, getattr(volunteer_data, field))
                    entry.config(state='readonly')
    # Bind the listbox callback function
    volunteers_listbox.bind('<<ListboxSelect>>', update_form)

    return root

