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
        self.volunteers_df = pd.read_csv("volunteers_file.csv")
        self.camps_df = pd.read_csv("camps.csv")

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
        self.camp_dropdown['values'] = self.camps_df['camp_id'].tolist()
        self.camp_dropdown.pack()
        self.camp_dropdown.bind('<<ComboboxSelected>>', self.on_camp_select)

        # Treeview for displaying volunteers
        self.volunteers_tree = ttk.Treeview(main_frame, columns=('user_id', 'first_name', 'last_name', 'camp_id'),
                                            show='headings')
        self.volunteers_tree.heading('user_id', text='User ID')
        self.volunteers_tree.heading('first_name', text='First Name')
        self.volunteers_tree.heading('last_name', text='Last Name')
        self.volunteers_tree.heading('camp_id', text='Camp ID')
        self.volunteers_tree.pack()

        # Button to allocate volunteers
        allocate_button = tk.Button(main_frame, text="Allocate Selected Volunteer",
                                    command=self.allocate_selected_volunteer)
        allocate_button.pack()

    def populate_volunteers_table(self):
        for index, row in self.volunteers_df.iterrows():
            self.volunteers_tree.insert('', index, values=(row['user_id'], row['first_name'], row['last_name'],
                                                           row['camp_id']))

    def allocate_selected_volunteer(self):
        selected_camp_id = self.camp_var.get()
        print(f"Selected camp ID: '{selected_camp_id}'")  # Debugging line

        if not selected_camp_id.strip():
            messagebox.showerror("Error", "Please select a camp.")
            return

        selected_item = self.volunteers_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a volunteer.")
            return

        selected_volunteer_id = self.volunteers_tree.item(selected_item[0])['values'][0]

        # Update the selected volunteer's camp_id
        self.volunteers_df.loc[self.volunteers_df['user_id'] == selected_volunteer_id, 'camp_id'] = selected_camp_id
        self.volunteers_df.to_csv("volunteers_file.csv", index=False)

        # Update Treeview
        for item in self.volunteers_tree.get_children():
            self.volunteers_tree.delete(item)
        self.populate_volunteers_table()

        messagebox.showinfo("Success", f"Volunteer {selected_volunteer_id} allocated to Camp {selected_camp_id}.")

    def on_camp_select(self, event=None):
        # This method is triggered when a camp is selected from the dropdown
        selected_camp = self.camp_dropdown.get()
        print("Selected camp:", selected_camp)

        # Update the self.camp_var with the selected camp
        self.camp_var.set(selected_camp)


if __name__ == '__main__':
    root = tk.Tk()
    root.title("Allocate Volunteer")
    root.geometry("1200x600")
    app = AllocateVolunteersFrame(root)
    root.mainloop()
