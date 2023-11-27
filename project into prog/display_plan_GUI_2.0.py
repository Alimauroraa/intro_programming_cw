import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pandas as pd
from close_plan import ClosePlan
def load_plan_ids():
    df = pd.read_csv("plan.csv")
    return sorted(df['PlanID'].dropna().unique())

def display_plan():
    try:
        plan_id = int(combo.get())
        df = pd.read_csv("plan.csv")
        plan_info = df[df['PlanID'] == plan_id]
        if not plan_info.empty:
            show_info(plan_info)
        else:
            display_error("Plan ID not found.")
    except ValueError:
        display_error("Please enter a valid Plan ID.")

def display_volunteers(parent, dataframe):
    camp_id = []
    # Find CampID and get corresponding volunteer data
    if 'campID' in dataframe.columns:
        camps = dataframe.iloc[0]['campID']
        camp_list = [int(item) for item in camps.split(",")]
        volunteer_csv = pd.read_csv("volunteers_file.csv")
        volunteers_for_plan = volunteer_csv[volunteer_csv['camp_id'].isin(camp_list)]

        # Create a new top-level window
        volunteer_window = tk.Toplevel(parent)
        volunteer_window.title("Volunteers for Plan")

        # Create Treeview widget
        tree = ttk.Treeview(volunteer_window)
        tree["columns"] = list(volunteers_for_plan.columns)
        tree["show"] = "headings"

        # Define headings
        for col in tree["columns"]:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor="center")

        # Insert data into the treeview
        for idx, row in volunteers_for_plan.iterrows():
            tree.insert("", "end", values=list(row))

        tree.pack(expand=True, fill='both')

def display_refugees(parent, dataframe):
    camp_id = []
    # Find CampID and get corresponding volunteer data
    if 'campID' in dataframe.columns:
        camps = dataframe.iloc[0]['campID']
        camp_list = [int(item) for item in camps.split(",")]
        refugees_csv = pd.read_csv("Refugee_DataFrame.csv")
        refugees_for_plan = refugees_csv[refugees_csv['Camp_ID'].isin(camp_list)]

        # Create a new top-level window
        refugees_window = tk.Toplevel(parent)
        refugees_window.title("Refugees for Plan")

        # Create Treeview widget
        tree = ttk.Treeview(refugees_window)
        tree["columns"] = list(refugees_for_plan.columns)
        tree["show"] = "headings"

        # Define headings
        for col in tree["columns"]:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor="center")

        # Insert data into the treeview
        for idx, row in refugees_for_plan.iterrows():
            tree.insert("", "end", values=list(row))

        tree.pack(expand=True, fill='both')
def show_info(dataframe):
    top = tk.Toplevel(root)
    top.title("Plan Details")

    frame = ttk.Frame(top)
    frame.pack(padx=20, pady=10, expand=True, fill='both')

    for idx, col in enumerate(dataframe.columns):
        label = ttk.Label(frame, text=col)
        label.grid(row=idx, column=0, padx=5, pady=5, sticky="w")

        if col == 'active':
            active_value = dataframe.iloc[0][col]
            message = "Plan is currently active" if active_value != 0 else "Plan is inactive"
            messagebox.showinfo("Plan Status", message)
        else:
            entry = ttk.Entry(frame, width=100)
            entry.insert(tk.END, str(dataframe.iloc[0][col]))
            entry.grid(row=idx, column=1, padx=20, pady=10, sticky="w")
            entry.config(state=tk.DISABLED)  # Make the entry non-editable

    # Add the 'Display Volunteers for Plan' button at the bottom
    volunteers_button = ttk.Button(frame, text="Display Volunteers for Plan",command=lambda: display_volunteers(top, dataframe))
    volunteers_button.grid(row=len(dataframe.columns) + 1, column=0, pady=10, padx=5)

    refugees_button = ttk.Button(frame, text="Display Refugees for Plan",command=lambda: display_refugees(top, dataframe))
    refugees_button.grid(row=len(dataframe.columns) + 1, column=1, pady=10, padx=5)


def display_error(message):
    error_label.config(text=message)

# Create tkinter window
root = tk.Tk()
root.title("Display Plan")

root_window_width = 700
root_window_height = 800
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x_position = (screen_width - root_window_width) // 2
y_position = (screen_height - root_window_height) // 2

root.geometry(f"{root_window_width}x{root_window_height}+{x_position}+{y_position}")

# Load Plan IDs for combobox
plan_ids = load_plan_ids()

# Create combobox for Plan ID
label = ttk.Label(root, text="Select Plan ID:")
label.pack()
combo = ttk.Combobox(root, values=plan_ids)
combo.pack()

# Create 'Display Plan' button
button = ttk.Button(root, text="Display Plan", command=display_plan)
button.pack()


# Display error message
error_label = ttk.Label(root, text="", foreground="red")
error_label.pack()

# Run the tkinter main loop
root.mainloop()