import tkinter as tk
from tkinter import ttk
import csv

# Function to filter and display live updates
def filter_and_display_updates(selected_option, live_feed_text):
    # global selected_option
    live_feed_text.delete(1.0, tk.END)  # Clear the current content

    # Read live updates from "liveupdates.csv"
    with open("liveupdates.csv", mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) >= 4:
                timestamp, camp, update_message, categories = row[0], row[1], row[2], row[3]
                categories = categories.split(", ")
                categories = [category for category in categories]

                # Check if the entry matches the selected option
                if selected_option == "All" or selected_option in categories:
                    formatted_update = f"{timestamp} - Camp {camp}: {update_message}\n"
                    live_feed_text.insert(tk.END, formatted_update)
                elif selected_option == 'Resources' and '1' in categories[0]:
                    formatted_update = f"{timestamp} - Camp {camp}: {update_message}\n"
                    live_feed_text.insert(tk.END, formatted_update)
                elif selected_option == 'Weather' and '1' in categories[1]:
                    formatted_update = f"{timestamp} - Camp {camp}: {update_message}\n"
                    live_feed_text.insert(tk.END, formatted_update)
                elif selected_option == 'Emergency' and '1' in categories[2]:
                    formatted_update = f"{timestamp} - Camp {camp}: {update_message}\n"
                    live_feed_text.insert(tk.END, formatted_update)
                elif selected_option == 'Refugees' and '1' in categories[3]:
                    formatted_update = f"{timestamp} - Camp {camp}: {update_message}\n"
                    live_feed_text.insert(tk.END, formatted_update)
def back(frame):
    frame.grid_forget()
def on_option_selected(event):
    selected_option = dropdown.get()
    filter_and_display_updates(selected_option,live_feed_text)

def livefeed_frame(parent):
    frame = tk.Frame(parent, bg='#021631')
    frame.grid_rowconfigure(1, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    # Dropdown menu for filtering options
    options = ["All", "Resources", "Weather", "Emergency", "Refugees"]
    selected_option = tk.StringVar(frame)
    selected_option.set(options[0])

    options_label = tk.Label(frame, text="Select from the options to filter messages:", font="calibri 11",
                             bg="#021631", fg="#fff")
    options_label.grid(row=0, column=0, sticky='nsew')

    global dropdown
    dropdown = ttk.Combobox(frame, textvariable=selected_option, values=options, state="readonly")
    dropdown.bind("<<ComboboxSelected>>", on_option_selected)
    dropdown.grid(row=1, column=0, padx=0, pady=10)

    back_button = tk.Button(frame, text="Back", bg="#FFFFFF", fg="black", width=10, height=1, command=lambda: back(frame))
    back_button.grid(row=3, column=0, pady=10)

    text_frame = tk.Frame(frame, width=700, height=800, bg='#021631')
    text_frame.grid(row=2, column=0, pady=10, padx=10)

    global live_feed_text
    live_feed_text = tk.Text(text_frame, wrap=tk.WORD, height=20, width=60)
    live_feed_text.pack(padx=20, pady=80, anchor='w')

    filter_and_display_updates(selected_option,live_feed_text)

    return frame

    # root.mainloop()
