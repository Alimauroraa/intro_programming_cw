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



class MainMenuWindow:
    def __init__(self, master):
        self.master = master
        master.title("Refugee Portal")

        # Get screen width and height
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()

        # Calculate the x and y coordinates for the main window to be centered
        x = (screen_width - 550) // 2  # Adjust 500 based on the width of your window
        y = (screen_height - 600) // 2  # Adjust 300 based on the height of your window

        # Set the geometry of the main window
        master.geometry(f"600x600+{x}+{y}")

        self.label = tk.Label(master, text="Hello and welcome to the refugee portal!")
        self.label.pack()

        # Buttons for menu options
        self.add_button = tk.Button(master, text="Add a new refugee", command=self.add_refugee)
        self.add_button.pack()

        self.edit_button = tk.Button(master, text="Edit an existing refugee", command=self.edit_refugee)
        self.edit_button.pack()

        self.view_button = tk.Button(master, text="View the database", command=self.view_database)
        self.view_button.pack()

        self.delete_button = tk.Button(master, text="Delete a refugee", command=self.delete_refugee)
        self.delete_button.pack()

        self.show_database = True

        # self.view_details_button = tk.Button(master, text="View refugee's details", command=self.view_refugee_details)
        # self.view_details_button.pack()

        self.exit_button = tk.Button(master, text="Exit the program", command=self.master.destroy)
        self.exit_button.pack()

    def add_refugee(self):
        self.master.iconify()
        # Create a new window for input
        input_window = tk.Toplevel(self.master)
        input_window.title("Add New Refugee")

        while True:
            random_refugee_id = random.randint(1, 9999)

            # Check if the generated ID is not already in the DataFrame
            if random_refugee_id not in refugee_df["Refugee_ID"].values:
                refugee_ID_var = tk.StringVar(value=str(random_refugee_id))
                break

        while True:
            random_profile_id = random.randint(1, 999)

            if random_profile_id not in refugee_df["Profile_ID"].values:
                profile_ID_var = tk.StringVar(value=str(random_profile_id))
                break

        available_camp_ids = camps_df['Camp ID'].tolist()


        camp_ID_var = tk.StringVar()
        camp_ID_var.set(available_camp_ids[0])  # Set the default value

        def back(input_window):
            input_window.destroy()
            self.master.deiconify()

        # Function to validate and process the entered data
        def process_input():
            # Your input validation logic goes here
            # For simplicity, I'm only checking if the fields are not empty
            while True:
                if not first_name_var.get() or not last_name_var.get() \
                        or not gender_var.get() or not volunteer_ID_var.get() or not medical_condition_var.get() \
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

            while True:
                volunteer_ID_value = volunteer_ID_var.get()
                if not volunteer_ID_value.isdigit():
                    messagebox.showerror("Invalid Input", "Ensure volunteer ID is number")
                    return
                else:
                    break

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
                    messagebox.showerror("Invalid Input", "Ensure there are no letters, only numbers")
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


            # Create a new DataFrame with the user's input, and append it to the existing data
            new_data = pd.DataFrame({
                'Refugee_ID': [refugee_ID_var.get()],
                'Camp_ID': [camp_ID_var.get()],
                'First_name': [first_name_value],
                'Last_name': [last_name_value],
                'Gender': [gender_value],
                'Volunteer_ID': [volunteer_ID_value],
                'Profile_ID': [int(profile_ID_var.get())],
                'Medical_Condition': [medical_condition_value],
                'Lead_Family_Member': [lead_family_member_value],
                'Lead_Phone_Number': [lead_phone_number_value],
                'Number_of_Relatives': [number_of_relatives_value]
            })

            try:
                existing_data = pd.read_csv(csv_filename)
                existing_data['Profile_ID'] = existing_data['Profile_ID'].astype(int)
                updated_data = pd.concat([existing_data, new_data], ignore_index=True)
            except pd.errors.EmptyDataError:
                updated_data = new_data

            updated_data.to_csv(csv_filename, index=False)
            messagebox.showinfo("Adding Refugee",
                                f"New refugee information appended to {csv_filename}. Please reopen application to view changes")
            input_window.destroy()
            self.master.deiconify()

        # Create StringVar for each entry
        refugee_ID_var = tk.StringVar(value=str(random_refugee_id))
        # camp_ID_var = tk.StringVar()
        first_name_var = tk.StringVar()
        last_name_var = tk.StringVar()
        gender_var = tk.StringVar()
        volunteer_ID_var = tk.StringVar()
        profile_ID_var = tk.StringVar(value=str(random_profile_id))
        medical_condition_var = tk.StringVar()
        lead_family_member_var = tk.StringVar()
        lead_phone_number_var = tk.StringVar()
        number_of_relatives_var = tk.StringVar()


        # tk.Label(input_window, text="Camp ID:").grid(row=1, column=0)
        # tk.Entry(input_window, textvariable=camp_ID_var).grid(row=1, column=1)

        tk.Label(input_window, text="Camp ID:").grid(row=1, column=0)

        camp_dropdown = ttk.Combobox(input_window, textvariable=camp_ID_var, values=available_camp_ids, state="readonly")
        camp_dropdown.grid(row=1, column=1)

        tk.Label(input_window, text="First Name:").grid(row=2, column=0)
        tk.Entry(input_window, textvariable=first_name_var).grid(row=2, column=1)

        tk.Label(input_window, text="Last Name:").grid(row=3, column=0)
        tk.Entry(input_window, textvariable=last_name_var).grid(row=3, column=1)

        tk.Label(input_window, text="Gender:").grid(row=4, column=0)
        tk.Entry(input_window, textvariable=gender_var).grid(row=4, column=1)

        tk.Label(input_window, text="Volunteer ID:").grid(row=5, column=0)
        tk.Entry(input_window, textvariable=volunteer_ID_var).grid(row=5, column=1)

        tk.Label(input_window, text="Medical Condition:").grid(row=7, column=0)
        tk.Entry(input_window, textvariable=medical_condition_var).grid(row=7, column=1)

        tk.Label(input_window, text="Lead Family Member:").grid(row=8, column=0)
        tk.Entry(input_window, textvariable=lead_family_member_var).grid(row=8, column=1)

        tk.Label(input_window, text="Lead Phone Number:").grid(row=9, column=0)
        tk.Entry(input_window, textvariable=lead_phone_number_var).grid(row=9, column=1)

        tk.Label(input_window, text="Number of Relatives:").grid(row=10, column=0)
        tk.Entry(input_window, textvariable=number_of_relatives_var).grid(row=10, column=1)

        # Button to submit the data
        tk.Button(input_window, text="Submit", command=process_input).grid(row=11, column=1, columnspan=1)
        tk.Button(input_window, text="Go Back", command=lambda: back(input_window)).grid(row=11, column=0, columnspan=1)

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

        fields = [
            'Camp ID', 'First name', 'Last name', 'Gender', 'Volunteer ID', 'Profile ID',
            'Medical Condition', 'Lead Family Member', 'Lead Phone Number', 'Number of Relatives'
        ]

        field_window = tk.Toplevel(self.master)
        field_window.title("Select Field to Edit")


        # Get screen width and height
        screen_width = field_window.winfo_screenwidth()
        screen_height = field_window.winfo_screenheight()

        # Calculate the x and y coordinates for the main window to be centered
        x = (screen_width - 550) // 2  # Adjust 500 based on the width of your window
        y = (screen_height - 550) // 2  # Adjust 300 based on the height of your window

        # Set the geometry of the main window
        field_window.geometry(f"500x300+{x}+{y}")

        field_var = tk.StringVar()
        field_var.set(fields[0])  # Set the default value

        field_label = tk.Label(field_window, text="Select Field to Edit:")
        field_label.pack()

        field_dropdown = ttk.Combobox(field_window, textvariable=field_var, values=fields, state="readonly")
        field_dropdown.pack()

        ok_button = tk.Button(field_window, text="OK", command=field_window.destroy)
        ok_button.pack()

        field_window.wait_window()  # Wait for the window to be closed

        selected_field = field_var.get()

        if selected_field.lower() == 'done':
            return

        new_value = self.edit_field(selected_field)

        if new_value is not None:
            refugee_df.loc[
                refugee_df['Refugee_ID'] == int(refugee_id_to_edit), selected_field.replace(" ", "_")] = new_value
            refugee_df.to_csv(csv_filename, index=False)

        field_window.update()
        field_window.destroy()
        

        messagebox.showinfo("Edit Refugee",
                            f"Refugee information updated for Refugee ID {refugee_id_to_edit}. Please reopen the application to view the changes.")



    def edit_field(self, field_name):
        root = tk.Tk()
        root.withdraw()  # Hide the main window

        new_value = None

        if field_name == 'Camp ID':
            camp_window = tk.Toplevel(self.master)
            camp_window.title("Edit Refugee")

            camp_window.geometry("300x150")
            camp_window.title("Choose Camp")

            label = tk.Label(camp_window, text="Choose the camp you'd like to assign the refugee:")
            label.pack(pady=10)



            available_camp_ids = camps_df['Camp ID'].tolist()

            camp_ID_var_edit = tk.StringVar()
            camp_ID_var_edit.set(available_camp_ids[0])  # Set the default value

            camp_dropdown = ttk.Combobox(camp_window, textvariable=camp_ID_var_edit, values=available_camp_ids, state="readonly")
            camp_dropdown.pack(pady=10)

            def submit():
                global new_value
                new_value = camp_ID_var_edit.get()
                camp_window.destroy()

            # Function to handle the Cancel button click
            def cancel():
                global new_value
                new_value = None
                camp_window.destroy()

            # Add Submit and Cancel buttons
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

        elif field_name == 'Profile ID':
            new_value = simpledialog.askinteger("Edit Profile ID",
                                                f"Enter your {field_name} (or press cancel to keep the current value):")

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
                                         "Invalid input, ensure it only has letters and no spaces")

        elif field_name == 'Lead Phone Number':
            new_value = simpledialog.askinteger("Edit Lead Phone Number",
                                                f"Enter your {field_name} (or press cancel to keep the current Number):")

            if new_value is not None:
                new_value = new_value

        elif field_name == 'Number of Relatives':
            new_value = simpledialog.askinteger("Edit Number of Relatives",
                                                f"Enter your {field_name} (or press cancel to keep the current Number):")

            if new_value is not None:
                new_value = new_value

        root.destroy() # Destroy the hidden root window
        return new_value







    def view_database(self):
        if not self.show_database:
            return

        database_window = tk.Toplevel(self.master)
        database_window.title("View Database")

        # Create a Text widget to show the database contents
        text_widget = tk.Text(database_window, wrap=tk.WORD)
        text_widget.pack(expand=True, fill="both")

        database_window.geometry('1200x400')

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
                    refugee_df.drop(refugee_df[refugee_df['Refugee_ID'] == refugee_id_to_delete].index, inplace=True)
                    refugee_df.to_csv(csv_filename, index=False)
                    messagebox.showinfo("Delete Refugee", f"Refugee ID {refugee_id_to_delete} deleted successfully.")
                    break


