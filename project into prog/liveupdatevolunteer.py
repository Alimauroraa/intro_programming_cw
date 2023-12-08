import tkinter as tk
from tkinter import ttk, messagebox
import csv
from datetime import datetime

import pandas as pd
from GUI_volunteer_login_update import login

def submit_update():
    selected_camp = camp_dropdown.get()
    update_message = update_entry.get()

    # # Check if a camp is selected, a message is provided, and at least one category is selected
    # if selected_camp == "Select a Camp" or selected_camp == "":
    #     messagebox.showerror("Error", "Please select a camp.")
    #     return
    # if not update_message.strip():
    #     messagebox.showerror("Error", "Please provide an update message.")
    #     return
    # if not any(category_states.values()):
    #     messagebox.showerror("Error", "Please select at least one category.")
    #     return

    selected_categories = [int(state) for state in category_states.values()]

    # # Debug print statements
    # print(f"Selected camp: {selected_camp}")
    # print(f"Update message: {update_message}")
    # print(f"Selected categories: {selected_categories}")

    # Proceed with the update
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("liveupdates.csv", mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, selected_camp, update_message, *selected_categories])

    messagebox.showinfo("Update Submitted", f"Live update has been successfully submitted on {timestamp}.")

    # Clear inputs
    update_entry.delete(0, tk.END)
    for category in category_states:
        category_states[category] = False
    camp_dropdown.set("Select a Camp")

def toggle_category(category):
    category_states[category] = not category_states[category]

def go_back():
    root.destroy()
    from GUI_volunteer_login_update import main_application
    main_application()

def main_live_updates():
    # Read camp IDs from "camps.csv"
    with open("camps.csv", mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        camp_ids = ["Select a Camp"] + [row[0] for row in reader]

    global root
    root = tk.Tk()
    root.title("Live Updates")
    root.configure(bg='#021631')

    frame = tk.Frame(root, bg='#021631')
    frame.place(relx=0.5, rely=0.5, anchor='center')

    camp_label = tk.Label(frame, text="Select Your Camp to Send a Message!", background="#021631", foreground="white")
    camp_label.pack()

    df=pd.read_csv('volunteers_file.csv')
    username_entered=login(display_messages=False)
    filtered_df=df[df['username']==username_entered[1]]
    camp_id=filtered_df['camp_id'].astype(int).tolist()

    camp_dropdown = ttk.Combobox(frame, values=camp_id, state="readonly")
    camp_dropdown.set("Select a Camp")
    camp_dropdown.pack()

    update_label = tk.Label(frame, text="Enter your live update:", background="#021631", foreground="white")
    update_label.pack()
    update_entry = ttk.Entry(frame)
    update_entry.pack()

    message_label = tk.Label(frame, text="What is your live update message about? Check all the boxes that apply.", background="#021631", foreground="white")
    message_label.pack()

    category_labels = ["Resources", "Weather", "Emergency", "Refugees"]
    category_states = {category_label: False for category_label in category_labels}

    for category_label in category_labels:
        checkbox = tk.Checkbutton(frame, text=category_label, command=lambda label=category_label: toggle_category(label), bg="#021631", fg="white", selectcolor="#021631", activebackground="#021631", activeforeground="white")
        checkbox.pack()

    submit_button = ttk.Button(frame, text="Submit Update", command=submit_update,width=14)
    submit_button.pack(pady=10)

    go_back_button = ttk.Button(frame, text="Go Back", command=go_back,width=14)
    go_back_button.pack(pady=10)

    main_window_width = 700
    main_window_height = 800
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_position = (screen_width - main_window_width) // 2
    y_position = (screen_height - main_window_height) // 2
    root.geometry(f"{main_window_width}x{main_window_height}+{x_position}+{y_position}")

    root.mainloop()



# login()