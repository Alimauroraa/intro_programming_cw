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

        self.camps = self.load_camps_from_csv('camps_information.csv')
        self.resources = self.load_resources_from_csv('inventory.csv')

        self.selected_camp = tk.StringVar()
        self.volunteer_id_var = tk.StringVar()
        self.location_var = tk.StringVar()
        self.capacity_var = tk.StringVar()
        self.specific_needs_var = tk.StringVar()
        self.allocate_resources_var = tk.StringVar()
        self.camp_id_var = tk.StringVar()
        self.selected_camp.trace('w', self.update_camp_info)  # Default to the first camp

        self.selected_resource = tk.StringVar()
        self.selected_resource.set(list(self.resources.keys())[0])  # Default to the first resource

        self.quantity_var = tk.IntVar(value=1)

        self.setup_ui()

    def load_camps_from_csv(self, filename):
        camps = []
        with open(filename, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                row = {key.strip(): value for key, value in row.items() if key is not None}  # Strip spaces from keys
                camp = Camp(**row)
                camps.append(camp)
        return camps

    def load_resources_from_csv(self, filename):
        resources = {}
        with open(filename, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                resources[row['inventory_name']] = int(row['quantity'])
        return resources

    def allocate_resources(self):
        selected_camp_id = self.selected_camp.get()
        selected_camp = next(camp for camp in self.camps if camp.camp_id == selected_camp_id)

        selected_resource = self.selected_resource.get()
        quantity = self.quantity_var.get()

        if selected_resource in self.resources and self.resources[selected_resource] >= quantity:
            inventory_item = Inventory(
                inventory_id=None, admin_id=None, inventory_name=selected_resource, quantity=quantity
            )
            selected_camp.inventory.append(inventory_item)
            selected_camp.allocatedresources += quantity 
            self.update_inventory_combobox()
            messagebox.showinfo("Success", f"Allocated {quantity} {selected_resource} to Camp {selected_camp.camp_id}")
        else:
            messagebox.showerror("Error", f"Not enough {selected_resource} available for Camp {selected_camp.camp_id}")

    def update_inventory_combobox(self):
        self.resource_combobox['values'] = list(self.resources.keys())

    def save_camps_to_csv(self, filename, camps):
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Camp ID', 'Volunteer ID', 'Location', 'Capacity', 'Specific Needs', 'Resources Allocated'])  # header
            for camp in camps:
                writer.writerow([camp.camp_id, camp.volunteer_id, camp.location, camp.capacity, camp.specific_needs, camp.allocatedresources])

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


    def setup_ui(self):
        # Select Camp Section
        camp_label = tk.Label(self.root, text="Select Camp:")
        camp_dropdown = ttk.Combobox(self.root, textvariable=self.selected_camp,
                                     values=[camp.camp_id for camp in self.camps], state="readonly")
        camp_label.grid(row=0, column=0)
        camp_dropdown.grid(row=0, column=1)

        camp_info_label = tk.Label(self.root, text="Camp Information:")
        camp_info_label.grid(row=0, column=3, columnspan=2)

        camp_id_label = tk.Label(self.root, textvariable=self.camp_id_var)
        camp_id_label.grid(row=2, column=3)

        specific_needs_label = tk.Label(self.root, textvariable=self.specific_needs_var)
        specific_needs_label.grid(row=3, column=3)

        location_label = tk.Label(self.root, textvariable=self.location_var)
        location_label.grid(row=4, column=3)
        
        # Resource Allocation Section
        resource_allocation_label = tk.Label(self.root, text="Allocate Resources:")
        resource_allocation_label.grid(row=2, column=0, columnspan=2)

        resource_label = tk.Label(self.root, text="Select Resource:")
        self.resource_combobox = ttk.Combobox(self.root, textvariable=self.selected_resource,
                                             values=list(self.resources.keys()), state="readonly")
        resource_label.grid(row=3, column=0)
        self.resource_combobox.grid(row=3, column=1)

        quantity_label = tk.Label(self.root, text="Quantity:")
        quantity_entry = tk.Entry(self.root, textvariable=self.quantity_var)
        quantity_label.grid(row=4, column=0)
        quantity_entry.grid(row=4, column=1)

        allocate_button = tk.Button(self.root, text="Allocate", command=self.allocate_resources)
        allocate_button.grid(row=5, column=0, columnspan=2)

        # Save Button
        save_button = tk.Button(self.root, text="Save Data", command=self.save_data)
        save_button.grid(row=6, column=0, columnspan=2)

# Main Application
if __name__ == "__main__":
    root = tk.Tk()
    app = ResourceAllocationApp(root)
    root.mainloop()