root = tk.Tk()
main_menu_window = MainMenuWindow(root)
root.mainloop()

# # Path to the CSV file
# csv_filename = 'Refugee_DataFrame.csv'
#
# # Read the CSV file into a DataFrame
# refugee_df = pd.read_csv(csv_filename)
#
# # Greeting function
# def greeting():
#     print("Hello and welcome to the refugee portal! Please type in what you'd like to do based on the following options: \n1. Add a new refugee \n2. Edit an existing refugee \n3. View the database \n4. View refugee's details \n5. Exit the program")
# # Display the DataFrame
# def display_csv():
#     print(refugee_df.to_string())
#
# def view_refugee_by_id():
#     while True:
#         refugee_id_number = input("Enter Refugee ID number of whom you want to see the associated details of, or press enter to cancel: ")
#         if refugee_id_number == '':
#             print("Returning to menu")
#             return
#         elif refugee_id_number.isdigit():
#             refugee_id_number = int(refugee_id_number)
#             break
#         else:
#             print("Invalid ID, ensure it only has numbers: ")
#
#     if refugee_id_number in refugee_df["Refugee_ID"].values:
#         print(refugee_df[refugee_df['Refugee_ID'] == refugee_id_number].to_string(index=False))
#     else:
#         print("Refugee not found.")
#
#
# def main_menu():
#     while True:
#         greeting()
#         choice = input("Enter your choice (1, 2, 3, 4, 5): ")
#
#         if choice == '1':
#             append_to_csv(csv_filename)
#         elif choice == '2':
#             edit_refugee()
#         elif choice == '3':
#             display_csv()
#         elif choice == '4':
#             view_refugee_by_id()
#         elif choice == '5':
#             print("Have a good day!")
#             break
#         else:
#             print("Invalid choice. Please enter 1, 2, 3, 4 or 5.")
#
# def append_to_csv(file_name):
#     # Prompt user for new refugee information
#     while True: # Enables a consistent loop
#         answer = input("Would you like to add a new refugee? ").lower() # Takes input from user, automatically converts to lowercase to make the if loops easier
#         if answer == "yes":
#             while True:
#                 refugee_ID = input("Enter the new Refugee's ID: ")
#                 if refugee_ID.isdigit():
#                     break
#                 else:
#                     print("Invalid Refugee ID number, ensure it only consists of numbers: ")
#
#             while True:
#                 camp_ID = input("Enter the new Camp's ID: ")
#                 if camp_ID.isdigit():
#                     break
#                 else:
#                     print("Invalid camp ID number, ensure it is only numbers: ")
#
#             while True:
#                 first_name = input("Enter the new Refugee's First Name: ")
#                 if first_name.isalpha():
#                     break
#                 else:
#                     print("Invalid first name. Ensure it has no special characters and numbers: ")
#
#             while True:
#                 last_name = input("Enter the new Refugee's Last Name: ")
#                 if last_name.isalpha():
#                     break
#                 else:
#                     print("Invalid last name. Ensure it has no special characters and numbers:")
#
#             while True:
#                 gender = input("Enter the new Refugee's Gender: ")
#                 if gender.isalpha():
#                     break
#                 else:
#                     print("Invalid gender, ensure it has no numbers or special characters: ")
#
#             while True:
#                 volunteer_ID = input("Enter the new Volunteer's ID: ")
#                 if volunteer_ID.isdigit():
#                     break
#                 else:
#                     print("Invalid volunteer ID. Ensure it only has numbers and no letters")
#
#             while True:
#                 profile_ID = input("Enter the new Profile ID: ")
#                 if profile_ID.isdigit():
#                     break
#                 else:
#                     print("Invalid Profile ID. Ensure it has only numbers and no letters")
#
#             medical_condition = input("Enter the new Medical Condition: ")
#
#             while True:
#                 lead_family_member = input("Enter the new Lead Family Member: ")
#                 if lead_family_member.isalpha():
#                     break
#                 else:
#                     print("Invalid name. Ensure it has no numbers or special characters: ")
#
#             while True:
#                 lead_phone_number = input("Enter the new Lead Phone Number: ")
#                 if lead_phone_number.isdigit():
#                     break
#                 else:
#                     print("Invalid phone number, ensure it only consists of numbers: ")
#
#             while True:
#                 number_of_relatives = input("Enter the new Number of Relatives: ")
#                 if number_of_relatives.isdigit():
#                     break
#                 else:
#                     print("Invalid number of relatives, ensure it only consists of numbers: ")
#
#             # Create a new DataFrame with the user's input
#             new_data = pd.DataFrame({
#                 'Refugee_ID': [refugee_ID],
#                 'Camp_ID': [camp_ID],
#                 'First_name': [first_name],
#                 'Last_name': [last_name],
#                 'Gender': [gender],
#                 'Volunteer_ID': [volunteer_ID],
#                 'Profile_ID': [profile_ID],
#                 'Medical_Condition': [medical_condition],
#                 'Lead_Family_Member': [lead_family_member],
#                 'Lead_Phone_Number': [lead_phone_number],
#                 'Number_of_Relatives': [number_of_relatives]
#             })
#
#             # Read the existing data and append the new data
#             try:
#                 existing_data = pd.read_csv(file_name)
#                 updated_data = pd.concat([existing_data, new_data], ignore_index=True)
#             except pd.errors.EmptyDataError:
#                 updated_data = new_data
#
#             # Write the updated DataFrame back to the CSV
#             updated_data.to_csv(file_name, index=False)
#             print(f"New refugee information appended to {file_name}.")
#             break
#         # If user decides no, this code below will skip this function
#         elif answer == "no":
#             print("Have a nice day!")
#             break
#         # If invalid response, the while loop will allow the user to reinput the info
#         else:
#             print("Invalid response. Please enter 'yes' or 'no'.")
#
# def edit_refugee():
#     display_csv()
#
#     while True:
#         refugee_id_to_edit = input("Enter the Refugee ID you want to edit (or 'cancel' to exit): ")
#         if refugee_id_to_edit.lower() == 'cancel':
#             print("Edit canceled.")
#             return
#         elif refugee_id_to_edit.isdigit():
#             break
#         else:
#             print("Invalid Refugee ID. Please enter a valid number.")
#
#     while True:
#         if int(refugee_id_to_edit) not in refugee_df["Refugee_ID"].values:
#             print("Refugee does not exist")
#
#             answer = input("Would you like to still edit another refugee? ")
#             if answer.lower() == 'yes':
#                 edit_refugee()
#                 return
#
#
#             elif answer.lower() == 'no':
#                 print("Have a good day!")
#                 return
#
#             else:
#                 print("Invalid response, either say yes or no")
#
#         else:
#             break
#
#
#     print(refugee_df[refugee_df['Refugee_ID'] == int(refugee_id_to_edit)].to_string(index=False))
#
#     while True:
#         answer = input("Which field do you wish to edit: \nCamp ID \nFirst name \nLast name \nGender \nVolunteer ID \nProfile ID \nMedical Condition \nLead Family Member \nLead Phone Number \nNumber of Relatives \nShould you wish to exit and save any changes, type 'Done'. ").lower().replace(" ", "_")
#         if answer == 'done':
#             break
#
#         elif answer == 'first_name':
#             while True:
#                 new_first_name = input("Enter the new First Name (or press Enter to keep the current value): ")
#                 if new_first_name == '':
#                     break
#                 elif new_first_name.isalpha():
#                     new_first_name = new_first_name.capitalize()
#                     break
#                 else:
#                     print("Invalid first name. Ensure it has no special characters and numbers: ")
#
#             if new_first_name != '':
#                 refugee_df.loc[refugee_df['Refugee_ID'] == int(refugee_id_to_edit), 'First_name'] = new_first_name
#
#         elif answer == 'camp_id':
#             while True:
#                 new_camp_id = input("Enter the new Camp ID (or press Enter to keep the current value): ")
#                 if new_camp_id == '':
#                     break
#                 elif new_camp_id.isdigit():
#                     break
#                 else:
#                     print("Invalid Camp ID. Ensure it has only numbers: ")
#
#             if new_camp_id != '':
#                 refugee_df.loc[refugee_df['Refugee_ID'] == int(refugee_id_to_edit), 'Camp_ID'] = int(new_camp_id)
#
#         elif answer == 'last_name':
#             while True:
#                 new_last_name = input("Enter the new Last Name (or press Enter to keep the current value): ")
#                 if new_last_name == '':
#                     break
#                 elif new_last_name.isalpha():
#                     new_last_name = new_last_name.capitalize()
#                     break
#                 else:
#                     print("Invalid last name. Ensure it has no special characters and numbers: ")
#
#             if new_last_name != '':
#                 refugee_df.loc[refugee_df['Refugee_ID'] == int(refugee_id_to_edit), 'Last_name'] = new_last_name
#
#         elif answer == 'gender':
#             while True:
#                 new_gender = input("Enter new gender, or press Enter to keep current value: ").capitalize()
#                 if new_gender == '':
#                     break
#                 elif new_gender.isalpha() and new_gender in ['Male', 'Female', 'Undisclosed']:
#                     break
#                 else:
#                     print("Invalid gender. Ensure it has no special characters and numbers and that it is either male, female or undisclosed: ")
#
#             if new_gender != '':
#                 refugee_df.loc[refugee_df['Refugee_ID'] == int(refugee_id_to_edit), 'Gender'] = new_gender
#
#         elif answer == 'volunteer_id':
#             while True:
#                 new_volunteer_id = input("Enter the new Volunteer ID, or press Enter to keep current value: ")
#                 if new_volunteer_id == '':
#                     break
#                 elif new_volunteer_id.isdigit():
#                     break
#                 else:
#                     print("Invalid volunteer ID. Ensure it only has numbers: ")
#
#             if new_volunteer_id != '':
#                 refugee_df.loc[refugee_df['Refugee_ID'] == int(refugee_id_to_edit), 'Volunteer_ID'] = new_volunteer_id
#
#         elif answer == "profile_id":
#             while True:
#                 new_profile_id = input("Enter the new Profile ID, or press Enter to keep current value: ")
#                 if new_profile_id == '':
#                     break
#                 elif new_profile_id.isdigit():
#                     break
#                 else:
#                     print("Invalid profile ID. Ensure it only has numbers: ")
#
#             if new_profile_id != '':
#                 refugee_df.loc[refugee_df['Refugee_ID'] == int(refugee_id_to_edit), 'Profile_ID'] = new_profile_id
#
#         elif answer == 'medical_condition':
#             new_medical_condition = input("Enter new medical condition, or press Enter to keep current condition(s): ")
#             new_medical_condition = new_medical_condition.capitalize()
#             if new_medical_condition != '':
#                 refugee_df.loc[refugee_df['Refugee_ID'] == int(refugee_id_to_edit), 'Medical_Condition'] = new_medical_condition
#
#         elif answer == 'lead_family_member':
#             while True:
#                 new_lead_family_member = input("Enter new lead family member, or press Enter to keep current lead: ")
#                 if new_lead_family_member == '':
#                     break
#                 elif new_lead_family_member.isalpha():
#                     new_lead_family_member = new_lead_family_member.capitalize()
#                     break
#                 else:
#                     print("Invalid name, please ensure it has no numbers or special characters: ")
#             if new_lead_family_member != '':
#                 refugee_df.loc[refugee_df['Refugee_ID'] == int(refugee_id_to_edit), 'Lead_Family_Member'] = new_lead_family_member
#
#         elif answer == 'lead_phone_number':
#             while True:
#                 new_lead_phone_number = input("Enter new lead phone number, or press Enter to keep current number: ")
#                 if new_lead_phone_number == '':
#                     break
#                 elif new_lead_phone_number.isdigit():
#                     break
#                 else:
#                     print("Invalid phone number, ensure it consists of only numbers: ")
#
#             if new_lead_phone_number != '':
#                 refugee_df.loc[refugee_df['Refugee_ID'] == int(refugee_id_to_edit), 'Lead_Phone_Number'] = new_lead_phone_number
#
#         elif answer == 'number_of_relatives':
#             while True:
#                 new_number_of_relatives = input("Enter new number of relatives, or press Enter to keep current number: ")
#                 if new_number_of_relatives == '':
#                     break
#                 elif new_number_of_relatives.isdigit():
#                     break
#                 else:
#                     print("Invalid number, please ensure there are no letters or special characters: ")
#
#             if new_number_of_relatives != '':
#                 refugee_df.loc[refugee_df['Refugee_ID'] == int(refugee_id_to_edit), 'Number_of_Relatives'] = new_number_of_relatives
#
#     refugee_df.to_csv(csv_filename, index=False)
#     print(f"Refugee information updated for Refugee ID {refugee_id_to_edit}.")
#
# if __name__ == "__main__":
#     main_menu()








