import tkinter as tk
from tkinter import messagebox
from edit_camp import Camp
import pandas as pd

class EditCampFrame(tk.Frame):
    def __init__(self, parent, camp):
        tk.Frame.__init__(self, parent)
        self.camp = camp
        self.create_widgets()

        self.autofill_button = tk.Button(self, text="Autofill Current Camp Information with Camp ID",
                                         command=self.autofill_data)
        self.autofill_button.grid(row=7, columnspan=2)

        self.submit_button = tk.Button(self, text="Submit", command=self.submit)
        self.submit_button.grid(row=8, columnspan=2)

        self.display_resources_button = tk.Button(self, text="Display Resources", command=self.display_resources)
        self.display_resources_button.grid(row=9, columnspan=2)

        self.resources_label = tk.Label(self, text="")
        self.resources_label.grid(row=10, columnspan=2)

    def create_widgets(self):
        tk.Label(self, text="Camp ID:").grid(row=0, column=0)
        self.camp_id_entry = tk.Entry(self)
        self.camp_id_entry.grid(row=0, column=1)

        # Volunteer ID
        tk.Label(self, text="Volunteer ID:").grid(row=1, column=0)
        self.volunteer_id_entry = tk.Entry(self)
        self.volunteer_id_entry.grid(row=1, column=1)

        # Location
        tk.Label(self, text="Location:").grid(row=2, column=0)
        self.location_entry = tk.Entry(self)
        self.location_entry.grid(row=2, column=1)

        # Capacity
        tk.Label(self, text="Capacity:").grid(row=3, column=0)
        self.capacity_entry = tk.Entry(self)
        self.capacity_entry.grid(row=3, column=1)

        # Specific Needs
        tk.Label(self, text="Specific Needs:").grid(row=4, column=0)
        self.specific_needs_entry = tk.Entry(self)
        self.specific_needs_entry.grid(row=4, column=1)

        # Resources
        tk.Label(self, text="Resources:").grid(row=5, column=0)
        self.resources_entry = tk.Entry(self)
        self.resources_entry.grid(row=5, column=1)

        self.submit_button = tk.Button(self, text="Submit", command=self.submit)
        self.submit_button.grid(row=7, columnspan=2)

    def submit(self):
        camp_id = self.camp_id_entry.get()
        volunteer_id = self.volunteer_id_entry.get()
        location = self.location_entry.get()
        capacity = self.capacity_entry.get()
        specific_needs = self.specific_needs_entry.get()
        resources = self.resources_entry.get()

        updated_info = {
            'Volunteer ID': volunteer_id,
            'Location': location,
            'Capacity': capacity,
            'Specific Needs': specific_needs,
            'Resources': resources
        }

        if self.camp.update_camp(camp_id, updated_info):
            messagebox.showinfo("Success", "Camp information updated successfully.")
        else:
            messagebox.showerror("Error", "Camp ID not found.")

    def display_resources(self):
        camp_id = self.camp_id_entry.get()
        resources = self.camp.get_resources(camp_id)

        if resources == "Invalid Camp ID" or resources == "Camp ID not found":
            messagebox.showerror("Error", resources)
        else:
            messagebox.showinfo("Resources", f"Resources: {resources}")

    def autofill_data(self):
        camp_id = self.camp_id_entry.get()
        camp_info = self.camp.get_camp_info(camp_id)

        if camp_info:
            for entry, key in [(self.volunteer_id_entry, 'Volunteer ID'),
                               (self.location_entry, 'Location'),
                               (self.capacity_entry, 'Capacity'),
                               (self.specific_needs_entry, 'Specific Needs'),
                               (self.resources_entry, 'Resources')]:
                entry.delete(0, tk.END)
                # Replace NaN with an empty string
                value = camp_info.get(key, '')
                if pd.isna(value):
                    value = ''
                entry.insert(0, value)
        else:
            messagebox.showerror("Error", "Camp ID not found or invalid.")

def main():
    root = tk.Tk()
    root.title("Edit Camp Information")
    camp = Camp("camps.csv")
    EditCampFrame(root, camp).pack()
    root.mainloop()

if __name__ == "__main__":
    main()

