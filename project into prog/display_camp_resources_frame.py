import tkinter as tk
from tkinter import ttk
import pandas as pd
import ast  # for safely evaluating string literals as Python expressions

class DisplayAllocatedResourcesFrame(tk.Frame):
    def __init__(self, parent, volunteer_id, **kwargs):
        super().__init__(parent, **kwargs)
        self.volunteer_id = volunteer_id
        self.tree = None
        self.setup_ui()

    def setup_ui(self):
        # Create the Treeview
        self.tree = ttk.Treeview(self, columns=('Resource', 'Quantity'))
        self.tree.heading('Resource', text='Resource')
        self.tree.heading('Quantity', text='Quantity')
        self.tree.column('Resource', width=120)
        self.tree.column('Quantity', width=120)
        self.tree['show'] = 'headings'
        self.tree.pack(expand=True, fill='both', side='left')

        # Add a scrollbar
        scrollbar = ttk.Scrollbar(self, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')

        # Load and display data
        self.load_data()

    def load_data(self):
        try:
            # Load the volunteer data
            volunteers_df = pd.read_csv('volunteers_file.csv')
            camps_df = pd.read_csv('camps.csv')

            # Check if the volunteer ID is valid and if 'camp_id' exists
            if self.volunteer_id not in volunteers_df['user_id'].values:
                print("Invalid volunteer ID.")
                return

            if 'camp_id' not in volunteers_df.columns:
                print("'camp_id' column not found in the volunteers file.")
                return

            # Get the camp_id for the volunteer
            camp_id = volunteers_df.loc[volunteers_df['user_id'] == self.volunteer_id, 'camp_id'].iloc[0]

            # Check if the 'allocated_resources' column exists in camps.csv
            if 'allocated_resources' not in camps_df.columns:
                print("'allocated_resources' column not found in the camps CSV file.")
                return

            # Find the record for the given camp_id
            camp_record = camps_df[camps_df['camp_id'] == camp_id].iloc[0]

            # Extract and parse the allocated_resources data
            allocated_resources = ast.literal_eval(camp_record['allocated_resources'])

            # Insert data into the treeview
            for resource, quantity in allocated_resources.items():
                self.tree.insert('', 'end', values=(resource, quantity))
        except Exception as e:
            print("Error loading data:", e)
            # Handle the error as needed


def main():
    root = tk.Tk()
    root.title("Display Allocated Resources")
    root.geometry("400x300")

    volunteer_id = 1  # Replace with the actual volunteer ID you want to display
    app = DisplayAllocatedResourcesFrame(root, volunteer_id=volunteer_id)
    app.pack(expand=True, fill='both')

    root.mainloop()

if __name__ == "__main__":
    main()
