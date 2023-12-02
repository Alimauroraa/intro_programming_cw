import tkinter as tk
from tkinter import ttk, messagebox
import csv
from datetime import datetime

# Function to handle the submission of live updates
def submit_update():
    selected_camp = camp_var.get()
    update_message = update_entry.get()
    selected_categories = [category_var.get() for category_var in category_vars]

    # Check if camp, message, and at least one category are selected
    if selected_camp and update_message and any(selected_categories):
        # Generate a timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Write the update to "liveupdates.csv" as a new line with timestamp
        with open("liveupdates.csv", mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, selected_camp, update_message, ", ".join(selected_categories)])

        # Show a confirmation message with the timestamp
        confirmation_message = f"Live update has been successfully submitted on {timestamp}."
        messagebox.showinfo("Update Submitted", confirmation_message)

        # Clear the update message entry and checkboxes
        update_entry.delete(0, tk.END)
        for checkbox in checkboxes:
            checkbox.deselect()
    else:
        messagebox.showerror("Error", "Please select a camp, provide an update message, and select at least one category.")

# Read camp IDs from "plan.csv"
with open("camps.csv", mode='r') as file:
    reader = csv.reader(file)
    next(reader)
    camp_ids = [row[0] for row in reader]

# Create tkinter window
root = tk.Tk()
root.title("Live Updates")

root.configure(bg='#021631')

# Create a frame to center the widgets
frame = tk.Frame(root, bg = '#021631')
frame.place(relx=0.5, rely=0.5, anchor='center')

# Create label for camp selection
camp_label = tk.Label(frame, text="Select a Camp:", background="#021631", foreground="white")
camp_label.pack()

# Create a dropdown menu for camp selection
camp_var = tk.StringVar()
camp_dropdown = ttk.Combobox(frame, textvariable=camp_var, values=camp_ids)
camp_dropdown.pack()

# Create label and entry for live update message
update_label = tk.Label(frame, text="Enter your live update:", background="#021631", foreground="white")
update_label.pack()
update_entry = ttk.Entry(frame)
update_entry.pack()


message_label = tk.Label(frame, text="What is your live update message about? Check all the boxes that apply.", background = "#021631", foreground="white")
message_label.pack()
# Create checkboxes for message categories
category_labels = ["Resources", "Weather", "Emergency", "Refugees"]
category_vars = [tk.StringVar() for _ in category_labels]
checkboxes = []

for i, category_label in enumerate(category_labels):
    checkbox = tk.Checkbutton(frame, text=category_label, variable=category_vars[i], bg= "#021631" , fg="white")
    checkbox.pack()
    checkboxes.append(checkbox)

# Create a "Submit Update" button
submit_button = ttk.Button(frame, text="Submit Update", command=submit_update)
submit_button.pack()

# Set the window size
main_window_width = 700
main_window_height = 800

# Get screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculate the position to center the window
x_position = (screen_width - main_window_width) // 2
y_position = (screen_height - main_window_height) // 2
root.geometry(f"{main_window_width}x{main_window_height}+{x_position}+{y_position}")

root.mainloop()


