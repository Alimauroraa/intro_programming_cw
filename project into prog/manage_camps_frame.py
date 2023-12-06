import tkinter as tk
from tkinter import ttk, Entry
import pandas as pd
from tkinter import messagebox
import numpy as np

class EntryPopup(Entry):
    def __init__(self, parent, iid, column, text, is_integer=False, **kw):
        super().__init__(parent, **kw)
        self.parent = parent
        self.iid = iid
        self.column = column
        self.is_integer = is_integer
        self.insert(0, text)
        self['exportselection'] = False

        if self.is_integer:
            self.config(validate="key", validatecommand=(self.register(self.is_valid_integer), '%P'))

        self.focus_force()
        self.bind("<Return>", self.on_return)
        self.bind("<Escape>", self.on_escape)

    def is_valid_integer(self, P):
        if P.isdigit() or P == "":
            return True
        messagebox.showerror("Error", "Only integer values are allowed")
        return False

    def on_return(self, event):
        current_values = list(self.parent.item(self.iid, 'values'))
        col_index = int(self.column.replace('#', '')) - 1
        current_values[col_index] = self.get()
        self.parent.item(self.iid, values=current_values)
        self.destroy()

    def on_escape(self, event):
        self.destroy()

class ManageCampsFrame:
    def __init__(self, root):
        self.root = root
        self.tree = None
        self.xscrollbar = None
        self.setup_ui()

    def setup_ui(self):
        tk.Label(self.root, text="Manage camps", font="calibri 16", bg="#021631", fg="#fff").place(x=25, y=30)
        # Display a message above the table
        info_label = tk.Label(self.root, text="Location, Max Capacity & Specific Needs fields can be clicked & edited."
                                              "\n   Double click the field, make changes, "
                                              "press Enter and click Save Changes.",
                              font="calibri 12")
        info_label.place(x=25, y=60)
        # Create the Treeview
        self.tree = ttk.Treeview(self.root)
        self.tree.grid(row=0, column=0, sticky="nsew", padx=25, pady=100)

        # Define the columns for the treeview
        self.tree['columns'] = ('camp_id', 'location', 'volunteers_number', 'refugees_number',
                                'plan_name', 'current_availability', 'max_capacity',
                                'specific_needs', 'allocated_resources')
        self.tree['show'] = 'headings'

        # Setting the column headings and widths
        for col in self.tree['columns']:
            self.tree.heading(col, text=col.replace("_", " ").title())  # Replace underscores with spaces and title-case
            self.tree.column(col, width=120, stretch=tk.YES)  # Adjust the width as needed

        self.tree.config(height=20)

        # Add a horizontal scrollbar
        self.xscrollbar = ttk.Scrollbar(self.root, orient='horizontal', command=self.tree.xview)
        self.xscrollbar.grid(row=1, column=0, sticky='ew', padx=5)
        self.tree.configure(xscrollcommand=self.xscrollbar.set)

        # Grid configuration for the root window
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Enable editing on double-click
        self.tree.bind('<Double-1>', self.edit_cell)

        # Button to save changes
        save_button = tk.Button(self.root, text="Save Changes", command=self.save_changes)
        save_button.place(x=250, y=650)

        # Initially display camps
        self.display_camps()

    # def on_xscroll(self, *args):
    #     """Handle horizontal scrolling"""
    #     self.xscrollbar.set(*args)
    #     self.tree.xview(*args)

    def save_changes(self):
        camps_data = [{col: self.tree.set(child_id, col) for col in self.tree['columns']}
                      for child_id in self.tree.get_children()]
        df = pd.DataFrame(camps_data)
        df.to_csv('camps.csv', index=False)
        messagebox.showinfo("Success", "Changes saved to camps.csv")

    def edit_cell(self, event):
        column = self.tree.identify_column(event.x)
        editable_columns = ['#2', '#7', '#8']  # Columns that should be editable

        # Check if the column is in the list of editable columns
        if column not in editable_columns:
            return  # Do nothing if the column is not editable

        row = self.tree.identify_row(event.y)
        x, y, width, height = self.tree.bbox(row, column)
        text = self.tree.item(row)['values'][int(column[1:]) - 1]
        # Check if the column is 'max_capacity'
        if column == '#7':  # Adjust the column number as needed
            popup = EntryPopup(self.tree, row, column, text, is_integer=True)
        else:
            popup = EntryPopup(self.tree, row, column, text)

        popup.place(x=x, y=y, anchor='w', width=width, height=height)

    def sort_camps_df(self, camps_df):
        return camps_df.sort_values(by='camp_id', ascending=True)

    def display_camps(self):
        try:
            dtype_spec = {
                'current_availability': 'Int64',  # Using 'Int64' to handle NaN values as well
                'max_capacity': 'Int64',
                'volunteers_number': 'Int64',
                'refugees_number': 'Int64'
            }
            camps_df = pd.read_csv('camps.csv', dtype=dtype_spec)

            if camps_df.empty:
                messagebox.showinfo("Info", "No camps data available.")
                return
        except FileNotFoundError:
            messagebox.showinfo("Info", "The file 'camps.csv' does not exist.")
            return
        except pd.errors.EmptyDataError:
            messagebox.showinfo("Info", "The file 'camps.csv' is empty.")
            return

        # Clear existing data in the tree
        for i in self.tree.get_children():
            self.tree.delete(i)

        # Fill NaN values with empty strings for all columns
        camps_df.fillna('', inplace=True)
        camps_df = self.sort_camps_df(camps_df)
        # Insert rows into the treeview
        for _, row in camps_df.iterrows():
            # Convert all values to strings for display
            values = [str(value) for value in row.tolist()]
            self.tree.insert('', 'end', values=values)


if __name__ == '__main__':
    root = tk.Tk()
    root.title("Manage Camps")
    root.geometry("1200x600")
    app = ManageCampsFrame(root)
    root.mainloop()
