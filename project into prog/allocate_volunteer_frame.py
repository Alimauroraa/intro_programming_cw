import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pandas as pd

class AllocateVolunteersFrame(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.root.title("Allocate Volunteers")

        # Read volunteers_file.csv and camps.csv
        self.volunteers_df = pd.read_csv("volunteers_file.csv", dtype={'camp_id': 'Int64'})
        self.camps_df = pd.read_csv("camps.csv", dtype={'volunteers_number': 'Int64'})

        # Create and configure GUI components
        self.create_gui()
        self.populate_volunteers_table()

    def create_gui(self):
        main_frame = tk.Frame(self.root)
        main_frame.pack()

        # Dropdown for selecting a camp
        tk.Label(main_frame, text="Select Camp:").pack()
        self.camp_var = tk.StringVar()
        self.camp_dropdown = ttk.Combobox(main_frame, textvariable=self.camp_var, state="readonly")
        sorted_camp_ids = sorted(self.camps_df['camp_id'].tolist())
        self.camp_dropdown['values'] = ['Not assigning camps for now'] + sorted_camp_ids
        self.camp_dropdown.pack()
        self.camp_dropdown.bind('<<ComboboxSelected>>', self.on_camp_select)

        # Treeview for displaying volunteers
        self.volunteers_tree = ttk.Treeview(main_frame, columns=('user_id', 'first_name', 'last_name', 'camp_id'),
                                            show='headings')
        self.volunteers_tree.heading('user_id', text='User ID')
        self.volunteers_tree.heading('first_name', text='First Name')
        self.volunteers_tree.heading('last_name', text='Last Name')
        self.volunteers_tree.heading('camp_id', text='Camp ID')

        # Set column widths
        self.volunteers_tree.column('user_id', width=100)
        self.volunteers_tree.column('first_name', width=150)
        self.volunteers_tree.column('last_name', width=150)
        self.volunteers_tree.column('camp_id', width=100)
        self.volunteers_tree.pack()

        # Button to allocate volunteers
        allocate_button = tk.Button(main_frame, text="Allocate Selected Volunteer",
                                    command=self.allocate_selected_volunteer)
        allocate_button.pack()

    def populate_volunteers_table(self):
        # Filter the DataFrame to include only active volunteers
        active_volunteers_df = self.volunteers_df[self.volunteers_df['active'] == True]

        for index, row in active_volunteers_df.iterrows():
            self.volunteers_tree.insert('', index,
                                        values=(row['user_id'], row['first_name'], row['last_name'], row['camp_id']))

    def allocate_selected_volunteer(self):
        selected_camp_id = self.camp_var.get()

        if not selected_camp_id.strip():
            messagebox.showerror("Error", "Please select a camp.")
            return

        selected_item = self.volunteers_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a volunteer.")
            return

        selected_volunteer_id = self.volunteers_tree.item(selected_item[0])['values'][0]

        # Handle 'Not assigning camps for now' option
        if selected_camp_id == 'Not assigning camps for now':
            selected_camp_id_int = None  # Set to None to make the field empty
        else:
            try:
                selected_camp_id_int = int(selected_camp_id)
            except ValueError:
                messagebox.showerror("Error", "Camp ID must be an integer.")
                return

        # Update the selected volunteer's camp_id with the integer value
        self.volunteers_df.loc[self.volunteers_df['user_id'] == selected_volunteer_id, 'camp_id'] = selected_camp_id_int
        self.volunteers_df.to_csv("volunteers_file.csv", index=False)

        # Update Treeview
        for item in self.volunteers_tree.get_children():
            self.volunteers_tree.delete(item)
        self.populate_volunteers_table()
        self.update_camp_volunteer_numbers()

        messagebox.showinfo("Success", f"Volunteer {selected_volunteer_id} allocated to Camp {selected_camp_id_int}.")

    def update_camp_volunteer_numbers(self):
        volunteer_counts = self.volunteers_df['camp_id'].value_counts()

        # Update volunteer counts
        for camp_id, count in volunteer_counts.items():
            self.camps_df.loc[self.camps_df['camp_id'] == camp_id, 'volunteers_number'] = count

        # Ensure camps without volunteers are updated
        all_camp_ids = set(self.camps_df['camp_id'])
        counted_camp_ids = set(volunteer_counts.index)
        camps_without_volunteers = all_camp_ids - counted_camp_ids
        for camp_id in camps_without_volunteers:
            self.camps_df.loc[self.camps_df['camp_id'] == camp_id, 'volunteers_number'] = 0

        # Convert the volunteers_number column to nullable integer type
        self.camps_df['volunteers_number'] = self.camps_df['volunteers_number'].astype('Int64')

        # Save the updated camps dataframe
        self.camps_df.to_csv("camps.csv", index=False)

    def on_camp_select(self, event=None):
        # This method is triggered when a camp is selected from the dropdown
        selected_camp = self.camp_dropdown.get()
        print("Selected camp:", selected_camp)

        # Update the self.camp_var with the selected camp
        self.camp_var.set(selected_camp)


if __name__ == '__main__':
    root = tk.Tk()
    root.title("Allocate Volunteer")
    root.geometry("1200x1000")
    app = AllocateVolunteersFrame(root)
    root.mainloop()
