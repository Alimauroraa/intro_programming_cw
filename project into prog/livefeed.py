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

def back(frame):
    frame.grid_forget()
def on_checkbox_change():
    filter_and_display_updates()

def livefeed_frame(parent):

    # Create a frame for the category checkboxes and live feed
    frame = tk.Frame(parent, bg='#021631')
    checkbox_frame= tk.Frame(frame, width=700, height=800,bg='#021631')
    checkbox_frame.pack(pady=10, padx=10, anchor="w")

    #create custom style for checkbox
    custom=ttk.Style()
    custom.configure('Custom.TCheckbutton',background='#021631', foreground='white', indicatoron=0)

    # Filter options for message categories
    global category_vars
    category_labels = ["Resources", "Weather", "Emergency", "Refugees"]
    category_vars = [tk.IntVar() for _ in category_labels]

    for i, category_label in enumerate(category_labels):
        checkbox = ttk.Checkbutton(checkbox_frame, text=category_label, variable=category_vars[i], style='Custom.TCheckbutton',command=on_checkbox_change)
        checkbox.grid(row=i+1, column=1, sticky="w")

    back_button= tk.Button(frame,text="Back", bg="#FFFFFF", fg="black", width=10, height=1,command=lambda:back(frame))
    back_button.pack(pady=10)

    #create label
    options_label=tk.Label(checkbox_frame,text="Select from the options to filter messages:", font="calibri 11", bg="#021631",fg="#fff")
    options_label.grid(row=0, column=0, columnspan=2, sticky='w')

    text_frame= tk.Frame(frame, width=700, height=800,bg='#021631')
    text_frame.pack(pady=10, padx=10, anchor="w")

    # Create a Text widget for displaying live updates
    global live_feed_text
    live_feed_text = tk.Text(text_frame, wrap=tk.WORD, height=20, width=60)
    live_feed_text.pack(padx=20, pady=50, anchor='w')
    # live_feed_text.grid(row=len(category_labels)+2, column=0, columnspan=2, pady=10, sticky='w')

    # Set the initial state of all checkboxes to unselected
    for category_var in category_vars:
        category_var.set(0)

    # Initially filter and display all updates
    filter_and_display_updates()

    return frame

    # root.mainloop()
