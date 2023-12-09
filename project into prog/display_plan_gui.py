import tkinter as tk
from tkinter import ttk
import pandas as pd
from tkinter import messagebox
def display_plan():
    try:
        plan_id = int(entry.get())
        df = pd.read_csv("plan.csv")

        # Ensure that PlanID column exists and the DataFrame is not empty
        if 'PlanID' in df.columns and not df.empty:
            # Convert PlanID in DataFrame to integer if it's not already
            df['PlanID'] = df['PlanID'].astype(int)

            if plan_id in df['PlanID'].values:  # Use .values for checking membership
                plan_info = df[df['PlanID'] == plan_id]
                show_table(plan_info)
            else:
                messagebox.showerror("Error", "Plan ID not found")
        else:
            messagebox.showerror("Error", "No plans available")

    except ValueError:
        messagebox.showerror("Error", "Please enter a valid plan ID, numerical characters only")


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

def back(root):
    root.grid_forget()

def display_plan_frame(parent):
    global root
    # Create tkinter window
    root = tk.Frame(parent,width=600, height=600, bg='#021631')
    root.grid_propagate(False)

    # Create label and entry for Plan ID
    tk.Label(root, text="Enter Plan ID",font="calibri 16",bg="#021631", fg="#fff").place(x=240,y=200)

    global entry
    entry = tk.Entry(root,width=20, bd=2, font="calibri 10")
    entry.place(x=230, y=270)

    # Create 'Display Plan' button
    button = tk.Button(root, text="Display Plan", bg="#FFFFFF", command=display_plan)
    button.place(x=270, y=320)

    back_button=tk.Button(root, text="Back", width=10, bg="#FFFFFF", command=lambda:back(root))
    back_button.place(x=270, y=500)

    return root

if __name__=='__main__':
    root = tk.Tk()
    root.title("Admin home page")
    root.eval("tk::PlaceWindow . center")
    root.geometry("600x600")
    root['bg'] = '#021631'
    display_plan_frame(root)

    frame=display_plan_frame(root)
    frame.pack()

    root.mainloop()