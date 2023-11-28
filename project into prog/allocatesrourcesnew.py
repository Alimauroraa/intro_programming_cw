from logging import root
import tkinter as tk
from tkinter import messagebox, ttk
import csv
import ast
from data_model import Camp, Inventory

# Load camp information from camps_information.csv
camps_information = []
with open('camps_information.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        camps_information.append(Camp(**row))

# Load inventory from inventory.csv
inventory_data = []
with open('inventory.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        inventory_data.append(Inventory(**row))

# Create a tkinter window
root = tk.Tk()
root.title("Camp Resource Allocation")
root.configure(bg='#021631')

main_window = root

# Set the window size
main_window_width = 750
main_window_height = 500

    # Get screen width and height
screen_width = main_window.winfo_screenwidth()
screen_height = main_window.winfo_screenheight()

screen_width = main_window.winfo_screenwidth()
screen_height = main_window.winfo_screenheight()

    # Calculate the position to center the window
x_position = (screen_width - main_window_width) // 2
y_position = (screen_height - main_window_height) // 2

    # Set the window geometry
main_window.geometry(f"{main_window_width}x{main_window_height}+{x_position}+{y_position}")


frame = tk.Frame(main_window, width=850, height=500, bg='#021631')
#frame.grid(row=0, column=0, padx=0, sticky='nsew')

# Create a function to display camp information
def display_camp_information():
    selected_camp_id = camp_var.get()  # Get the selected camp from the dropdown menu
    camp_info_text.delete(1.0, tk.END)  # Clear the camp information text widget
    camp_info_text.insert(tk.END, "Camp Information:\n\n")

    for camp in camps_information:
        if camp.camp_id == selected_camp_id:
            camp_info_text.insert(tk.END, f"{camp.camp_id}\nLocation: {camp.location}\nCapacity: {camp.capacity}\nSpecific Needs: {camp.specific_needs}\nAllocated Resources: {camp.allocatedresources}\n\n")
            break

# Create a function to display inventory
def display_inventory():
    inventory_info_text.delete(1.0, tk.END)  # Clear the inventory text widget
    inventory_info_text.insert(tk.END, "Current Inventory:\n\n")
    for item in inventory_data:
        inventory_info_text.insert(tk.END, f"{item.inventory_name}\nQuantity: {item.quantity}\n\n")

# Create a function to display both camp information and inventory
def display_information():
    display_camp_information()
    display_inventory()

# Create a function to allocate resources
def allocate_resources():
    selected_camp_id = camp_var.get()  # Get the selected camp from the dropdown menu
    selected_inventory_name = inventory_var.get()  # Get the selected inventory from the dropdown menu

    try:
        allocated_quantity = int(quantity_entry.get())  # Get the quantity from the entry widget
        if allocated_quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")

        for camp in camps_information:
            if camp.camp_id == selected_camp_id:
                for item in inventory_data:
                    if item.inventory_name == selected_inventory_name:
                        allocated_resources = ast.literal_eval(camp.allocatedresources)  # Convert string to dictionary
                        allocated_resources[selected_inventory_name] = allocated_resources.get(selected_inventory_name, 0) + allocated_quantity
                        camp.allocatedresources = str(allocated_resources)  # Convert dictionary to string
                        item.quantity = str(int(item.quantity) - allocated_quantity)  # Update quantity as a string
                        messagebox.showinfo("Allocation Success", f"{allocated_quantity} {selected_inventory_name} allocated to {selected_camp_id}")
                        display_camp_information()  # Update the displayed camp information
                        break
                break
    except ValueError as e:
        messagebox.showerror("Allocation Error", str(e))

# Create a function to clear the text boxes
def clear_text():
    camp_info_text.delete(1.0, tk.END)
    inventory_info_text.delete(1.0, tk.END)

# Create a function to save the updated data
def save_data():
    # Save camp and inventory data to camps_information.csv and inventory.csv
    with open('camps_information.csv', 'w', newline='') as csvfile:
        fieldnames = camps_information[0].__dict__.keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for camp in camps_information:
            writer.writerow(camp.__dict__)

    with open('inventory.csv', 'w', newline='') as csvfile:
        fieldnames = inventory_data[0].__dict__.keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for item in inventory_data:
            writer.writerow(item.__dict__)

    messagebox.showinfo("Save Success", "Data saved successfully.")

# Create tkinter buttons, labels, and entry
display_button = tk.Button(root, text="Display Information", command=display_information)
allocate_button = tk.Button(root, text="Allocate Resources", command=allocate_resources)
save_button = tk.Button(root, text="Save Data", command=save_data)
clear_button = tk.Button(root, text="Go Back", command=clear_text)

quantity_label = tk.Label(root, text="Quantity:")
quantity_entry = tk.Entry(root)

# Place the buttons, labels, and entry in the tkinter window using grid layout
#display_button.place(x=236,y=300)
display_button.grid(row=0, column=0, padx=5, pady=5)
allocate_button.grid(row=4, column=1, padx=10, pady=10)
save_button.grid(row=0, column=2, padx=10, pady=10)
clear_button.grid(row=0, column=2, padx=10, pady=10)
quantity_label.grid(row=3, column=0, padx=10, pady=10)
quantity_entry.grid(row=3, column=1, padx=10, pady=10)
save_button.grid(row=1, column=2, padx=10, pady=10)

# Create Text widgets to display camp information and inventory
camp_info_text = tk.Text(root, height=15, width=40)
camp_info_text.grid(row=2, column=0, padx=10, pady=10)

inventory_info_text = tk.Text(root, height=15, width=40)
inventory_info_text.grid(row=2, column=1, padx=10, pady=10)

# Create dropdown menus for camps and inventory
camp_var = tk.StringVar(value=camps_information[0].camp_id)  # Default value
camp_dropdown = ttk.Combobox(root, textvariable=camp_var, values=[camp.camp_id for camp in camps_information])

inventory_var = tk.StringVar(value=inventory_data[0].inventory_name)  # Default value
inventory_dropdown = ttk.Combobox(root, textvariable=inventory_var, values=[item.inventory_name for item in inventory_data])

# Place the dropdowns in the tkinter window using grid layout
camp_dropdown.grid(row=1, column=0, padx=10, pady=10)
inventory_dropdown.grid(row=1, column=1, padx=10, pady=10)

# Start the tkinter event loop
root.mainloop()
