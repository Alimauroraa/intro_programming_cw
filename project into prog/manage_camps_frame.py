import tkinter as tk
from tkinter import ttk, Entry
import pandas as pd
from tkinter import messagebox

class EntryPopup(Entry):
    def __init__(self, parent, iid, column, text, **kw):
        super().__init__(parent, **kw)
        self.parent = parent
        self.iid = iid
        self.column = column
        self.insert(0, text)
        self['exportselection'] = False

        self.focus_force()
        self.bind("<Return>", self.on_return)
        self.bind("<Escape>", self.on_escape)

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
        self.setup_ui()

    def setup_ui(self):
        # Create the Treeview with horizontal scrollbar
        self.tree = ttk.Treeview(self.root, xscrollcommand=lambda f, l: self.on_xscroll(f, l))
        self.tree.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Define the columns for the treeview
        self.tree['columns'] = ('CampID', 'Location', 'Capacity', 'Specific Needs', 'Volunteers', 'Refugees', 'Resources Allocated')
        self.tree['show'] = 'headings'

        # Setting the column headings and widths
        for col in self.tree['columns']:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, stretch=tk.YES)

        # Add a horizontal scrollbar
        self.xscrollbar = ttk.Scrollbar(self.root, orient='horizontal', command=self.tree.xview)
        self.xscrollbar.grid(row=1, column=0, sticky='ew')
        self.tree.configure(xscrollcommand=self.xscrollbar.set)

        # Configure the treeview to use the scrollbar
        self.tree.configure(xscrollcommand=self.xscrollbar.set)

        # Enable editing on double-click
        self.tree.bind('<Double-1>', self.edit_cell)

        # Button to save changes
        save_button = tk.Button(self.root, text="Save Changes", command=self.save_changes)
        save_button.grid(row=2, column=0, pady=20, sticky='ew')

        # Initially display camps
        self.display_camps()

    def on_xscroll(self, *args):
        """Handle horizontal scrolling"""
        self.xscrollbar.set(*args)
        self.tree.xview(*args)

    def save_changes(self):
        camps_data = [{col: self.tree.set(child_id, col) for col in self.tree['columns']}
                      for child_id in self.tree.get_children()]
        df = pd.DataFrame(camps_data)
        df.to_csv('camps.csv', index=False)
        messagebox.showinfo("Success", "Changes saved to camps.csv")

    def edit_cell(self, event):
        column = self.tree.identify_column(event.x)
        row = self.tree.identify_row(event.y)
        x, y, width, height = self.tree.bbox(row, column)
        text = self.tree.item(row)['values'][int(column[1:]) - 1]
        popup = EntryPopup(self.tree, row, column, text)
        popup.place(x=x, y=y, anchor='w', width=width, height=height)

    def display_camps(self):
        try:
            camps_df = pd.read_csv('camps.csv')
            if camps_df.empty:
                messagebox.showinfo("Info", "No camps data available.")
                return
        except FileNotFoundError:
            messagebox.showinfo("Info", "The file 'camps.csv' does not exist.")
            return
        except pd.errors.EmptyDataError:
            messagebox.showinfo("Info", "The file 'camps.csv' is empty.")
            return
        for i in self.tree.get_children():
            self.tree.delete(i)
        try:
            camps_df = pd.read_csv('camps.csv')
            camps_df.fillna('', inplace=True)

            # Ensure the column name used here matches exactly with your CSV file's column name.
            # If your CSV has 'Camp ID', use 'Camp ID' instead of 'CampID'.
            if 'CampID' in camps_df.columns:
                # Correctly convert 'Camp ID' to an integer if it's a valid number
                def convert_to_int(val):
                    try:
                        return int(val)
                    except ValueError:
                        return val  # Return as is if it can't be converted to an integer

                camps_df['CampID'] = camps_df['CampID'].apply(convert_to_int)
            else:
                raise KeyError("Column 'Camp ID' does not exist in CSV.")

        except FileNotFoundError:
            messagebox.showerror("Error", "The file 'camps.csv' does not exist.")
            return
        except KeyError as e:
            messagebox.showerror("Error", str(e))
            return

        for _, row in camps_df.iterrows():
            values = [str(value) for value in row.tolist()]
            self.tree.insert('', 'end', values=values)


if __name__ == '__main__':
    root = tk.Tk()
    root.title("Manage Camps")
    root.geometry("800x600")
    app = ManageCampsFrame(root)
    root.mainloop()
