import tkinter as tk
from tkinter import messagebox
from data_model import Admin, Volunteer
# Import your existing functions here

# Create the main window
root = tk.Tk()

# Create form fields
fields = ['user_id', 'username', 'user_password', 'first_name', 'last_name', 'dob', 'user_email',
          'contact_number', 'address1', 'address2', 'city', 'acc_type', 'availability', 'gender', 'active']
entries = {field: tk.Entry(root) for field in fields}

# Arrange the form fields in a grid
for i, field in enumerate(fields):
    tk.Label(root, text=field).grid(row=i)
    entries[field].grid(row=i, column=1)

# Create a listbox for displaying volunteers
volunteers_listbox = tk.Listbox(root)
volunteers_listbox.grid(row=0, column=2, rowspan=len(fields))

# Load volunteers from the CSV file
volunteers = load_volunteers_from_csv('volunteers.csv')

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
    for field, entry in entries.items():
        setattr(volunteers[selected_index], field, entry.get())
    # Save the volunteers to the CSV file
    save_volunteers_to_csv('volunteers.csv', volunteers)
    messagebox.showinfo("Success", "Volunteer data saved successfully.")

def deactivate_volunteer():
    # Deactivate the selected volunteer
    selected_index = volunteers_listbox.curselection()[0]
    volunteers[selected_index].active = False
    messagebox.showinfo("Success", "Volunteer deactivated successfully.")

def delete_volunteer():
    # Delete the selected volunteer
    selected_index = volunteers_listbox.curselection()[0]
    del volunteers[selected_index]
    messagebox.showinfo("Success", "Volunteer deleted successfully.")

# Create buttons
load_button = tk.Button(root, text="Load Volunteers", command=load_volunteers)
save_button = tk.Button(root, text="Save Volunteers", command=save_volunteers)
deactivate_button = tk.Button(root, text="Deactivate Volunteer", command=deactivate_volunteer)
delete_button = tk.Button(root, text="Delete Volunteer", command=delete_volunteer)

# Arrange the buttons in a grid
load_button.grid(row=len(fields), column=0)
save_button.grid(row=len(fields), column=1)
deactivate_button.grid(row=len(fields), column=2)
delete_button.grid(row=len(fields), column=3)

# Run the application
root.mainloop()