import tkinter as tk
from tkinter import ttk
import pandas as pd
def display_plan():
    try:
        plan_id = int(entry.get())
        df = pd.read_csv("plan.csv")
        plan_info = df[df['PlanID'] == plan_id]
        show_table(plan_info)
    except ValueError:
        result_text.config(state=tk.NORMAL)
        result_text.delete('1.0', tk.END)
        result_text.insert(tk.END, "Please enter a valid Plan ID.")
        result_text.config(state=tk.DISABLED)
def show_table(dataframe):
    top = tk.Toplevel(root)
    top.title("Plan Details")

    tree = ttk.Treeview(top)
    tree.pack(fill="both", expand=True)

    scrollbar = ttk.Scrollbar(top, orient="vertical", command=tree.yview)
    scrollbar.pack(side="right", fill="y")

    tree.configure(yscrollcommand=scrollbar.set)

    tree["columns"] = list(dataframe.columns)
    tree["show"] = "headings"

    for column in dataframe.columns:
        tree.heading(column, text=column)

    for index, row in dataframe.iterrows():
        tree.insert("", tk.END, values=list(row))

# Create tkinter window
root = tk.Tk()
root.title("Display Plan")

# Create label and entry for Plan ID
label = tk.Label(root, text="Enter Plan ID:")
label.pack()
entry = tk.Entry(root)
entry.pack()

# Create 'Display Plan' button
button = tk.Button(root, text="Display Plan", command=display_plan)
button.pack()

# Create text widget to display the result
result_text = tk.Text(root, height=10, width=50)
result_text.pack()
result_text.config(state=tk.DISABLED)

# Run the tkinter main loop
root.mainloop()