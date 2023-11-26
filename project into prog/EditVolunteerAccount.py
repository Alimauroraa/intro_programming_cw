import csv
import tkinter as tk
from tkinter import messagebox
from data_model import Volunteer

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
        writer = csv.writer(csvfile)
        writer.writerow(['user_id', 'username', 'user_password', 'first_name', 'last_name', 'dob', 'user_email', 'contact_number', 'address1', 'address2', 'city', 'acc_type', 'availability', 'gender', 'active', 'camp_id', 'emergency_profiles'])
        for volunteer in volunteers:
            writer.writerow([volunteer.user_id, volunteer.username, volunteer.user_password, volunteer.first_name, volunteer.last_name, volunteer.dob, volunteer.user_email, volunteer.contact_number, volunteer.address1, volunteer.address2, volunteer.city, volunteer.acc_type, volunteer.availability, volunteer.gender, volunteer.active, volunteer.camp_id, volunteer.emergency_profiles])
        # fieldnames = ['user_id', 'username', 'user_password', 'first_name', 'last_name', 'dob', 'user_email',
        #       'contact_number', 'address1', 'address2', 'city', 'acc_type', 'availability', 'gender', 'active',
        #       'camp_id', 'emergency_profiles']
        # writer = csv.DictWriter(cvsfile, fieldnames=fieldnames)
        # writer.writeheader()
        # for volunteer in volunteers:
        #     writer.writerow(vars(volunteer))

# Create the main window
root = tk.Tk()
root.title("Edit Volunteer")
root.geometry("700x800")
root['bg'] = '#021631'

# Create form fields
fields = ['user_id', 'username', 'user_password', 'first_name', 'last_name', 'dob', 'user_email',
              'contact_number', 'address1', 'address2', 'city', 'acc_type', 'availability', 'gender', 'active',
              'camp_id', 'emergency_profiles']
entries = {field: tk.Entry(root, bd=2, font="calibri 10") for field in fields}

# Arrange the form fields in a grid
for i, field in enumerate(fields):
    tk.Label(root, text=field, font="calibri 16", bg="#021631", fg="#fff").grid(row=i, pady=10)  # Add vertical padding
    entries[field].grid(row=i, column=1, pady=10)  # Add vertical padding

# Create a listbox for displaying volunteers
volunteers_listbox = tk.Listbox(root)
volunteers_listbox.grid(row=0, column=2, rowspan=len(fields), padx=20)

# Load volunteers from the CSV file
volunteers = load_volunteers_from_csv('volunteers_file.csv')

# Listbox callback function
def update_form(event):
    # Update the form fields with the selected volunteer's data
    selected_index = volunteers_listbox.curselection()[0]
    for field, entry in entries.items():
        entry.delete(0, tk.END)
        entry.insert(0, getattr(volunteers[selected_index], field))

# Bind the listbox callback function
volunteers_listbox.bind('<<ListboxSelect>>', update_form)

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
        entry_value = entry.get()
        print(f"Setting attribute {field} to {entry_value}")
        setattr(volunteers[selected_index], field, entry_value)
    # Save the volunteers to the CSV file
    save_volunteers_to_csv('volunteers_file.csv', volunteers)
    messagebox.showinfo("Success", "Volunteer data saved successfully.")

def deactivate_volunteer():
    # Get the selected volunteer
    selected_index = volunteers_listbox.curselection()
    if selected_index:  # Check if a volunteer is selected
        selected_index = selected_index[0]
        # Deactivate the selected volunteer
        volunteers[selected_index].active = 'False'
        # Save the updated volunteers list to the CSV file
        save_volunteers_to_csv('volunteers_file.csv', volunteers)
        # Show a success message
        messagebox.showinfo("Success", "Volunteer deactivated successfully.")
    else:
        # Show an error message if no volunteer is selected
        messagebox.showerror("Error", "No volunteer selected.")

def delete_volunteer():
    # Get the selected volunteer
    selected_index = volunteers_listbox.curselection()
    if selected_index:  # Check if a volunteer is selected
        selected_index = selected_index[0]
        # Delete the selected volunteer
        del volunteers[selected_index]
        # Save the updated volunteers list to the CSV file
        save_volunteers_to_csv('volunteers_file.csv', volunteers)
        # Show a success message
        messagebox.showinfo("Success", "Volunteer deleted successfully.")
    else:
        # Show an error message if no volunteer is selected
        messagebox.showerror("Error", "No volunteer selected.")

def go_back():
    # Code to go back to the previous screen
    pass

# Create buttons
load_button = tk.Button(root, text="Load Volunteers", command=load_volunteers)
save_button = tk.Button(root, text="Save Volunteers", command=save_volunteers)
deactivate_button = tk.Button(root, text="Deactivate Volunteer", command=deactivate_volunteer)
delete_button = tk.Button(root, text="Delete Volunteer", command=delete_volunteer)
go_back_button = tk.Button(root, text="Go Back", command=go_back)

# Arrange the buttons in a grid
load_button.grid(row=len(fields), column=0)
save_button.grid(row=len(fields), column=1)
deactivate_button.grid(row=len(fields), column=2)
delete_button.grid(row=len(fields), column=3)
go_back_button.grid(row=len(fields), column=4)

# Run the application
root.mainloop()
