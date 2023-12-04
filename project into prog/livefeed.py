import tkinter as tk
from tkinter import ttk
import csv

# Function to filter and display live updates
def filter_and_display_updates():
    selected_categories = [category_vars[i].get() for i in range(len(category_vars))]
    live_feed_text.delete(1.0, tk.END)  # Clear the current content

    # Read live updates from "liveupdates.csv"
    with open("liveupdates.csv", mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) >= 4:
                timestamp, camp, update_message, categories = row[0], row[1], row[2], row[3]
                categories = categories.split(", ")
                categories = [int(category) for category in categories]

                # Check if the entry matches the selected categories
                if all(categories[i] == 1 if selected_categories[i] else True for i in range(len(selected_categories))):
                    formatted_update = f"{timestamp} - Camp {camp}: {update_message}\n"
                    live_feed_text.insert(tk.END, formatted_update)

# Create tkinter window
root = tk.Tk()
root.title("Camp message live feed")
root.configure(bg='#021631')

# Create a frame for the category checkboxes and live feed
frame = tk.Frame(root, bg='#021631')
frame.pack(padx=10, pady=10)

# Filter options for message categories
category_labels = ["Resources", "Weather", "Emergency", "Refugees"]
category_vars = [tk.IntVar() for _ in category_labels]
checkboxes = []

for i, category_label in enumerate(category_labels):
    checkbox = tk.Checkbutton(frame, text=category_label, variable=category_vars[i], bg="#021631", fg="white")
    checkbox.grid(row=i, column=0, sticky="w")
    checkboxes.append(checkbox)

# Create a "Filter Updates" button
filter_button = ttk.Button(frame, text="Filter Updates", command=filter_and_display_updates)
filter_button.grid(row=len(category_labels), column=0, columnspan=2, pady=10)

# Create a Text widget for displaying live updates
live_feed_text = tk.Text(root, wrap=tk.WORD, height=20, width=60)
live_feed_text.pack(padx=10, pady=10)

# Set the initial state of all checkboxes to unselected
for category_var in category_vars:
    category_var.set(0)

# Initially filter and display all updates
filter_and_display_updates()

root.mainloop()
