import random
import pandas as pd
import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox
from tkinter import ttk
csv_filename = 'Refugee_DataFrame.csv'
camp_csv = 'camps.csv'
refugee_df = pd.read_csv(csv_filename)
camps_df = pd.read_csv(camp_csv)

bg_color = '#021631'
class MainMenuWindow:
    def __init__(self, master):
        self.master = master
        master.title("Refugee Portal")

        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()

        x = (screen_width - 700) // 2  # Adjust 500 based on the width of your window
        y = (screen_height - 800) // 2  # Adjust 300 based on the height of your window

        # Set the geometry of the main window
        master.geometry(f"700x800+{x}+{y}")
        master['bg'] = bg_color

        self.label = tk.Label(master, text="Hello and welcome to the refugee portal!", bg=bg_color,
        fg="white",
        font=("Calibri", 14))
        self.label.pack(pady=(150, 10))

        # Buttons for menu options
        self.add_button = tk.Button(master, text="Add a new refugee", command=self.add_refugee, font=("Calibri", 12),
        width=20,
        height=0,
        bg="#FFFFFF",
        fg="black",
        cursor="hand2",
        activebackground="#B8B8B8",
        activeforeground="black")
        self.add_button.pack(pady=10)

        self.edit_button = tk.Button(master, text="Edit an existing refugee", command=self.edit_refugee, font=("Calibri", 12),
        width=20,
        height=0,
        bg="#FFFFFF",
        fg="black",
        cursor="hand2",
        activebackground="#B8B8B8",
        activeforeground="black")
        self.edit_button.pack(pady=10)

        self.view_button = tk.Button(master, text="View the database", command=self.view_database, font=("Calibri", 12),
        width=20,
        height=0,
        bg="#FFFFFF",
        fg="black",
        cursor="hand2",
        activebackground="#B8B8B8",
        activeforeground="black")
        self.view_button.pack(pady=10)

        self.delete_button = tk.Button(master, text="Delete a refugee", command=self.delete_refugee, font=("Calibri", 12),
        width=20,
        height=0,
        bg="#FFFFFF",
        fg="black",
        cursor="hand2",
        activebackground="#B8B8B8",
        activeforeground="black")
        self.delete_button.pack(pady=10)

        self.show_database = True

        self.exit_button = tk.Button(master, text="Go back", command=self.exit_application, font=("Calibri", 12),
        width=20,
        height=0,
        bg="#FFFFFF",
        fg="black",
        cursor="hand2",
        activebackground="#B8B8B8",
        activeforeground="black")
        self.exit_button.pack(pady=10)

    def exit_application(self):
        self.master.destroy()

    def generate_refugee_id(self):
        if refugee_df["Refugee_ID"].empty:
            return 1  # Start from 1 if the DataFrame is empty
        else:
            return refugee_df["Refugee_ID"].max() + 1

    def add_refugee(self):
        #self.master.iconify()
        input_window = tk.Toplevel(self.master)
        input_window.title("Add New Refugee")
        input_window['bg'] = bg_color
        input_window.geometry('700x800')

        camps_df = pd.read_csv(camp_csv) 
        available_camps = camps_df[camps_df['current_availability'] > 0]

        screen_width = input_window.winfo_screenwidth()
        screen_height = input_window.winfo_screenheight()

        x_position = (screen_width - 700) // 2
        y_position = (screen_height - 800) // 2

        input_window.geometry(f'+{x_position}+{y_position}')

        if available_camps.empty:
            messagebox.showerror("No Camps Available", "No Camps available to create a refugee.")
            input_window.destroy()
            return

        while True:
            if camps_df.empty:
                messagebox.showerror("Empty Camps File",
                                     "The camps file is empty. Please add camps before adding refugees.")
                input_window.quit()
                input_window.destroy()
                #self.master.deiconify()
                return
            else:
                break

        refugee_ID_var = tk.StringVar(value=str(self.generate_refugee_id()))


        # while True:
        #     random_profile_id = random.randint(1, 999)
        #
        #     if random_profile_id not in refugee_df["Profile_ID"].values:
        #         profile_ID_var = tk.StringVar(value=str(random_profile_id))
        #         break

         # Filter out camps with zero availability
        available_camps_with_availability = camps_df[camps_df['current_availability'] > 0]
        available_camp_ids = available_camps_with_availability['camp_id'].tolist()

        if not available_camp_ids:
            messagebox.showerror("No Available Camps",
                                 "There are no camps with available space. Please add more camps.")
            input_window.destroy()
            #self.master.deiconify()
            return

        camp_ID_var = tk.StringVar()
        camp_ID_var.set(available_camp_ids[0])  # Set the default value

        def back(input_window):
            input_window.destroy()
            #self.master.deiconify()

        def process_input():
            # For simplicity, I'm only checking if the fields are not empty
            while True:
                if not first_name_var.get() or not last_name_var.get() \
                        or not gender_var.get() or not medical_condition_var.get() \
                        or not lead_family_member_var.get() or not lead_phone_number_var.get() or not number_of_relatives_var.get():
                    messagebox.showerror("Invalid Input", "All fields must be filled")
                    return
                else:
                    break

            # Additional validation can be added here (e.g., checking gender, ensuring numbers are valid, etc.)
            while True:
                camp_id_value = camp_ID_var.get()
                if not camp_id_value.isdigit():
                    messagebox.showerror("Invalid Input", "Ensure Camp ID is a number")
                    return
                else:
                    break

            while True:
                first_name_value = first_name_var.get().capitalize()
                if not first_name_value.isalpha():
                    messagebox.showerror("Invalid Input", "Ensure first name has no numbers or special characters")
                    return
                else:
                    break

            while True:
                last_name_value = last_name_var.get().capitalize()
                if not last_name_value.isalpha():
                    messagebox.showerror("Invalid Input", "Ensure last name has no numbers or special characters")
                    return
                else:
                    break

            while True:
                gender_value = gender_var.get().capitalize()
                if gender_value.capitalize() in ["Male", "Female", "Other"]:
                    break
                else:
                    messagebox.showerror("Invalid Input", "Ensure gender is either Male, Female, or Other")
                    return



            medical_condition_value = medical_condition_var.get().capitalize()

            while True:
                lead_family_member_value = lead_family_member_var.get().capitalize()
                if not lead_family_member_value.isalpha():
                    messagebox.showerror("Invalid Input", "Ensure lead family member name does not have numbers or special characters")
                    return
                else:
                    break

            while True:
                lead_phone_number_value = lead_phone_number_var.get()
                if not lead_phone_number_value.isdigit():
                    messagebox.showerror("Invalid Input", "Ensure there are no letters, only numbers of phone numbers")
                    return
                else:
                    break

            while True:
                number_of_relatives_value = number_of_relatives_var.get()
                if not number_of_relatives_value.isdigit():
                    messagebox.showerror("Invalid Input", "Ensure there are only numbers for number of relatives")
                    return
                else:
                    break

            total_family_size = 1 + int(number_of_relatives_value)
            selected_camp_id = str(camp_ID_var.get())

            camp_availability = camps_df.loc[camps_df['camp_id'].astype(str) == selected_camp_id, 'current_availability'].iloc[0]
            if total_family_size > camp_availability:
                messagebox.showerror("Exceeded Capacity",
                                     "Adding this refugee and their relatives will exceed the camp's capacity. Please reduce the number of relatives or cancel.")
                return


            # Create a new DataFrame with the user's input, and append it to the existing data
            new_data = pd.DataFrame({
                'Refugee_ID': [refugee_ID_var.get()],
                'Camp_ID': [camp_ID_var.get()],
                'First_name': [first_name_value],
                'Last_name': [last_name_value],
                'Gender': [gender_value],

                # 'Profile_ID': [int(profile_ID_var.get())],
                'Medical_Condition': [medical_condition_value],
                'Lead_Family_Member': [lead_family_member_value],
                'Lead_Phone_Number': [lead_phone_number_value],
                'Number_of_Relatives': [number_of_relatives_value]
            })

            try:
                existing_data = pd.read_csv(csv_filename)
                # existing_data['Profile_ID'] = existing_data['Profile_ID'].astype(int)
                updated_data = pd.concat([existing_data, new_data], ignore_index=True)
            except pd.errors.EmptyDataError:
                updated_data = new_data


            # Update the camps_df DataFrame with the new refugee information
            selected_camp_id = str(camp_ID_var.get())
            selected_camp_row = camps_df[camps_df['camp_id'].astype(str) == selected_camp_id]
            # Increment refugees_number and decrement max_capacity
            camps_df.loc[camps_df['camp_id'].astype(str) == selected_camp_id, 'refugees_number'] += (1 + int(number_of_relatives_value))
            camps_df.loc[camps_df['camp_id'].astype(str) == selected_camp_id, 'current_availability'] -= (1 + int(number_of_relatives_value))
            camps_df.to_csv(camp_csv, index=False)

            updated_data.to_csv(csv_filename, index=False)
            messagebox.showinfo("Adding Refugee",
                                f"New refugee information appended to {csv_filename}.")

            input_window.destroy()
            self.master.deiconify()

        # Create StringVar for each entry
        # refugee_ID_var = tk.StringVar(value=str(random_refugee_id))
        # camp_ID_var = tk.StringVar()
        first_name_var = tk.StringVar()
        last_name_var = tk.StringVar()
        gender_var = tk.StringVar()

        # profile_ID_var = tk.StringVar(value=str(random_profile_id))
        medical_condition_var = tk.StringVar()
        lead_family_member_var = tk.StringVar()
        lead_phone_number_var = tk.StringVar()
        number_of_relatives_var = tk.StringVar()

        label_x = 150  
        entry_x = 350  
        label_y = 150  # Adjust the initial y-coordinate
        y_increment = 40  # Adjust the y-increment for the next label and entry

        tk.Label(input_window, text="Camp ID:", bg=bg_color, fg="white", font=("Calibri", 14)).place(x=label_x,
                                                                                                     y=label_y)

        camp_ID_var = tk.StringVar()
        camp_dropdown = ttk.Combobox(input_window, textvariable=camp_ID_var, values=available_camp_ids, state='readonly')
        camp_dropdown.config(width=18)  # Adjust the width as needed
        camp_dropdown.place(x=entry_x, y=label_y)
        # Increment y-coordinate for the next label and entry
        label_y += y_increment

        tk.Label(input_window, text="First Name:", bg=bg_color, fg="white", font=("Calibri", 14)).place(x=label_x,
                                                                                                        y=label_y)
        tk.Entry(input_window, textvariable=first_name_var).place(x=entry_x, y=label_y)
        label_y += y_increment

        tk.Label(input_window, text="Last Name:", bg=bg_color, fg="white", font=("Calibri", 14)).place(x=label_x,
                                                                                                       y=label_y)
        tk.Entry(input_window, textvariable=last_name_var).place(x=entry_x, y=label_y)
        label_y += y_increment

        tk.Label(input_window, text="Gender:", bg=bg_color, fg="white", font=("Calibri", 14)).place(x=label_x,
                                                                                                    y=label_y)
        tk.Entry(input_window, textvariable=gender_var).place(x=entry_x, y=label_y)
        label_y += y_increment

        tk.Label(input_window, text="Volunteer ID:", bg=bg_color, fg="white", font=("Calibri", 14)).place(x=label_x,
                                                                                                          y=label_y)


        tk.Label(input_window, text="Medical Condition:", bg=bg_color, fg="white", font=("Calibri", 14)).place(
            x=label_x,
            y=label_y)
        tk.Entry(input_window, textvariable=medical_condition_var).place(x=entry_x, y=label_y)
        label_y += y_increment

        tk.Label(input_window, text="Lead Family Member:", bg=bg_color, fg="white", font=("Calibri", 14)).place(
            x=label_x,
            y=label_y)
        tk.Entry(input_window, textvariable=lead_family_member_var).place(x=entry_x, y=label_y)
        label_y += y_increment

        tk.Label(input_window, text="Lead Phone Number:", bg=bg_color, fg="white", font=("Calibri", 14)).place(
            x=label_x,
            y=label_y)
        tk.Entry(input_window, textvariable=lead_phone_number_var).place(x=entry_x, y=label_y)
        label_y += y_increment

        tk.Label(input_window, text="Number of Relatives:", bg=bg_color, fg="white", font=("Calibri", 14)).place(
            x=label_x,
            y=label_y)
        tk.Entry(input_window, textvariable=number_of_relatives_var).place(x=entry_x, y=label_y)

        tk.Button(input_window, text="Submit", command=process_input,
                  font=("Calibri", 12),
                  width=16,
                  height=1,
                  bg="#FFFFFF",
                  fg="black",
                  cursor="hand2",
                  activebackground="#B8B8B8",
                  activeforeground="black").place(x=entry_x, y=label_y + 2 * y_increment)

        tk.Button(input_window, text="Go Back", command=lambda: back(input_window),
                  font=("Calibri", 12),
                  width=16,
                  height=1,
                  bg="#FFFFFF",
                  fg="black",
                  cursor="hand2",
                  activebackground="#B8B8B8",
                  activeforeground="black").place(x=label_x, y=label_y + 2 * y_increment)

    def get_valid_input(self, title, prompt, validator, error_message):
        while True:
            user_input = simpledialog.askstring(title, prompt)
            if user_input is None:
                # User clicked Cancel
                return None

            if validator(user_input):
                return user_input
            else:
                messagebox.showerror("Invalid Input", error_message)

    def edit_refugee(self):
        self.view_database()  # Display the DataFrame
        while True:
            refugee_id_to_edit = simpledialog.askinteger("Edit Refugee",
                                                         "Enter the Refugee ID you want to edit (or 'cancel' to exit):")
            if refugee_id_to_edit is None:
                messagebox.showinfo("Edit Refugee", "Command cancelled")
                return

            else:
                break

        while True:
            if int(refugee_id_to_edit) not in refugee_df["Refugee_ID"].values:
                # Create a custom error dialog
                error_dialog = tk.Toplevel(self.master)
                error_dialog.title("Error")
                error_dialog.geometry("200x60")
                error_label = tk.Label(error_dialog, text="Refugee does not exist")
                error_label.pack()

                # Add an OK button to close the error dialog
                ok_button = tk.Button(error_dialog, text="OK", command=error_dialog.destroy)
                ok_button.pack()

                # Center the error dialog
                error_dialog.geometry("+{}+{}".format(
                    int(self.master.winfo_x() + (self.master.winfo_width() - error_dialog.winfo_reqwidth()) / 2),
                    int(self.master.winfo_y() + (self.master.winfo_height() - error_dialog.winfo_reqheight()) / 2)
                ))

                # Run the Tkinter event loop until the error dialog is closed
                self.master.wait_window(error_dialog)

                answer = simpledialog.askstring("Edit Refugee", "Would you like to still edit another refugee? ")
                if answer.lower() == 'yes':
                    while True:
                        refugee_id_to_edit = simpledialog.askinteger("Edit Refugee",
                                                                         "Enter the Refugee ID you want to edit (or 'cancel' to exit):")
                        if refugee_id_to_edit in refugee_df["Refugee_ID"].values:
                            break

                        if refugee_id_to_edit is None:
                            return

                        else:
                            messagebox.showerror("Refugee still does not exist, please try again")

                elif answer.lower() == 'no':
                    confirm_cancel = messagebox.askokcancel("Edit refugee", "Are you sure you want to cancel?")
                    if confirm_cancel:
                        return

                else:
                    messagebox.showerror("Edit refugee", "Invalid input, ensure it's either a yes or no")

            else:
                break

        original_camp_id = refugee_df.loc[refugee_df['Refugee_ID'] == int(refugee_id_to_edit), 'Camp_ID'].values[0]

        fields = [
            'Camp ID', 'First name', 'Last name', 'Gender', 'Volunteer ID',
            'Medical Condition', 'Lead Family Member', 'Lead Phone Number', 'Number of Relatives'
        ]

        field_window = tk.Toplevel(self.master)
        field_window.title("Select Field to Edit")
        window_width = 700
        window_height = 800
        field_window['bg'] = bg_color
        # Get screen width and height
        screen_width = field_window.winfo_screenwidth()
        screen_height = field_window.winfo_screenheight()

        # Calculate the x and y coordinates for the main window to be centered
        x = (screen_width - window_width) // 2  # Adjust 500 based on the width of your window
        y = (screen_height - window_height) // 2  # Adjust 300 based on the height of your window

        # Set the geometry of the main window
        field_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        field_var = tk.StringVar()
        field_var.set(fields[0])  # Set the default value

        field_label = tk.Label(field_window, text="Select Field to Edit:", bg=bg_color, fg="white",
                               font=("Calibri", 14))
        field_label.pack(pady=(275, 10))

        field_dropdown = ttk.Combobox(field_window, textvariable=field_var, values=fields, state="readonly")
        field_dropdown.pack(pady=10)

        ok_button = tk.Button(field_window, text="OK", command=field_window.destroy, font=("Calibri", 12),
        width=16,
        height=0,
        bg="#FFFFFF",
        fg="black",
        cursor="hand2",
        activebackground="#B8B8B8",
        activeforeground="black")
        ok_button.pack(pady=10)

        field_window.wait_window()  # Wait for the window to be closed

        selected_field = field_var.get()

        if selected_field.lower() == 'done':
            return

        new_value = self.edit_field(selected_field, refugee_id_to_edit)

        if new_value is not None:
            refugee_df.loc[
                refugee_df['Refugee_ID'] == int(refugee_id_to_edit), selected_field.replace(" ", "_")] = new_value
            refugee_df.to_csv(csv_filename, index=False)

            new_camp_id = new_value if selected_field == 'Camp ID' else original_camp_id
            self.update_camp_info(original_camp_id, new_camp_id, int(refugee_id_to_edit))

        field_window.update()
        field_window.destroy()
        

        messagebox.showinfo("Edit Refugee",
                            f"Refugee information updated for Refugee ID {refugee_id_to_edit}.")

    def update_camp_info(self, original_camp_id, new_camp_id, refugee_id):
        original_camp_id = str(original_camp_id).strip()
        new_camp_id = str(new_camp_id).strip()

        number_of_relatives = int(refugee_df.loc[refugee_df['Refugee_ID'] == refugee_id, 'Number_of_Relatives'].iloc[0])
        total_family_size = 1 + number_of_relatives
        if original_camp_id != new_camp_id:
            # Increment refugees_number and decrement current_availability for the original camp ID
            camps_df.loc[camps_df['camp_id'].astype(str) == original_camp_id, 'refugees_number'] -= total_family_size
            camps_df.loc[camps_df['camp_id'].astype(str) == original_camp_id, 'current_availability'] += total_family_size

            # Increment refugees_number and decrement current_availability for the new camp ID
            camps_df.loc[camps_df['camp_id'].astype(str) == new_camp_id, 'refugees_number'] += total_family_size
            camps_df.loc[camps_df['camp_id'].astype(str) == new_camp_id, 'current_availability'] -= total_family_size

            camps_df.to_csv(camp_csv, index=False)


    def edit_field(self, field_name, refugee_id):
        root = tk.Tk()
        root.withdraw()  

        new_value = None

        if field_name == 'Camp ID':
            camp_window = tk.Toplevel(self.master)
            camp_window.title("Edit Refugee")

            camp_window.geometry("300x150")
            camp_window.title("Choose Camp")

            label = tk.Label(camp_window, text="Choose the camp you'd like to assign the refugee:")
            label.pack(pady=10)

            number_of_relatives = int(refugee_df.loc[refugee_df['Refugee_ID'] == refugee_id, 'Number_of_Relatives'].iloc[0])
            total_family_size = 1 + number_of_relatives

            available_camps_with_availability = camps_df[camps_df['current_availability'] > total_family_size]
            available_camp_ids = available_camps_with_availability['camp_id'].tolist()

            if not available_camp_ids:
                messagebox.showerror("No Available Camps",
                                     "There are no camps with available space. Please add more camps.")
                camp_window.destroy()
                self.master.deiconify()
                return

            camp_ID_var_edit = tk.StringVar()
            camp_ID_var_edit.set(available_camp_ids[0])  # Set the default value

            camp_dropdown = ttk.Combobox(camp_window, textvariable=camp_ID_var_edit, values=available_camp_ids, state="readonly")
            camp_dropdown.pack(pady=10)

            def submit():
                nonlocal new_value
                new_value = camp_ID_var_edit.get()
                camp_window.destroy()

            def cancel():
                nonlocal new_value
                new_value = None
                camp_window.destroy()

            submit_button = tk.Button(camp_window, text="Submit", command=submit)
            submit_button.pack(side=tk.LEFT, padx=10)

            cancel_button = tk.Button(camp_window, text="Cancel", command=cancel)
            cancel_button.pack(side=tk.RIGHT, padx=10)

            camp_window.wait_window()

            # new_value = camp_ID_var_edit.get()
            camp_window.destroy()
            # new_value = simpledialog.askinteger("Edit Camp ID",
            #                                         f"Enter the new {field_name} (or 'cancel' to keep current value):")
            if new_value is not None:
                new_value = new_value

        elif field_name == 'First name':
            while True:
                new_value = simpledialog.askstring("Edit First Name",
                                                       f"Enter the new {field_name} (or press cancel to keep the current value):")
                if new_value is not None and new_value.isalpha():
                    new_value = new_value.capitalize()
                    break

                elif not new_value.isalpha():
                    messagebox.showerror("Edit First Name",
                                         "Invalid input, ensure there are no spaces, numbers or special characters")


        elif field_name == 'Last name':
            while True:
                new_value = simpledialog.askstring("Edit Last Name",
                                                   f"Enter the new {field_name} (or press cancel to keep the current value):").lower()

                if new_value is not None and new_value.isalpha():
                    new_value = new_value.capitalize()
                    break

                elif not new_value.isalpha():
                    messagebox.showerror("Edit Last Name",
                                         "Invalid input, ensure there are no numbers or special characters and spaces")


        elif field_name == 'Gender':
            while True:
                new_value = simpledialog.askstring("Edit Gender",
                                                       f"Enter the new {field_name} (or press cancel to keep the current value):").lower()
                if new_value is not None and new_value.capitalize() in ["Male", "Female", "Other"]:
                    new_value = new_value.capitalize()
                    break
                else:
                    messagebox.showerror("Edit Gender", "Invalid input, ensure it's either Male, Female or Other")

        elif field_name == 'Volunteer ID':
            new_value = simpledialog.askinteger("Edit Volunteer ID",
                                                f"Enter your {field_name} (or press cancel to keep the current value):")
            if new_value is not None:
                new_value = new_value
        #
        # elif field_name == 'Profile ID':
        #     new_value = simpledialog.askinteger("Edit Profile ID",
        #                                         f"Enter your {field_name} (or press cancel to keep the current value):")

            if new_value is not None:
                new_value = new_value

        elif field_name == 'Medical Condition':
            new_value = simpledialog.askstring("Edit medical condition",
                                               f"Enter your {field_name} (or press cancel to keep the current condition):")

            if new_value is not None:
                new_value = new_value.capitalize()

        elif field_name == 'Lead Family Member':
            while True:
                new_value = simpledialog.askstring("Enter new Lead Family Member",
                                                   f"Enter your {field_name} (first name only) (or press cancel to keep the current Member):")

                if new_value is not None and new_value.isalpha():
                    new_value = new_value.capitalize()
                    break

                elif not new_value.isalpha():
                    messagebox.showerror("Enter new Lead Family Member (",
                                         "Invalid input, ensure lead family member only has letters and no spaces")

        elif field_name == 'Lead Phone Number':
            new_value = simpledialog.askinteger("Edit Lead Phone Number",
                                                f"Enter your {field_name} (or press cancel to keep the current Number):")

            if new_value is not None:
                new_value = new_value







        elif field_name == 'Number of Relatives':

            new_number_of_relatives = simpledialog.askinteger("Edit Number of Relatives",

                                                              f"Enter the new {field_name} for Refugee ID {refugee_id} (or press cancel to keep the current number):")

            if new_number_of_relatives is None:
                return None

            # Call the update_number_of_relatives function

            new_family_size = self.update_number_of_relatives(refugee_id, new_number_of_relatives)

            if new_family_size is None:
                # Show an error message if the camp cannot accommodate the new family size

                messagebox.showerror("Edit Number of Relatives",

                                     "The camp cannot accommodate the new family size. Please reduce the number or change the camp.")

                return None

            return new_number_of_relatives

        root.destroy() # Destroy the hidden root window
        return new_value

    # When updating the Number of Relatives
    def update_number_of_relatives(self, refugee_id, new_number_of_relatives):
        global refugee_df
        global camps_df

        # Reload the DataFrames to get the latest data
        refugee_df = pd.read_csv("Refugee_DataFrame.csv")
        camps_df = pd.read_csv("camps.csv")

        # Continue with the rest of the logic
        current_number_of_relatives = \
        refugee_df.loc[refugee_df['Refugee_ID'] == refugee_id, 'Number_of_Relatives'].iloc[0]
        original_family_size = 1 + current_number_of_relatives
        new_family_size = 1 + new_number_of_relatives
        difference_in_family_size = new_family_size - original_family_size

        refugee_camp_id = refugee_df.loc[refugee_df['Refugee_ID'] == refugee_id, 'Camp_ID'].iloc[0]

        # Update camps DataFrame and then write to CSV
        camps_df.loc[camps_df['camp_id'] == refugee_camp_id, 'refugees_number'] += difference_in_family_size
        camps_df.loc[camps_df['camp_id'] == refugee_camp_id, 'current_availability'] -= difference_in_family_size
        camps_df.to_csv("camps.csv", index=False)

        # Update refugee DataFrame and then write to CSV
        refugee_df.loc[refugee_df['Refugee_ID'] == refugee_id, 'Number_of_Relatives'] = new_number_of_relatives
        refugee_df.to_csv("Refugee_DataFrame.csv", index=False)

        return new_family_size

    def view_database(self):
        if not self.show_database:
            return
        global refugee_df
        refugee_df = pd.read_csv(csv_filename)
        database_window = tk.Toplevel(self.master)
        database_window.title("View Database")

        # Create a Text widget to show the database contents
        text_widget = tk.Text(database_window, wrap=tk.WORD)
        text_widget.pack(expand=True, fill="both")

        database_window.geometry('1300x400')

        # Insert the database contents into the Text widget
        text_widget.insert(tk.END, refugee_df.to_string(index=False))

        # Make the Text widget read-only
        text_widget.config(state=tk.DISABLED)

    def delete_refugee(self):
        self.view_database()
        while True:
            refugee_id_to_delete = simpledialog.askinteger("Delete Refugee",
                                                           "Enter the Refugee ID you want to delete (or 'cancel' to exit):")
            if refugee_id_to_delete is None:
                return  # User clicked Cancel

            if refugee_id_to_delete not in refugee_df["Refugee_ID"].values:
                messagebox.showerror("Delete Refugee", "Refugee does not exist")

            else:
                confirm_delete = messagebox.askokcancel("Delete Refugee", "Are you sure you want to delete this refugee?")
                if confirm_delete:
                    # Retrieve the camp ID of the refugee to be deleted
                    camp_id_to_update = refugee_df.loc[refugee_df['Refugee_ID'] == refugee_id_to_delete, 'Camp_ID'].values[0]
                    camp_id_to_update = str(camp_id_to_update).strip()

                    number_of_relatives = self.refugee_df.loc[self.refugee_df['Refugee_ID'] == refugee_id_to_delete, 'Number_of_Relatives'].values[0]
                    total_family_size = 1 + int(number_of_relatives)

                    # Decrement refugees_number and increment current_availability for the respective camp
                    camps_df.loc[camps_df['camp_id'].astype(str) == camp_id_to_update, 'refugees_number'] -= total_family_size
                    camps_df.loc[camps_df['camp_id'].astype(str) == camp_id_to_update, 'current_availability'] += total_family_size
                    camps_df.to_csv(camp_csv, index=False)

                    refugee_df.drop(refugee_df[refugee_df['Refugee_ID'] == refugee_id_to_delete].index, inplace=True)
                    refugee_df.to_csv(csv_filename, index=False)
                    messagebox.showinfo("Delete Refugee", f"Refugee ID {refugee_id_to_delete} deleted successfully.")
                    break


root = tk.Toplevel()

main_menu_window = MainMenuWindow(root)
root.mainloop()
