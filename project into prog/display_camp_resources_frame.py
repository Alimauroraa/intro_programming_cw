import tkinter as tk
from tkinter import ttk


class DisplayCampResourcesFrame(tk.Frame):
    def __init__(self, parent, camp_id, **kwargs):
        super().__init__(parent, **kwargs)
        self.camp_id = camp_id
        self.tree = None
        self.setup_ui()

    def setup_ui(self):
        # Create a Treeview to display resources
        self.tree = ttk.Treeview(self)
        self.tree['columns'] = ('Resource', 'Quantity')
        self.tree.column('#0', width=0, stretch=tk.NO)
        self.tree.column('Resource', anchor=tk.W, width=120)
        self.tree.column('Quantity', anchor=tk.W, width=120)

        self.tree.heading('#0', text='', anchor=tk.W)
        self.tree.heading('Resource', text='Resource', anchor=tk.W)
        self.tree.heading('Quantity', text='Quantity', anchor=tk.W)

        self.tree.pack(expand=True, fill='both')
        self.display_resources()

    def display_resources(self):
        # Fetch and display resources for the given camp_id
        # For demonstration, I'm using a placeholder for data fetching
        # Replace this with actual data retrieval logic
        allocated_resources = self.fetch_resources_for_camp(self.camp_id)

        for resource, quantity in allocated_resources.items():
            self.tree.insert('', tk.END, values=(resource, quantity))

    def fetch_resources_for_camp(self, camp_id):
        # Placeholder for fetching resources data
        # Implement actual data retrieval logic here
        return {"Tents": 50, "Water Bottles": 200}  # Example data
