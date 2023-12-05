from logging import root
import tkinter as tk
from tkinter import messagebox, ttk
import csv
import ast
from data_model import Camp, Inventory

def create_gui(parent):
    camps_information = []
    with open('camps.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        print(reader)
        for row in reader:
            if 'allocated_resources' in row and not row['allocated_resources']:
                allocated_resources = {}  
            else:
                allocated_resources = row['allocated_resources']
            camp_instance = Camp(
                camp_id=row['camp_id'],
                location=row['location'],
                volunteers_number=row['volunteers_number'],
                refugees_number=row['refugees_number'],
                plan_name=row['plan_name'],
                current_availability=row['current_availability'],
                max_capacity=row['max_capacity'],
                specific_needs=row['specific_needs'],
                allocated_resources=allocated_resources
            )
            camps_information.append(camp_instance)

    # Load inventory from inventory.csv
    inventory_data = []
    with open('inventory.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            inventory_data.append(Inventory(**row))

    frame=tk.Frame(parent,width=700, height=800,bg='#021631')
    tk.Label(frame,text='Allocate resources to camps', font="calibri 16",bg="#021631", fg="#fff").grid(row=4, column=0, padx=10, pady=30)
    
    camp_info_text = tk.Text(frame, height=15, width=40)
    camp_info_text.grid(row=9, column=0, padx=10, pady=10)

    inventory_info_text = tk.Text(frame, height=15, width=40)
    inventory_info_text.grid(row=9, column=1, padx=10, pady=10)

    
    camp_var = tk.StringVar(value=camps_information[0].camp_id)  # Default value
    camp_dropdown = ttk.Combobox(frame, textvariable=camp_var, values=[camp.camp_id for camp in camps_information])

    inventory_var = tk.StringVar(value=inventory_data[0].inventory_name)  # Default value
    inventory_dropdown = ttk.Combobox(frame, textvariable=inventory_var, values=[item.inventory_name for item in inventory_data])

    
    camp_dropdown.grid(row=7, column=0, padx=10, pady=10)
    inventory_dropdown.grid(row=7, column=1, padx=10, pady=10)

    
    def display_camp_information():
        selected_camp_id = camp_dropdown.get()
        camp_info_text.delete(1.0, tk.END)
        camp_info_text.insert(tk.END, "Camp Information:\n\n")
        for camp in camps_information:
            if camp.camp_id == selected_camp_id:
                camp_info_text.insert(tk.END, f"{camp.camp_id}\nLocation: {camp.location}\nCapacity: {camp.max_capacity}\nSpecific Needs: {camp.specific_needs}\nAllocated Resources: {camp.allocated_resources}\n\n")
                break

    def display_inventory():
        inventory_info_text.delete(1.0, tk.END)
        inventory_info_text.insert(tk.END, "Current Inventory:\n\n")
        for item in inventory_data:
            inventory_info_text.insert(tk.END, f"{item.inventory_name}\nQuantity: {item.quantity}\n\n")
        # inventory_info_text.config(state=tk.DISABLED)

    def display_information():
        display_camp_information()
        display_inventory()

    
    def allocate_resources():
        quantity = quantity_entry.get()
        selected_camp_id = camp_dropdown.get()
        selected_inventory_name = inventory_dropdown.get()
        quantity = quantity_entry.get()

        if not selected_camp_id:
            messagebox.showerror("Error", "No camp selected to allocate a resource.")
            return
        
        if not quantity:
            messagebox.showerror("Error", "Please enter a quantity.")
            return

        if not quantity.isdigit():
            messagebox.showerror("Error", "Quantity must be a number.")
            return

        quantity = int(quantity)

        inventory_dict = {}
        
        with open('inventory.csv', 'r') as f:
            reader = csv.reader(f)
            next(reader)  # Skip the header row
            for row in reader:
                inventory_dict[row[2]] = int(row[3])

        inventory = inventory_dict.get(selected_inventory_name)

        if inventory is None:
            messagebox.showerror("Error", "Choose an inventory item.")
            return

        if quantity > inventory:
            messagebox.showerror("Error", "Quantity cannot be greater than the inventory.")
            return

        try:
            allocated_quantity = int(quantity_entry.get())
            if allocated_quantity <= 0:
                raise ValueError("Quantity must be greater than zero.")

            for camp in camps_information:
                if camp.camp_id == selected_camp_id:
                    for item in inventory_data:
                        if item.inventory_name == selected_inventory_name:
                            if not camp.allocated_resources:        #check if the camp.allocated resources is empty string or not
                                aresources = {}
                            else:
                                aresources = ast.literal_eval(camp.allocated_resources)
                            aresources[selected_inventory_name] = aresources.get(
                                selected_inventory_name, 0) + allocated_quantity
                            camp.allocated_resources = str(aresources)
                            item.quantity = str(int(item.quantity) - allocated_quantity)
                            messagebox.showinfo("Allocation Success",
                                                f"{allocated_quantity} {selected_inventory_name} allocated to {selected_camp_id}")
                            display_camp_information()
                            break
                    break
        except ValueError as e:
                messagebox.showerror("Allocation Error", str(e))

    data_saved = tk.BooleanVar()
    data_saved.set(False)

    def back(frame):
        if not data_saved.get():
            messagebox.showwarning("Warning", "You have not saved your data.")
        else:
            frame.grid_forget()
        
    def save_data():
        with open('camps.csv', 'w', newline='') as csvfile:
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

    # buttons here
    display_button = tk.Button(frame, text="Display Information", command=display_information)
    allocate_button = tk.Button(frame, text="Allocate Resources", command=allocate_resources)
    save_button = tk.Button(frame, text="Save Data", width=10,command=save_data)
    back_button = tk.Button(frame, text="Back", width=10,command=lambda:back(frame))
    quantity_label = tk.Label(frame, text="Quantity:",font="calibri 10", bg="#021631",fg="#fff")
    quantity_entry = tk.Entry(frame)

    # place 
    display_button.grid(row=8, column=0, padx=10, pady=10)
    allocate_button.grid(row=11, column=1, padx=10, pady=10)
    back_button.grid(row=11, column=0, padx=10, pady=10)
    quantity_label.grid(row=10, column=0, padx=10, pady=10)
    quantity_entry.grid(row=10, column=1, padx=10, pady=10)
    save_button.grid(row=12, column=1, padx=10, pady=10)
    choose_camp_label = tk.Label(frame, text="CAMPS \n \n Choose which camp to display \n from the list below:",font="calibri 10", bg="#021631",fg="#fff")
    choose_camp_label.grid(row=6, column=0, padx=10, pady=10)

    choose_inventory_label = tk.Label(frame, text=" RESOURCES \n \n Choose resource to allocate to each camp. \n If you need multiple resources, \n please allocate them one at a time",font="calibri 10", bg="#021631",fg="#fff")
    choose_inventory_label.grid(row=6, column=1, padx=10, pady=10)

    # info_label = tk.Label(frame, text="Allocate Resources to Camps")
    # info_label.grid(row=0, column=1, padx=10, pady=10)

    return frame

    # root.mainloop()


