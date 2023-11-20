import csv
import tkinter as tk
from tkinter import ttk, messagebox
from data_model import Camp, Inventory

class ResourceAllocationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Resource Allocation")
        self.root.geometry("700x600")  # Set window size
        self.root['bg'] = '#021631'  # Set background color

        # Initialize Tkinter variables
        self.camp_id_var = tk.StringVar()
        self.specific_needs_var = tk.StringVar()
        self.location_var = tk.StringVar()
        self.selected_camp = tk.StringVar()
        self.selected_resource = tk.StringVar()
        self.quantity_var = tk.StringVar()
        self.volunteer_id_var = tk.StringVar()
        self.capacity_var = tk.StringVar()
        self.allocatedresources_var = tk.StringVar()
        self.selected_resource_quantity_var = tk.StringVar()

        self.camps = self.load_camps_from_csv('camps_information.csv')
        self.resources = self.load_resources_from_csv('inventory.csv')

        self.selected_camp = tk.StringVar()
        self.selected_camp.trace('w', self.update_camp_info)  # Update camp info when a camp is selected

        self.selected_resource = tk.StringVar()
        self.quantity_var = tk.StringVar()

        self.setup_ui()

    def load_camps_from_csv(self, camps_information):
        camps = []
        with open(camps_information, 'r') as file:
            reader = csv.reader(file)
            header = next(reader) 
            for row in reader:
                allocatedresources = dict(zip(header[5:], row[5:]))
                camp = Camp(*row[:5], allocatedresources)
                camps.append(camp)
        return camps

    def load_resources_from_csv(self, inventory):
        resources = {}
        with open(inventory, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header row
            for row in reader:
                inventory = Inventory(*row)
                resources[inventory.inventory_name] = inventory
        return resources
    
    def update_camp_info(self, *args):
        selected_camp_id = self.selected_camp.get()
        selected_camp = next(camp for camp in self.camps if camp.camp_id == selected_camp_id)
        self.camp_id_var.set(selected_camp.camp_id)
        self.volunteer_id_var.set(selected_camp.volunteer_id)
        self.location_var.set(selected_camp.location)
        self.capacity_var.set(selected_camp.capacity)
        self.specific_needs_var.set(selected_camp.specific_needs)
        self.allocatedresources_var.set(selected_camp.allocatedresources)

    def allocate_resources(self):
        selected_camp_id = self.selected_camp.get()
        selected_resource_name = self.selected_resource.get()
        quantity = int(self.quantity_var.get())

        # Update the allocated resources for the selected camp
        for camp in self.camps:
            if camp.camp_id == selected_camp_id:
                # Ensure 'allocated_resources' is initialized as a dictionary
                if not isinstance(camp.allocatedresources, dict):
                    camp.allocatedresources = {}
                # Update the quantity for the selected resource
                current_quantity = int(camp.allocatedresources.get(selected_resource_name, 0))
                camp.allocatedresources[selected_resource_name] = current_quantity + quantity
                self.allocatedresources_var.set(camp.allocatedresources)
                break

        # Update the quantity of the selected resource in the inventory
        self.resources[selected_resource_name].quantity -= quantity

        # Save the updated camps and inventory to the CSV files
        self.save_data_to_csv('camps_information.csv', self.camps)
        self.save_data_to_csv('inventory.csv', self.resources.values())


    def save_data_to_csv(self,camps_information, data):
        with open(camps_information, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(data[0]._fields)  # Write the header row
            for item in data:
                writer.writerow(item)

    def save_camps_to_csv(self, inventory, camps):
        with open(inventory, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Camp ID', 'Volunteer ID', 'Location', 'Capacity', 'Specific Needs', 'Allocated Resources'])  # header
            for camp in camps:
                writer.writerow([camp.camp_id, camp.volunteer_id, camp.location, camp.capacity, camp.specific_needs, camp.allocatedresources])

    def save_resources_to_csv(self, inventory, resources):
        with open(inventory, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Inventory ID', 'Admin ID', 'Inventory Name', 'Quantity'])
            for resource in resources:
                writer.writerow([resource.inventory_id, resource.admin_id, resource.inventory_name, resource.quantity])

    def save_data(self):
        self.save_camps_to_csv('camps_information.csv', self.camps)
        self.save_resources_to_csv('inventory.csv', self.resources)
        messagebox.showinfo("Success", "Data saved successfully.")

    def update_camp_info(self, *args):
        selected_camp_id = self.selected_camp.get()
        selected_camp = next(camp for camp in self.camps if camp.camp_id == selected_camp_id)
        self.camp_id_var.set(selected_camp.camp_id)
        self.specific_needs_var.set(selected_camp.specific_needs)
        self.location_var.set(selected_camp.location)
    
    def update_resource_info(self, *args):
        selected_resource_id = self.selected_resource.get()
        selected_resource = next(resource for resource in self.resources if resource.resource_id == selected_resource_id)
        self.selected_resource_quantity_var.set(selected_resource.quantity)
    
    def setup_ui(self):
        bg_color = '#021631'
        fg_color = 'white'
        font_style = ("Calibri", 12)

    # Title
        title_label = tk.Label(self.root, text="Allocate Resources to Camps", fg=fg_color, bg=bg_color, font=("Calibri", 16))
        title_label.grid(row=0, column=0, columnspan=4, pady=20)

    # Select Camp Section
        camp_label = tk.Label(self.root, text="Select Camp:", fg=fg_color, bg=bg_color, font=font_style)
        camp_dropdown = ttk.Combobox(self.root, textvariable=self.selected_camp,
                                 values=[camp.camp_id for camp in self.camps], state="readonly")
        camp_label.grid(row=1, column=0, padx=20, pady=20)
        camp_dropdown.grid(row=1, column=1, padx=20, pady=20)

        camp_info_label = tk.Label(self.root, text="Camp Information:", fg=fg_color, bg=bg_color, font=font_style)
        camp_info_label.grid(row=1, column=2, columnspan=2, padx=20, pady=20)

        camp_id_label = tk.Label(self.root, textvariable=self.camp_id_var, fg=fg_color, bg=bg_color, font=font_style)
        camp_id_label.grid(row=2, column=2, padx=20, pady=20)

        specific_needs_label = tk.Label(self.root, textvariable=self.specific_needs_var, fg=fg_color, bg=bg_color, font=font_style)
        specific_needs_label.grid(row=3, column=2, padx=20, pady=20)

        volunteer_id_label = tk.Label(self.root, textvariable=self.volunteer_id_var,fg=fg_color, bg=bg_color, font=font_style)
        volunteer_id_label.grid(row=4, column=2, padx=20, pady=20)

        location_label = tk.Label(self.root, textvariable=self.location_var,fg=fg_color, bg=bg_color, font=font_style)
        location_label.grid(row=5, column=2, padx=20, pady=20)

        capacity_label = tk.Label(self.root, textvariable=self.capacity_var,fg=fg_color, bg=bg_color, font=font_style)
        capacity_label.grid(row=6, column=2)

        allocated_resources_label = tk.Label(self.root, textvariable=self.allocatedresources_var,fg=fg_color, bg=bg_color, font=font_style)
        allocated_resources_label.grid(row=7, column=2, padx=20, pady=20)

        resource_quantity_label = tk.Label(self.root, textvariable=self.selected_resource_quantity_var)
        resource_quantity_label.grid(row=3, column=2, padx=20, pady=20)

    # Resource Allocation Section
        resource_label = tk.Label(self.root, text="Select Resource:", fg=fg_color, bg=bg_color, font=font_style)
        resource_dropdown = ttk.Combobox(self.root, textvariable=self.selected_resource,
                                     values=list(self.resources.keys()), state="readonly")
        resource_label.grid(row=4, column=0, padx=20, pady=20)
        resource_dropdown.grid(row=4, column=1, padx=20, pady=20)

        quantity_label = tk.Label(self.root, text="Quantity:", fg=fg_color, bg=bg_color, font=font_style)
        quantity_entry = tk.Entry(self.root, textvariable=self.quantity_var,bg="white")
        quantity_label.grid(row=5, column=0, padx=20, pady=20)
        quantity_entry.grid(row=5, column=1, padx=20, pady=20)

        allocate_button = tk.Button(self.root, text="Allocate Resources", command=self.allocate_resources)
        allocate_button.grid(row=6, column=0, columnspan=2, padx=20, pady=20)

        save_button = tk.Button(self.root, text="Save Data", command=self.save_data)
        save_button.grid(row=8, column=0, columnspan=2, padx=20, pady=20)

# Main Application
if __name__ == "__main__":
    root = tk.Tk()
    app = ResourceAllocationApp(root)
    root.mainloop()
